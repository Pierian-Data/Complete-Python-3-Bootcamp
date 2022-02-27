# Written by Eric Martin for COMP9021


from IPython.core.magic import register_cell_magic
from difflib import Differ
from itertools import cycle
from pathlib import Path
from subprocess import run, TimeoutExpired
from tempfile import NamedTemporaryFile
from neotermcolor import colored, cprint
import codecs
import re

import neotermcolor
neotermcolor.tty_aware = False

@register_cell_magic
def run_and_test(magic_arguments, outputs_inputs):
    '''Options are:
    -e followed by a space or another option, to express that an
       error is supposed to be raised;
    -i followed by a string, denoting the input to provide, with \\n
       expressing that user presses carriage return;
    -r followed by : possibly surrounded by integers (possibly
       preceded by - but not by +), denoting the range of output to
       examine, the integer to the left defaulting to 0, the integer
       to the right defaulting to the length of the output;
    -t followed a positive integer, denoting maximum running time,
       expressed in seconds, set to 10 by default;
    -s followed a positive integer, denoting maximum output size,
       expressed in bytes, set to 1000 by default.
       
    After the options comes the command to be run, expected to be of
    one of these forms:\n        python3 filename.py
    or\n        python3 -c python_statements_enclosed_by_quotes
    
    The cell is meant to store one or more strings, all surrounded by
    (single or triple) quotes, the first of which can be preceded by
    an arbitrary amount of space, the last of which can be followed
    by an arbitrary amount of space, two successive strings being
    separated by no other characters but spaces and at most one comma.
    
    Strings not separated by a comma are meant to be concatenated.
    
    When using triple quotes, the convention is that all lines between
    the surrounding triple quotes end in \\n, without following spaces;
    such spaces would indeed not be immediately visible in the cell.
    
    Strings separated by a comma represent program output for one and
    user input for the other; the first string represents program
    output.
    
    A string can span many lines, and is then meant to be no different
    to a string written on a single line, be it surrounded by single
    quotes. New line characters are meant to be explicitly indicated.
    For instance,
    'one\n     two'
    (with no space after one) represents the string 'one two', whereas
    'one\\n\n    two'
    (with no space after \\n) represents the string 'one\\ntwo'.
    '''
    # magic_arguments is a string (not ending in \n) that captures the
    # arguments to the magic on the line where it is invoked.
    # Occurrences of embedded \n on the line appear as \\n in the
    # string. The following statement changes all those \\n to \n,
    # so the character \ followed by the character n to the new line
    # character.
    magic_arguments = codecs.decode(magic_arguments, 'unicode_escape').strip()
    options = {}
    # Up to 5 options to process.
    for _ in range(5):
        try:
            offset = process_possible_option(magic_arguments, options)
            if not offset:
                break
            magic_arguments = magic_arguments[offset :].lstrip()
        except CommandToRunError as e:
            print(e)
            return
    if not magic_arguments.startswith('python3 '):
        print('No call to python3 (possibly after options)')
        return
    # len('python3 ') == 8
    magic_arguments = magic_arguments[8 :].lstrip()
    if magic_arguments.startswith('-c'):
        magic_arguments = magic_arguments[2 :].lstrip()
        if len(magic_arguments) < 2 or magic_arguments[0] not in '\'"'\
           or magic_arguments[-1] != magic_arguments[0]:
            print('python3 -c not followed by string')
            return
        # - Get rid of the surrounding quotes, as magic_arguments itself
        #   is a string.
        # - Let repr() escape quotes if needed.
        # - Get rid of the surrounding quotes of the string returned by
        #   repr().
        statements = repr(magic_arguments[1 : -1])[1 : -1]
        # It is assumed that there is a unique import statement of this
        # kind, for a module that is stored in the working directory.
        match = re.search('from (\S+) import \*', statements)
        if match:
            module = match.groups()[0] + '.py'
            if not Path(module).exists():
                print(module, 'is not an existing Python module')
                return
            with NamedTemporaryFile('w', dir='.', suffix='.py') as temp_file:
                expand_with_echoed_input(module, temp_file)
                # temp_file.name is the name of an absolute path to a
                # temporary file.
                # Path(temp_file.name).stem is used to extract only
                # the name of that file, without the .py extension.
                # match.span() is the start and end+1 positions of the
                # occurrence, in magic_arguments, of the name of the
                # module all of whose contents is to be imported.
                p = execute(('python3', '-B', '-c',
                             statements.replace(
                                 statements[slice(*match.span())],
                                 f'from {Path(temp_file.name).stem} import *'
                                               )
                            ), options
                           )
        else:
            p = execute(('python3', '-B', '-c', statements), options)
    elif not magic_arguments.endswith('.py')\
         or not Path(magic_arguments).exists():
        print(magic_arguments, 'is not an existing Python module')
        return
    else:
        # It is assumed that the module to run is stored in the working
        # directory.
        with NamedTemporaryFile('w', dir='.') as temp_file:
            expand_with_echoed_input(magic_arguments, temp_file)
            p = execute(('python3', '-B', temp_file.name), options)
    if not p:
        return
    size_limit = options.get('-s') or 1000
    start, end = options.get('-r', (None, None))
    try:
        error = p.stderr[p.stderr.rindex('\n', 0, -1) + 1 :]
    except ValueError:
        error = ''
    if '-e' in options:
        program_output = error
    elif p.stderr:
        cprint('PROGRAM PRODUCED AN ERROR\n', attrs='bold')
        print(error)
        return
    elif len(p.stdout) > size_limit:
        cprint('TOO MUCH OUTPUT, DISPLAYING MAX ALLOWED\n',
               attrs='bold'
              )
        print(p.stdout[: size_limit][slice(start, end)])
        return
    else:
        program_output = p.stdout[slice(start, end)]
    # outputs_inputs is a string that represents the cell contents,
    # with the end of each line in the cell represented by \n, and with
    # all embedded \n represented by \\n. For instance, if the cell
    # contains
    # 'one
    #  two'
    # then outputs_inputs contains 'one\n two' (the quotes being
    # escaped in case outputs_inputs is itself surrounded by simple
    # quotes), whereas if the cell contains
    # 'one\n
    # two'
    # then outputs_inputs contains 'one\\n\ntwo' (with the same remark
    # on the quotes).
    # Recall:
    # - an occurrence of \n not preceeded by \ is the new line
    #   character;
    # - an occurrence of \\n is two characters: \ followed by n.
    # The call to eval() returns a string in case no successive strings
    # within outputs_inputs have a comma in-between, and a tuple of
    # at least 2 strings otherwise.
    outputs_inputs = eval(outputs_inputs.replace('\n', ''))
    if isinstance(outputs_inputs, str):
        outputs_inputs = [outputs_inputs]
    expected_output = ''.join(outputs_inputs)
    cprint('PASSED' if program_output == expected_output else 'FAILED',
           attrs='bold'
          )
    if start:
        if start == 1:
            cprint(f'IGNORING FIRST CHARACTER OF OUTPUT', attrs='underline')
        elif start > 0:
            cprint(f'IGNORING FIRST {start} CHARACTERS OF OUTPUT',
                   attrs='underline'
                  )
        elif start == -1:
            cprint(f'IGNORING ALL BUT LAST CHARACTER OF OUTPUT',
                   attrs='underline'
                  )
        else:
            cprint(f'IGNORING ALL BUT LAST {-start} CHARACTERS OF OUTPUT',
                   attrs='underline'
                  )
    if end:
        if end == -1:
            cprint(f'IGNORING LAST CHARACTER OF OUTPUT', attrs='underline')      
        elif end < 0:
            cprint(f'IGNORING LAST {-end} CHARACTERS OF OUTPUT', 
                   attrs='underline'
                  )
        elif end == 1:
            cprint(f'IGNORING ALL BUT FIRST CHARACTER OF OUTPUT',
                   attrs='underline'
                  )
        else:
            cprint(f'IGNORING ALL BUT FIRST {end} CHARACTERS OF OUTPUT',
                   attrs='underline'
                  )
    if program_output and program_output[-1] != '\n'\
       and expected_output and expected_output[-1] != '\n':
        program_output += '\n'
        expected_output += '\n'
    elif program_output and program_output[-1] != '\n':
        cprint('MISSING NEW LINE AT END OF OUTPUT NOT SHOWN IN DIFF',
               attrs='bold'
              )
        program_output += '\n'
    elif expected_output and expected_output[-1] != '\n':
        cprint('EXTRA NEW LINE AT END OF OUTPUT NOT SHOWN IN DIFF',
               attrs='bold'
              )
        expected_output += '\n'
    print()
    coloured_lines = []
    if len(outputs_inputs) > 1:
        grey_or_blue = cycle(('grey', 'blue'))
        coloured_snippets = []
        snippet = [' ']
        starting_new_line = True
        for output_or_input in outputs_inputs:
            colour = next(grey_or_blue)
            for c in output_or_input:
                snippet.append(c)
                if c == '\n':
                    coloured_snippets.append([snippet, colour])
                    coloured_lines.append(coloured_snippets)
                    coloured_snippets = []
                    snippet = [' ']
                    starting_new_line = True
                else:
                    starting_new_line = False
            if snippet and (not starting_new_line or snippet != [' ']):
                coloured_snippets.append([snippet, colour])
                snippet = [' '] if starting_new_line else []
        if coloured_snippets:
            coloured_lines.append(coloured_snippets)
        if expected_output[-1] != '\n':
            coloured_lines[-1][-1][0].append('\n')
    for line in coloured_diff(program_output, expected_output,
                              coloured_lines
                             ):
        print(line, end='')


