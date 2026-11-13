# Testing Syllabus - self-assessment suite

A marked test for every section of the Complete Python 3 Bootcamp course in
this repository. Work through the lecture notebooks, then take the matching
test and let the grader mark the coding half for you.

## Contents

| File | What it is |
| --- | --- |
| `00 - Testing Syllabus.ipynb` | The blueprint: what is tested, weights, pass bands, prerequisites, eight-week study plan, readiness checklist. |
| `01 - How to Use the Test Suite.ipynb` | Workflow, marking rules, grader usage, troubleshooting, how to add your own tests. |
| `02 - Grading Records.ipynb` | Live mark sheet: best score per module, weighted course mark, band, sign-off checklist, attempt history. |
| `03 - Project Portfolio.ipynb` | One portfolio project per course section: deliverables to tick, and the README entry to copy. |
| `T00` ... `T19` | One marked test per course section, 20 points each. |
| `99 - Final Comprehensive Exam.ipynb` | Cumulative exam: 36 questions, 60 points. |
| `grade.py` | Self-grader. Standard library only. |
| `grade_records.py` | Ledger tool: logs attempts, computes the course mark, exports `GRADE_REPORT.md`. |
| `records.json` | The ledger: one entry per attempt. Plain JSON, yours to edit or import. |
| `GRADE_REPORT.md` | Generated report - commit it into your portfolio repository as proof of work. |
| `nbkit.py` | Small builder used to generate the notebooks in this folder. |

The `T**` file names line up with the numbered course folders at the root of
the repository: `T05` tests `05-Object Oriented Programming`, and so on.

## Marking

Every coding exercise is followed by a `check` cell containing `assert`
statements. The grader replays the notebook's code cells in order and reports
each check as PASS or FAIL:

```
C:\Users\andre\anaconda3\python.exe 20-Testing-Syllabus\grade.py "T03 - Methods and Functions Test.ipynb"
```

```
[OK ] T03 - Methods and Functions Test.ipynb                       6/6 checks passed
        FAIL Q7: AssertionError

0 checks passed, 0 failed across 1 notebooks.
```

Without arguments it grades every test in the folder. With `--solutions` it
also runs the reference solutions, which is how you check that a failing
assertion is your mistake and not a broken test:

```
C:\Users\andre\anaconda3\python.exe 20-Testing-Syllabus\grade.py --solutions
```

The grader needs only a Python 3 interpreter. It exits with status 1 if any
check failed, so it can be used from a script or CI job.

Prose questions (multiple choice, conceptual, predict-the-output) are marked
by you against the collapsed solution next to each question.

## Grading records

Every attempt is logged in `records.json`. The best attempt per module counts
towards your mark:

```
C:\Users\andre\anaconda3\python.exe 20-Testing-Syllabus/grade_records.py run "T03 - Methods and Functions Test.ipynb" --prose 7
C:\Users\andre\anaconda3\python.exe 20-Testing-Syllabus/grade_records.py summary
C:\Users\andre\anaconda3\python.exe 20-Testing-Syllabus/grade_records.py report
```

`run` grades the notebook as saved, counts the checks that pass and asks for
the points for the hand-marked questions (`--prose`, 1 point per multiple
choice or conceptual question). `summary` prints the per-module best scores,
the weighted course mark and the band. `report` writes `GRADE_REPORT.md`.

The course mark is `0.85 * section mark + 0.15 * final exam`, with the module
weights from `00 - Testing Syllabus.ipynb`. `02 - Grading Records.ipynb` shows
the same information as live notebook output.

## Portfolio

`03 - Project Portfolio.ipynb` gives you one project per course section, the
deliverables that make it portfolio ready, and the README entry to copy into
your own repository. The capstone (section 18) is the flagship project; the
other nineteen entries are supporting evidence.

## Requirements

- Python 3.8 or newer for the grader (standard library only).
- Jupyter or JupyterLab to work through the notebooks.
- Optional, only for full marks on the tooling sections: `requests`,
  `beautifulsoup4`, `pillow`, `pypdf`, `openpyxl`. Checks that need a missing
  package skip themselves instead of failing.

## Rules the suite keeps

- Deterministic: no network, no unseeded randomness, no dependence on the
  current date.
- Nothing writes into the repository; file exercises use `tempfile`.
- No credentials, API keys or email accounts needed.
- Retakes are unlimited.

## Adding your own test

`nbkit.py` writes a valid notebook from a list of cells:

```python
import sys
sys.path.insert(0, r"C:/Users/andre/Learning/Udemy-Complete-Python-3-Bootcamp/20-Testing-Syllabus")
from nbkit import md, code, check, solution, nb

cells = [
    md("### Q1. Add two numbers\n\nDefine `add(a, b)` returning the sum."),
    code("# your answer here"),
    solution("def add(a, b):\n    return a + b", "Arguments are positional by default."),
    check("assert add(2, 3) == 5", qid="Q1"),
]

nb(r".../20-Testing-Syllabus/T99 - My Extra Test.ipynb", cells)
```

Keep the order `question -> answer -> solution -> check`: the grader walks the
notebook once from top to bottom, so the reference solution must be defined
before the check runs. Always validate a new test with
`grade.py --solutions` before handing it out.
