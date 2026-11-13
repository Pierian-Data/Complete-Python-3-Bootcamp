# Testing Syllabus - self-assessment suite

A marked test for every section of the Complete Python 3 Bootcamp course in
this repository. Work through the lecture notebooks, then take the matching
test and let the grader mark the coding half for you.

## Contents

| File | What it is |
| --- | --- |
| `S0 - Testing Syllabus.ipynb` | The blueprint: what is tested, weights, pass bands, prerequisites, eight-week study plan, readiness checklist. |
| `S1 - How to Use the Test Suite.ipynb` | Workflow, marking rules, grader usage, troubleshooting, how to add your own tests. |
| `S2 - Grading Records.ipynb` | Live mark sheet: best score per module, weighted course mark, band, sign-off checklist, attempt history. |
| `S3 - Project Portfolio.ipynb` | One portfolio project per course section: deliverables to tick, and the README entry to copy. |
| `S4 - AI Tutor.ipynb` | How to reach the professor: the agent in this repo, the local `professor.py` CLI, or any chat assistant. |
| `S5 - Using the Learning System.ipynb` | The lesson: how the pieces fit together, how to take a test, do a project, log progress, and the weekly loop. |
| `PRACTICE - Practice Test.ipynb` | A dry run of the test mechanics. Not graded for the mark. |
| `PRACTICE - Practice Project - Book Tracker.ipynb` | A practice project: full brief, four stages, and the rubric to self-score against. |
| `rubrics.json` | The project grading contract: six criteria, weights, and the 0-4 scale. |
| `professor.py` | Local AI tutor CLI. Talks to any OpenAI-compatible endpoint (OpenAI, OpenRouter, Ollama, LM Studio), grounded in the course material and your record. |
| `T00` ... `T19` | One marked test per course section, 20 points each. |
| `FINAL - Final Comprehensive Exam.ipynb` | Cumulative exam: 36 questions, 60 points. |
| `grade.py` | Self-grader. Standard library only. |
| `grade_records.py` | Ledger tool: logs attempts, computes the course mark, exports `GRADE_REPORT.md`. |
| `records.json` | The ledger: a hash-chained entry per attempt. Plain JSON, yours to read. |
| `integrity.py` | Tamper evidence: manifest of every file, signed seal over the chain, attestation writer, verifier. |
| `SEAL.json` | The signed seal: chain head + manifest + attestations, Ed25519 signed. |
| `suite.manifest.json` | SHA-256 of every file in this folder, so a weakened test cannot pass unnoticed. |
| `agent.pub` | The professor agent's public key. The private key lives outside the repository. |
| `INTEGRITY.md` | What the scheme guarantees, what it cannot, and how to anchor the seal externally. |
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
weights from `S0 - Testing Syllabus.ipynb`. `S2 - Grading Records.ipynb` shows
the same information as live notebook output.

## Portfolio

`S3 - Project Portfolio.ipynb` gives you one project per course section, the
deliverables that make it portfolio ready, and the README entry to copy into
your own repository. The capstone (section 18) is the flagship project; the
other nineteen entries are supporting evidence.

## The professor

`PROFESSOR.md` at the repository root is the operating manual for an AI tutor
that teaches this course: diagnose the misconception first, explain from the
actual lecture notebook, practise, verify with the grader, record the attempt.

Three ways to reach it:

```
# A. the agent already in this repository (Claude Code, Copilot, Cursor, ...)
#    AGENTS.md makes it behave like the professor - nothing to set up

# B. the local tutor CLI
C:\Users\andre\anaconda3\python.exe 20-Testing-Syllabus/professor.py ask --section 02 "why does range(0, 6) give me five items?"
C:\Users\andre\anaconda3\python.exe 20-Testing-Syllabus/professor.py ask --check "T02 - Python Statements Test.ipynb" "why did Q7 fail?"
C:\Users\andre\anaconda3\python.exe 20-Testing-Syllabus/professor.py office-hours --section 05
C:\Users\andre\anaconda3\python.exe 20-Testing-Syllabus/professor.py check "T02 - Python Statements Test.ipynb"

# C. any chat assistant: paste PROFESSOR.md as the system prompt
```

Route B needs a model. Set `PROFESSOR_API_KEY` for a hosted model, or point it
at a local one:

```
set PROFESSOR_BASE_URL=http://localhost:11434/v1
set PROFESSOR_MODEL=llama3.1
```

Use `--offline` to see the exact payload that would be sent without calling
anything.

## Integrity - tamper evidence

The ledger is append-only and hash-chained: every entry carries the hash of
its predecessor and of its own content, plus the SHA-256 and git blob id of
the notebook that was graded. The suite itself is covered by a manifest of
file hashes, and a signed `SEAL.json` binds the chain head to that manifest.

The manifest has two classes, because you are meant to edit some of these
files:

- **System files** (the grader, the ledger, the professor CLI, the rubrics, the
  docs) - any change fails the verify.
- **Your notebooks** (`T**`, `PRACTICE`, `FINAL`) - writing your answers is
  expected and reported as an expected change. But their *grading logic* is
  fingerprinted: change a check cell or a reference solution and the verify
  fails.

```bash
python 20-Testing-Syllabus/integrity.py verify     # chain + manifest + seal + attestations
python 20-Testing-Syllabus/integrity.py manifest   # re-hash the suite after an intentional change
python 20-Testing-Syllabus/integrity.py seal       # sign the current state
```

**Redoing a test or a project is documented, never erased.** A redo is a new
entry that names the attempt it supersedes; the best attempt per module is
the one that counts; `grade_records.py reset` voids an attempt but keeps the
history. `INTEGRITY.md` has the full protocol, the threat model, and how to
anchor the seal somewhere you do not control (GitHub artifact attestation,
OpenTimestamps).

