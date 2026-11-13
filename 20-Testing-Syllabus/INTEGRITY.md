# INTEGRITY.md - tamper evidence for your grades, your work, and the tests

What this guarantees, what it cannot guarantee, and how to check it yourself.

---

## 1. The honest threat model

You own this fork. You can rewrite your own git history, delete files, and
change anything in your own repository. **No scheme stored only in a repo you
control can prove anything against you.** What it can do:

| Threat | Covered? | How |
| --- | --- | --- |
| An AI agent quietly inflating a grade | **Yes** | Grades live in a hash chain; the agent cannot change one without breaking it, and the chain head is signed and externally anchored |
| A check cell being weakened so a failing test passes | **Yes** | `suite.manifest.json` hashes every file in this folder; CI fails if a file changed without the manifest being regenerated and reviewed |
| Accidental edit of a past score | **Yes** | The chain reports the exact entry that was edited |
| Your work being changed after it was graded | **Detected** | Each attempt stores the SHA-256 and the git blob id of the notebook as graded; git history shows when and what changed |
| You deliberately rewriting the whole history | **Only with an external anchor** | Anchor the seal hash somewhere you do not control (section 5) |

Read that last row as the boundary: **the seal is only as strong as where you
anchor it.** Inside this repository alone it is a strong audit trail and a
deterrent, not a proof.

---

## 2. The three mechanisms

### 2.1 Hash-chained ledger (`records.json`)

Every entry carries the hash of its predecessor (`prev`) and the hash of its
own content (`hash`). Entry *n* is valid only if it follows entry *n-1* and its
content still hashes to the recorded value.

```
entry 1: prev = 0000...0000            hash = sha256(entry 1 + prev)
entry 2: prev = hash(entry 1)           hash = sha256(entry 2 + prev)
entry 3: prev = hash(entry 2)           hash = sha256(entry 3 + prev)
```

Change one character in entry 1 and every later `prev` no longer matches.

The chain carries four kinds of entry, all equally protected:

| Event | What it records |
| --- | --- |
| `attempt` | A test attempt: checks passed, prose points, total, the attempt number, the attempt it supersedes, and the SHA-256 and git blob id of the notebook that was graded |
| `project` | A rubric score: the per-criterion scores, the weighted mark, the level, and the project repository's commit |
| `journal` | A dated progress note, and the hash of any review file it refers to |
| `reset` | A void event - the attempts it voids stay visible in the history |

### 2.2 Manifest (`suite.manifest.json`)

The suite has two kinds of file, and the manifest treats them differently.

**System files** - the grader, the ledger, the professor CLI, the builder, the
rubrics, the documentation. The manifest stores their full SHA-256. Change one
and `integrity.py verify` fails with exit code 1. This is what stops someone
quietly weakening the grading logic.

**Learner notebooks** - the `T**`, `PRACTICE` and `FINAL` notebooks, where you
write your answers. Those are expected to change, so the manifest stores two
things for them:

- the full SHA-256, reported as an *expected change* when it moves - you are
  meant to edit these;
- a **fingerprint** of the parts that decide what the test checks: every cell
  tagged `check`, every reference solution block, and the header cell. If any
  of those change, the fingerprint stops matching and the verify fails.

So:

| You do | Result |
| --- | --- |
| Write your answer in a code cell and save | Expected change. Still verified. |
| Change a check cell (for example to `assert True`) | **Caught.** "protected content changed" |
| Edit a reference solution | **Caught.** "protected content changed" |
| Edit the grader or the rubric | **Caught.** "modified since the manifest was written" |

The whole file is pinned separately, at the moment it is graded: every attempt
in the ledger stores the SHA-256 and the git blob id of the notebook as it was
graded, so any edit *after* grading shows up as work drift. Between the
fingerprint (before) and the pinned hash (after), there is no window in which
a change goes unnoticed.

Regenerate the manifest deliberately (`integrity.py manifest`) and the change
shows up as a reviewable diff in the commit.

### 2.3 Signed seal (`SEAL.json`)

Binds three things together with one signature:

- the chain head hash,
- the manifest hash,
- the list of attestations.

Signed with an **Ed25519** key. The private key lives **outside** the
repository, in `%USERPROFILE%\.professor\professor_key.pem`; the public key
(`agent.pub`) is committed, so anyone can verify a seal without trusting the
machine that produced it.

---

## 3. Redo policy - retakes are recorded, never erased

Reworking a test or a project because the mark was unsatisfactory is normal
learning, and it is fully documented:

1. **Nothing is deleted.** The ledger is append-only. A redo is a *new entry*
   that names the attempt it supersedes (`supersedes: <seq>`) and its attempt
   number (`attempt_number`).
2. **The best attempt counts.** Your mark is the highest score per module.
   A worse retake cannot lower it.
3. **A reset voids, it does not erase.** `grade_records.py reset T03` appends a
   `reset` event to the chain; the attempts stay visible in the history, marked
   void. Use it when an attempt was graded against a broken test, not to hide a
   bad score.
4. **The story is visible.** `grade_records.py list` shows every attempt with
   `attempt N`, `supersedes #k`, and whether it is the current best or
   superseded. The exported `GRADE_REPORT.md` prints the same history, so a
   reviewer sees the improvement, not just the final number.

```
2026-11-13  T03  attempt 1 (supersedes #3)  4/6 checks  12/20 points  best         a1b2c3d4e5f6
2026-11-20  T03  attempt 2 (supersedes #5)  6/6 checks  19/20 points  best         f6e5d4c3b2a1
```