def process_possible_option(magic_arguments, options):
    prefix = magic_arguments[: 2]
    if len(prefix) < 2 or prefix[0] != '-' or prefix[1] not in 'eirst':
        return 0
    if prefix in options:
        raise CommandToRunError(f'Option {prefix} provided more than once')
    if prefix[1] == 'e':
        if len(magic_arguments) < 3 or magic_arguments[2] not in ' -':
            raise CommandToRunError(f'Option {prefix} not followed by '
                                    'space or another option'
                                   )
        options[prefix] = True
        return 2
    if prefix[1] in 'ts':
        match = re.compile('\s*\d+').match(magic_arguments, 2)
        try:
            argument = int(match.group())
        except AttributeError:
            raise CommandToRunError(f'Option {prefix} not followed by digits')
        options[prefix] = argument
        return match.span()[1]
    if prefix[1] == 'r':
        match = re.compile('\s*((?:-\d)?\d*)\s*:'
                           '\s*((?:-\d)?\d*)'
                          ).match(magic_arguments, 2)
        try:
            start, end = (m or None for m in match.groups())
        except AttributeError:
            raise CommandToRunError(f'Option {prefix} not followed by : '
                                    'possibly with integers on either side'
                                   )
        if start is not None:
            try:
                start = int(start)
            except AttributeError:
                raise CommandToRunError(f'Option {prefix} not with possibly '
                                        'minus sign and nondigits preceding :'
                                       )
        if end is not None:
            try:
                end = int(end)
            except AttributeError:
                raise CommandToRunError(f'Option {prefix} not with possibly '
                                        'minus sign and nondigits preceding :'
                                       )
        options[prefix] = start, end
        return match.span()[1]
    offset = len(magic_arguments)
    magic_arguments = magic_arguments[2 :].lstrip()
    offset -= len(magic_arguments)
    if not any(magic_arguments.startswith(quote) for quote in '\'"'):
        raise CommandToRunError(f'Option {prefix} not followed by string')
    quote = magic_arguments[0]
    match = re.compile(f'.*?[^\\\\]{quote}',
                       re.DOTALL
                      ).search(magic_arguments, 1)
    if match is None:
        raise CommandToRunError(f'Option {prefix} not followed by string')
    options[prefix] = match.group()[: -1]
    return match.span()[1] + offset