## Version control - what lives where

Everything in this folder is a git-tracked file, so the whole suite, your
grades and your work live in your fork's history.

| Thing | Where | In git? |
| --- | --- | --- |
| The tests, the grader, the tools | this folder | Yes |
| Your attempt history | `records.json` | Yes - hash-chained, append-only |
| The signed seal | `SEAL.json` | Yes - Ed25519 signed |
| The file manifest | `suite.manifest.json` | Yes |
| The professor agent's public key | `agent.pub` | Yes |
| **The professor agent's private key** | `%USERPROFILE%\.professor\professor_key.pem` | **No** - it must never enter the repository. Back it up somewhere safe (a password manager); with it you can keep signing, without it you can still verify every seal already made. |
| **Your model API key** | the `PROFESSOR_API_KEY` environment variable | **No** - `.env` and `*.pem` are git-ignored |
| Your answers | the `T**` notebooks | Yes - commit them as you go |
| Your report | `GRADE_REPORT.md` | Yes - a regenerated snapshot of the ledger |
| The environment | `requirements.txt` | Yes - pinned versions |

### The loop per section

```bash
# 1. work in the test notebook and save it
# 2. grade and log the attempt
python 20-Testing-Syllabus/grade_records.py run "T03 - Methods and Functions Test.ipynb" --prose 7
# 3. re-seal so the signature covers the new chain head
python 20-Testing-Syllabus/integrity.py seal
# 4. commit and push
git add -A && git commit -m "T03: 19/20, signed off" && git push
# 5. mark the milestone with a signed tag (GitHub shows "Verified")
git tag -s v1.0-T03-pass -m "T03 signed off: 19/20"
git push origin v1.0-T03-pass
```

The signed tag is the git-native half of the guarantee: it says *this exact
state was signed off*, and the seal says *these are the grades that led to
it*. GitHub stores both, and its transparency log stores the attestation.

**Two independent layers.** Git history is the record of your *work*; the hash
chain and the seal are the record of your *grades*. Each attempt stores the
git blob id of the notebook as graded, so if you later edit your answer cells,
`integrity.py verify` reports the drift and `git log` shows the change.

## How projects are graded

Projects are not auto-graded - a rubric is. `rubrics.json` holds one rubric
used for **every** project in the course, so the marks are comparable:

| Criterion | Weight | What it asks |
| --- | --- | --- |
| Functionality | 3 | Does it do what the brief asks? |
| Robustness | 2 | Does it handle bad input and edge cases? |
| Tests | 2 | Is there a suite, does it pass, does it cover the core? |
| Code quality and structure | 2 | Clear names, sensible split, no dead code? |
| Documentation | 2 | README that says what it is and how to run it? |
| Use of the section's skills | 1 | Does it use what the section taught? |

Each criterion is scored 0-4 (0 not attempted, 1 partial, 2 basic, 3 solid,
4 excellent). The weighted score is `sum(score x weight) / (4 x total weight)`.

```bash
python 20-Testing-Syllabus/grade_records.py rubric P05          # read the rubric
python 20-Testing-Syllabus/grade_records.py rubric all          # list every project
python 20-Testing-Syllabus/grade_records.py record-project P05 --scores 3,4,2,3,4,3
python 20-Testing-Syllabus/grade_records.py record-project P-PRACTICE --scores 3,3,2,3,4,2 --repo ../my-project
```

The score is appended to the hash chain with the rubric breakdown and the
project repository's commit, so a project mark cannot be quietly changed
either. Project marks are reported separately from the course mark.

## The progress log and the AI reviews

```bash
# a dated note in the chained journal
python 20-Testing-Syllabus/grade_records.py log "rebuilt the OOP model, still stuck on super()"

# the professor reviews a project against its rubric and writes a report
python 20-Testing-Syllabus/professor.py review --project P05 --path ../my-project

# the professor analyses your whole record: where you are, what to work on next
python 20-Testing-Syllabus/professor.py progress
```

Both write to `reviews/` and both add a journal entry, so the written advice
is part of the recorded history. `S2 - Grading Records.ipynb` renders the
project table, the weakest-criterion analysis and the journal.

## Naming scheme

Every artifact has one prefix, and each prefix means one thing:

| Prefix | Means | Examples |
| --- | --- | --- |
| `T00` - `T19` | A graded test for that course section | `T05 - Object Oriented Programming Test.ipynb` |
| `FINAL` | The cumulative exam | `FINAL - Final Comprehensive Exam.ipynb` |
| `P00` - `P19` | The portfolio project for that course section (a rubric id, not a file) | `record-project P05` |
| `P-PRACTICE` | The practice project (a rubric id, not a file) | `record-project P-PRACTICE` |
| `S0` - `S5` | The suite's own documentation | `S0 - Testing Syllabus.ipynb` |
| `PRACTICE` | A drill that is never graded for the mark | `PRACTICE - Practice Test.ipynb` |
| `00-` - `19-` | The original course folders at the repository root | `05-Object Oriented Programming/` |

The numbers always mean the same thing: the prefix number is the course
section it belongs to. `T05`, `P05` and section `05` are the same topic in
three different roles - the test, the project, and the lectures.

The final exam used to be `99` and the system docs used to be `00`-`05`,
which made them look like course sections. They are now `FINAL` and `S0`-`S5`.

## Requirements

- Python 3.8 or newer for the grader (standard library only).
- Jupyter or JupyterLab to work through the notebooks.
- `cryptography` for the integrity tooling (Ed25519 signing). It ships with
  Anaconda; `pip install cryptography` otherwise. Everything else - the
  grader, the ledger, the builder - is standard library only.
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