Both entries stay in the chain. The second names the first. Nothing is hidden.

---

## 4. Commands

```bash
# one-off: create the agent keypair (private key stays outside the repo)
python 20-Testing-Syllabus/integrity.py keygen

# write the manifest (do this after any intentional change to the suite)
python 20-Testing-Syllabus/integrity.py manifest

# seal: sign the chain head + manifest + attestations
python 20-Testing-Syllabus/integrity.py seal

# verify everything
python 20-Testing-Syllabus/integrity.py verify
```

`verify` prints:

```
ledger chain   : OK (12 entries, head 7ca83b6b5f5bcb76)
suite manifest : OK (35 files)
seal           : OK
attestations   : OK (4 signed statements)
work drift     : none
```

Exit code 0 means healthy, 1 means a problem - so CI can use it as a gate.

**Recording an attempt** (the chain entry is written for you):

```bash
python 20-Testing-Syllabus/grade_records.py run "T03 - Methods and Functions Test.ipynb" --prose 7
python 20-Testing-Syllabus/grade_records.py run "T03 - ..." --prose 8 --seal
```

**Recording project work and progress notes** (same chain, same protection):

```bash
python 20-Testing-Syllabus/grade_records.py record-project P05 --scores 3,4,2,3,4,3 --repo ../my-project
python 20-Testing-Syllabus/grade_records.py log "rebuilt the OOP model, still stuck on super()"
```

**An agent attestation** - a signed statement that a specific module was
graded and signed off, produced by the professor agent:

```bash
python 20-Testing-Syllabus/integrity.py attest "T03 signed off: 19/20, all checks passed" \
  --context '{"test":"T03","points":19,"checks":"6/6"}'
```

Attestations are written to `attestations/` and are covered by the next seal.

---

## 5. Anchoring the seal outside this repository

Do this once you care that the record survives a rewrite of your own history.

**Option A - GitHub artifact attestation (keyless, free).**
The workflow `.github/workflows/integrity.yml` attests the commit in GitHub's
transparency log using OIDC, with no keys to manage. Verify from anywhere:

```bash
gh attestation verify <seal-file> --repo vonstegen/Udemy-Complete-Python-3-Bootcamp
```

**Option B - OpenTimestamps (independent service, no account).**

```bash
pip install opentimestamps-client
ots stamp 20-Testing-Syllabus/SEAL.json     # writes SEAL.json.otsr
ots verify 20-Testing-Syllabus/SEAL.json.otsr
```

Commit the `.otsr` file. Anyone can verify the stamp with no key and no
account, and the timestamp comes from independent Bitcoin notarisation.

**Option C - somewhere else entirely.** Mail the seal hash to yourself, post
it in a Discord or Slack channel you do not administer, or drop it in a
repository owned by someone else. The point is only that the copy lives where
you cannot quietly edit it.

---

## 6. Signed commits

The seal covers the *content*; signed commits cover *who made the change*. This
machine already has an SSH key (`~/.ssh/id_ed25519`), which Git can use for
signing:

```bash
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global commit.gpgsign true
```

GitHub then shows a green **Verified** badge on the commit, and
`git log --show-signature` verifies it locally. Add the public key under
*Settings -> SSH and GPG keys* on GitHub if it is not there already.

---

## 7. The git layer

Git is the other half of the guarantee, and it covers a different thing:

| Layer | Covers | Where it lives |
| --- | --- | --- |
| Git history and signed tags | **your work** - every edit to a notebook, and *when* | your fork on GitHub |
| Hash chain and seal | **your grades** - every attempt, and that it was not edited | `records.json`, `SEAL.json` |
| CI | that neither was quietly changed | `.github/workflows/integrity.yml` |
| GitHub transparency log | third-party evidence of the seal | `gh attestation verify` |

The two layers are linked: each attempt in the ledger stores the git blob id
of the notebook as it was graded, so an edit to your answer after grading is
visible both in `integrity.py verify` (work drift) and in `git log`.

Signed tags mark a milestone:

```bash
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global tag.gpgsign true

git tag -s v1.0-T03-pass -m "T03 signed off: 19/20"
git push origin v1.0-T03-pass
```

What is tracked, and what deliberately is not:

| Tracked in git | Deliberately not tracked |
| --- | --- |
| Tests, tools, notebooks | The agent private key (`%USERPROFILE%\.professor\professor_key.pem`) |
| `records.json`, `SEAL.json`, `suite.manifest.json`, `agent.pub` | API keys and `.env` files |
| `GRADE_REPORT.md` (a regenerated snapshot; CI diffs it against a fresh one) | `__pycache__`, `.ipynb_checkpoints` |

Back the private key up outside the repository (a password manager is fine).
Without it you can still verify every seal already made - the public key is
committed - you just cannot sign new ones.

---

## 8. What the CI workflow checks

On every push to the branch, `.github/workflows/integrity.yml`:

1. installs `requirements.txt` and runs `grade.py --solutions` - the tests
   themselves still pass their own reference solutions, so nobody can weaken a
   check without CI noticing;
2. runs `integrity.py verify` - chain, manifest, seal and attestations;
3. regenerates `GRADE_REPORT.md` and fails if it differs from the committed
   one (a hand-edited report is caught here);
4. uploads `GRADE_REPORT.md`, `SEAL.json` and the manifest as artifacts;
5. attests the commit to GitHub's transparency log (keyless, OIDC).

A red build means: a test was changed without regenerating the manifest, a
grade was edited, or the seal no longer matches. Read the diff before you
re-baseline anything - that is the whole point of the exercise.
