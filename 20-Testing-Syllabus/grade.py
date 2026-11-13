"""Self-grader for the test notebooks in this folder.

Usage
-----
    python grade.py                            # grade every test in this folder
    python grade.py "T03 - Methods and Functions Test.ipynb"
    python grade.py --solutions "T03 - ..."     # validate the test itself

The grader replays the notebook's code cells in order in a single namespace,
exactly like a kernel would, and reports every cell tagged ``check``.

Standard library only - Jupyter is not required to grade.

Exit code is 0 when every check passes, 1 otherwise.
"""

import argparse
import contextlib
import glob
import io
import json
import os
import re
import sys
import traceback

CODE_BLOCK = re.compile(r"```python\n(.*?)```", re.DOTALL)
HERE = os.path.dirname(os.path.abspath(__file__))


def is_check(cell):
    return "check" in cell.get("metadata", {}).get("tags", [])


def question_id(cell, fallback):
    return cell.get("metadata", {}).get("question", fallback)


def code_blocks(cell):
    return CODE_BLOCK.findall("".join(cell.get("source", [])))


def run_cell(source, namespace, name):
    """Execute one cell, returning (ok, error_text, captured_output).

    Anything the cell prints is captured rather than shown, so a graded run
    stays readable; the captured text is only reported for a failing check.
    """
    buffer = io.StringIO()
    try:
        with contextlib.redirect_stdout(buffer):
            exec(compile(source, name, "exec"), namespace)
        return True, None, buffer.getvalue()
    except Exception:
        error = traceback.format_exc(limit=2).strip().splitlines()[-1]
        return False, error, buffer.getvalue()


def grade(path, solutions=False, verbose=False):
    with open(path, encoding="utf-8") as handle:
        document = json.load(handle)

    namespace = {"__name__": "__main__"}
    passed = failed = 0
    failures = []
    problems = []

    for index, cell in enumerate(document["cells"]):
        source = "".join(cell.get("source", []))
        label = question_id(cell, "cell-%d" % (index + 1))

        if cell["cell_type"] == "markdown":
            if solutions:
                for block in code_blocks(cell):
                    ok, error, _ = run_cell(block, namespace, "<solution>")
                    if not ok:
                        problems.append("solution block failed: %s" % error)
            continue

        if is_check(cell):
            ok, error, captured = run_cell(source, namespace, "<check %s>" % label)
            if ok:
                passed += 1
                if verbose:
                    print("  [PASS] %s" % label)
            else:
                failed += 1
                detail = error
                if captured.strip():
                    detail = "%s | output: %s" % (error, captured.strip().splitlines()[-1])
                failures.append((label, detail))
            continue

        # Ordinary cell (student answer or setup).
        ok, error, _ = run_cell(source, namespace, "<cell %d>" % (index + 1))
        if not ok and solutions:
            problems.append("cell %d failed: %s" % (index + 1, error))

    return passed, failed, failures, problems


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("notebook", nargs="*", help="notebook file(s) to grade")
    parser.add_argument("--solutions", action="store_true",
                        help="also run the reference solutions (validates the test)")
    parser.add_argument("-v", "--verbose", action="store_true", help="list passing checks too")
    args = parser.parse_args(argv)

    if args.notebook:
        targets = args.notebook
    else:
        # Every notebook that carries check cells: the section tests, the
        # practice drills and the final exam.
        targets = sorted(glob.glob(os.path.join(HERE, "T*.ipynb")))
        targets += sorted(glob.glob(os.path.join(HERE, "PRACTICE*.ipynb")))
        targets += sorted(glob.glob(os.path.join(HERE, "FINAL*.ipynb")))

    if not targets:
        print("no notebooks found in %s" % HERE)
        return 1

    total_pass = total_fail = 0
    bad = 0

    for target in targets:
        if not os.path.isabs(target):
            candidate = os.path.join(HERE, target)
            if os.path.exists(candidate):
                target = candidate
        name = os.path.basename(target)
        passed, failed, failures, problems = grade(target, args.solutions, args.verbose)
        total_pass += passed
        total_fail += failed

        status = "OK " if not failed and not problems else "BAD"
        if failed or problems:
            bad += 1
        print("[%s] %-58s %d/%d checks passed" % (status, name, passed, passed + failed))
        for label, error in failures:
            print("        FAIL %s: %s" % (label, error))
        for problem in problems:
            print("        PROBLEM %s" % problem)

    print("\n%d checks passed, %d failed across %d notebooks." % (total_pass, total_fail, len(targets)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