def expand_with_echoed_input(module, filename):
    with open(filename.name, 'w') as file:
        file.write('import builtins\n'
                   'def input(prompt):\n'
                   '    user_input = builtins.input(prompt)\n'
                   '    print(user_input)\n'
                   '    return user_input\n'
                  )
        file.writelines(open(module))


def execute(executable, options):
    try:
        return run(executable, capture_output=True,
                   input=options.get('-i'),
                   timeout=options.get('-t') or 10,
                   encoding='utf8'
                  )
    except TimeoutExpired:
        cprint('MAX RUNNING TIME EXCEEDED, PROGRAM KILLED\n', attrs='bold')


def coloured_diff(a, b, coloured_lines):
    class Cdiffer(Differ):
        def __init__(self, *args, **kargs):
            super().__init__(*args, **kargs)

        def compare(self, a, b, coloured_lines):
            diff = super().compare(a, b)
            colours = {' ': 'grey', '+': 'red', '-': 'green', '?': 'yellow'}
            if not coloured_lines:
                return [colored(line, colours[line[0]]) for line in diff]
            coloured_diff = []
            line_nb = -1
            for line in diff:
                line_nb += line[0] in ' +'
                if line[0] == ' ':
                    coloured_diff.extend(colored(''.join(snippet), colour)
                                             for snippet, colour in
                                                    coloured_lines[line_nb]
                                        )
                else:
                    coloured_diff.append(colored(line, colours[line[0]]))
            return coloured_diff

    return Cdiffer().compare(a.splitlines(keepends=True),
                             b.splitlines(keepends=True), coloured_lines
                            )


class CommandToRunError(Exception):
    pass


def load_ipython_extension(ipython):
    ipython.register_magic_function(run_and_test, 'cell')    