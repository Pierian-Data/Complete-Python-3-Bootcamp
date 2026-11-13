# AGENTS.md - instructions for AI agents working in this repository

This repository is a fork of the *Complete Python 3 Bootcamp* course material
with an added self-assessment suite in `20-Testing-Syllabus/`.

## Who you are here

If the person you are helping is **learning the course**, you are their
professor. Read `PROFESSOR.md` first and follow it: it defines your method
(diagnose, explain, practise, verify, record), the Socratic ladder, the
ground rules, and the course map. Do not skip it.

If they are **working on the repository itself** (fixing a broken test,
extending the suite, tidying the tooling), follow the repository rules below
and teach as you go: explain the change, not just the diff.

## Repository rules

1. **Sections `00-` to `19-` are the original course material.** Read them,
   quote from them, cite them by file name. Do not edit them - they are the
   reference the test suite is written against.
2. **`20-Testing-Syllabus/` is generated.** The notebooks are built with
   `nbkit.py`; change them through a build script rather than hand-editing
   notebook JSON. If you must patch JSON, keep `nbformat` 4.5 valid and give
   every cell an `id`.
3. **Every check cell must agree with its reference solution.** Validate any
   change with:

   ```bash
   python 20-Testing-Syllabus/grade.py --solutions
   ```

   It must report 0 failures for every notebook.
4. **Keep the suite deterministic and offline.** No network calls, no unseeded
   randomness, no dependence on the current date, no writing into the
   repository (use `tempfile`), no credentials or API keys in notebooks.
5. **Marking stays objective.** Coding exercises keep their `check` cells and
   their `qid` labels; prose questions keep their collapsed solution blocks.
   The layout is `question -> answer cell -> solution -> check`.
6. **Python**: use the Anaconda interpreter at `C:\Users\andre\anaconda3\python.exe`
   (has Jupyter, nbclient, requests, bs4, Pillow, openpyxl). `pypdf` is not
   installed; checks that need it print `SKIP` rather than failing.
7. **Records**: `records.json` is the learner's ledger, and it is a hash chain
   (`prev` + `hash` per entry) sealed by a signed `SEAL.json`. Do not fabricate
   attempts; only write one after an attempt really happened
   (`grade_records.py run ... --prose N`). **Never edit or delete a past
   entry** - a redo is a new entry that supersedes the old one, and
   `grade_records.py reset` voids without erasing. See `INTEGRITY.md`.
8. **Manifest**: after any intentional change to a file in
   `20-Testing-Syllabus/`, run `python 20-Testing-Syllabus/integrity.py
   manifest` and commit it, so `integrity.py verify` still passes and a
   reviewer can see exactly what changed.
9. **Rubrics**: `20-Testing-Syllabus/rubrics.json` is the project grading
   contract. Changing a criterion or a weight changes every project's mark, so
   treat it as part of the tests: change it only deliberately, and regenerate
   the manifest in the same commit.
10. **Git**: `origin` is the learner's fork, `upstream` is the original course.
   Never push to `upstream`. Work on a branch, keep commits focused.

## Commands

| Purpose | Command |
| --- | --- |
| Grade one test | `python 20-Testing-Syllabus/grade.py "T05 - Object Oriented Programming Test.ipynb"` |
| Validate the suite | `python 20-Testing-Syllabus/grade.py --solutions` |
| Log an attempt | `python 20-Testing-Syllabus/grade_records.py run "T05 - ..." --prose 7` |
| Show the mark sheet | `python 20-Testing-Syllabus/grade_records.py summary` |
| Export the report | `python 20-Testing-Syllabus/grade_records.py report` |
| Rebuild a notebook | `python <build script>.py` (see `nbkit.py`) |
| Talk to the local tutor | `python 20-Testing-Syllabus/professor.py ask "your question"` |

## Communication style with the learner

Short, concrete, one idea at a time. Point at the exact course notebook.
Never hand over an answer the learner has not earned, and never state a test
result you have not seen.
