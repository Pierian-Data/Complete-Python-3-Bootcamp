"""nbkit - tiny, dependency-free builder for the notebooks in this folder.

Only the standard library is used, so the test notebooks can be rebuilt on any
Python 3 install without installing anything.

Cell order is meaningful for the self-grader (grade.py):

    question  -> markdown
    answer    -> code      (empty, the student writes here)
    solution  -> markdown  (<details> block; executed only by --solutions)
    check     -> code      (tagged "check"; asserts the student's answer)

The solution block deliberately sits *before* the check so that a single
forward pass works for both grading modes.
"""

import hashlib
import json
import os

__all__ = ["md", "code", "check", "solution", "nb"]


def _src(text):
    lines = text.strip("\n").split("\n")
    return [line + "\n" for line in lines[:-1]] + [lines[-1]]


def md(text):
    """Markdown cell."""
    return {"cell_type": "markdown", "metadata": {}, "source": _src(text)}


def code(text, qid=None):
    """Code cell. `qid` labels the cell for the grader output."""
    metadata = {}
    if qid:
        metadata["question"] = qid
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": metadata,
        "outputs": [],
        "source": _src(text),
    }


def check(text, qid=None):
    """Code cell that asserts the student's work. Always tagged 'check'."""
    cell = code(text, qid=qid)
    cell["metadata"]["tags"] = ["check"]
    return cell


def solution(code_text, why=""):
    """Collapsed markdown block holding the reference solution."""
    body = "<details>\n<summary>Solution</summary>\n\n```python\n%s\n```\n" % code_text.strip("\n")
    if why:
        body += "\n**Why:** %s\n" % why.strip()
    body += "\n</details>"
    return md(body)


def nb(path, cells):
    """Write a notebook to `path` (relative or absolute). Returns the path."""
    document = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "version": "3.14",
                "mimetype": "text/x-python",
                "file_extension": ".py",
                "pygments_lexer": "ipython3",
                "nbconvert_exporter": "python",
                "codemirror_mode": {"name": "ipython", "version": 3},
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    target = os.path.abspath(path)
    os.makedirs(os.path.dirname(target), exist_ok=True)
    for index, cell in enumerate(document["cells"]):
        if "id" not in cell:
            digest = hashlib.md5(
                ("%d|%s" % (index, "".join(cell.get("source", [])))).encode("utf-8")
            ).hexdigest()[:8]
            cell["id"] = digest
    with open(target, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(document, handle, indent=1, ensure_ascii=False)
        handle.write("\n")
    return path
