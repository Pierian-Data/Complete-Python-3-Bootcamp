"""Grading records - a tamper-evident ledger for the test suite.

Keeps every attempt at every test, computes your weighted course mark from the
blueprint in "00 - Testing Syllabus.ipynb", and exports a markdown report you
can paste into a portfolio.

Every entry is appended to a hash chain (see integrity.py): each entry carries
the hash of its predecessor and of its own content, plus the SHA-256 and git
blob id of the notebook that was graded. Editing or deleting a past entry
breaks the chain and `integrity.py verify` reports exactly where.

Commands
--------
    record   record an attempt by hand
    run      grade a notebook with grade.py and record the result
    list     show every attempt
    summary  per-test best scores, weighted course mark, band, next target
    report   write a markdown report (default: GRADE_REPORT.md)
    reset    void the attempts for one test (the history stays, marked void)

Examples
--------
    python grade_records.py run "T03 - Methods and Functions Test.ipynb" --prose 7
    python grade_records.py record T00 --checks 5/6 --prose 6 --notes "slicing still slips"
    python grade_records.py summary
    python grade_records.py report
"""

import argparse
import datetime
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import integrity

RECORDS_PATH = integrity.LEDGER

PASS_MARK = 14          # out of 20, per module test
FINAL_PASS = 42         # out of 60, final exam
SECTION_SHARE = 0.85    # section tests -> 85% of the course mark
FINAL_SHARE = 0.15      # final exam   -> 15% of the course mark

# id, title, file name, weight (% of the 400 section points), expected checks
SECTION_SPECS = [
    ("T00", "Objects and Data Structures", "T00 - Objects and Data Structures Test.ipynb", 12, 6),
    ("T01", "Comparison Operators", "T01 - Comparison Operators Test.ipynb", 3, 6),
    ("T02", "Python Statements", "T02 - Python Statements Test.ipynb", 9, 6),
    ("T03", "Methods and Functions", "T03 - Methods and Functions Test.ipynb", 9, 6),
    ("T04", "Milestone Project 1", "T04 - Milestone Project 1 Test.ipynb", 4, 4),
    ("T05", "Object Oriented Programming", "T05 - Object Oriented Programming Test.ipynb", 7, 6),
    ("T06", "Modules and Packages", "T06 - Modules and Packages Test.ipynb", 3, 6),
    ("T07", "Errors and Exception Handling", "T07 - Errors and Exception Handling Test.ipynb", 5, 6),
    ("T08", "Milestone Project 2", "T08 - Milestone Project 2 Test.ipynb", 3, 2),
    ("T09", "Built-in Functions", "T09 - Built-in Functions Test.ipynb", 5, 6),
    ("T10", "Decorators", "T10 - Decorators Test.ipynb", 4, 6),
    ("T11", "Generators", "T11 - Generators Test.ipynb", 4, 6),
    ("T12", "Advanced Python Modules", "T12 - Advanced Python Modules Test.ipynb", 7, 6),
    ("T13", "Web Scraping", "T13 - Web Scraping Test.ipynb", 4, 6),
    ("T14", "Working with Images", "T14 - Working with Images Test.ipynb", 3, 6),
    ("T15", "PDFs and Spreadsheets", "T15 - PDFs and Spreadsheets Test.ipynb", 3, 6),
    ("T16", "Emailing with Python", "T16 - Emailing with Python Test.ipynb", 2, 6),
    ("T17", "Advanced Python Objects", "T17 - Advanced Python Objects Test.ipynb", 8, 6),
    ("T18", "Milestone Project 3 (Capstone)", "T18 - Milestone Project 3 Test.ipynb", 3, 2),
    ("T19", "GUI Bonus Material", "T19 - GUI Bonus Material Test.ipynb", 2, 4),
]

FINAL_SPEC = ("FINAL", "Final Comprehensive Exam", "FINAL - Final Comprehensive Exam.ipynb", 6, 5)


def _count_checks(path):
    """Number of cells tagged 'check' in a notebook, or None if unreadable."""
    try:
        with open(path, encoding="utf-8") as handle:
            document = json.load(handle)
    except (OSError, ValueError):
        return None
    return sum(
        1
        for cell in document.get("cells", [])
        if "check" in cell.get("metadata", {}).get("tags", [])
    )


def load_tests():
    """Test catalogue. Check counts come from the notebooks when they exist."""
    tests = []
    for tid, title, filename, weight, expected_checks in SECTION_SPECS:
        checks = _count_checks(os.path.join(HERE, filename))
        if checks is None:
            checks = expected_checks
        tests.append(
            {
                "id": tid,
                "title": title,
                "file": filename,
                "weight": weight,
                "points_possible": 20,
                "checks": checks,
                "points_per_check": 2,
            }
        )
    tid, title, filename, expected_checks, points_per_check = FINAL_SPEC
    checks = _count_checks(os.path.join(HERE, filename))
    if checks is None:
        checks = expected_checks
    final = {
        "id": tid,
        "title": title,
        "file": filename,
        "weight": 0,
        "points_possible": 60,
        "checks": checks,
        "points_per_check": points_per_check,
    }
    return tests, final


def prose_max(test):
    """Points available for the hand-marked (prose) questions."""
    return test["points_possible"] - test["checks"] * test["points_per_check"]


def load_records():
    return integrity.load_ledger()


def save_records(data):
    integrity.save_ledger(data)


def find_test(identifier, tests, final):
    """Resolve a test id, file name or bare file name to a test record."""
    for test in list(tests) + [final]:
        if identifier.lower() in (test["id"].lower(), test["file"].lower()):
            return test
    for test in list(tests) + [final]:
        if os.path.basename(test["file"]).lower() == os.path.basename(identifier).lower():
            return test
    for test in list(tests) + [final]:
        if test["title"].lower() == identifier.lower():
            return test
    return None


def record_attempt(test, checks_passed, prose_points, notes="", date=None,
                   notebook=None, failures=None):
    """Append an attempt to the hash-chained ledger and return the entry."""
    payload = {
        "event": "attempt",
        "date": date or datetime.date.today().isoformat(),
        "test": test["id"],
        "title": test["title"],
        "checks_passed": checks_passed,
        "checks_total": test["checks"],
        "coding_points": checks_passed * test["points_per_check"],
        "prose_points": prose_points,
        "points": checks_passed * test["points_per_check"] + prose_points,
        "points_possible": test["points_possible"],
        "notes": notes,
    }
    # A redo never overwrites: it is a new entry that names the attempt it
    # supersedes, so the full history stays legible in the chain.
    previous = [
        entry for entry in attempt_entries()
        if entry.get("test") == test["id"]
    ]
    payload["attempt_number"] = len(previous) + 1
    if previous:
        payload["supersedes"] = previous[-1]["seq"]
    if notebook:
        path = notebook if os.path.isabs(notebook) else os.path.join(HERE, notebook)
        if os.path.exists(path):
            payload["notebook"] = os.path.basename(path)
            payload["notebook_sha256"] = integrity.sha256_file(path)
            blob = integrity.git_blob(path)
            if blob:
                payload["notebook_git_blob"] = blob
    if failures:
        payload["grader_failures"] = list(failures)
    return integrity.append_entry(payload)


def attempt_entries(data=None):
    """Attempt entries that have not been voided by a reset."""
    data = load_records() if data is None else data
    voided = integrity.voided_tests(data)
    return [
        entry for entry in integrity.chain_entries(data)
        if entry.get("event") == "attempt" and entry.get("test") not in voided
    ]


def best_scores(records, tests, final):
    """Best points achieved per test id."""
    best = {}
    for attempt in attempt_entries(records):
        tid = attempt["test"]
        if attempt["points"] > best.get(tid, -1):
            best[tid] = attempt["points"]
    return best


def summarize(records=None, tests=None, final=None):
    """Everything the summary and report need, computed once."""
    records = load_records() if records is None else records
    if tests is None:
        tests, final = load_tests()
    best = best_scores(records, tests, final)

    rows = []
    weighted_points = 0.0
    for test in tests:
        points = best.get(test["id"])
        rows.append({"test": test, "best": points})
        if points is not None:
            weighted_points += points * test["weight"]

    section_max = sum(t["points_possible"] * t["weight"] for t in tests)
    section_mark = weighted_points / section_max if section_max else 0.0
    final_points = best.get(final["id"])
    final_mark = (final_points / final["points_possible"]) if final_points else 0.0
    course_mark = SECTION_SHARE * section_mark + FINAL_SHARE * final_mark

    if course_mark >= 85:
        band = "Distinction"
    elif course_mark >= 70:
        band = "Merit"
    elif course_mark >= 55:
        band = "Pass"
    else:
        band = "Below pass"

    signed_off = [r["test"]["id"] for r in rows if r["best"] is not None and r["best"] >= PASS_MARK]
    pending = [r["test"]["id"] for r in rows if r["best"] is None or r["best"] < PASS_MARK]
    next_target = pending[0] if pending else None

    projects = best_projects(records)
    journal = journal_entries(records)
    averages = criterion_averages(records)
    portfolio_scores = [entry["percent"] for entry in projects.values()]
    portfolio_mark = round(sum(portfolio_scores) / len(portfolio_scores), 1) if portfolio_scores else None
    names = criterion_names()
    weakest = sorted(
        ({"criterion": key, "name": names.get(key, key.replace("_", " ").capitalize()),
          "average": round(value[0], 2), "projects": value[1]}
         for key, value in averages.items()),
        key=lambda item: item["average"],
    )

    return {
        "rows": rows,
        "best": best,
        "weighted_points": weighted_points,
        "section_max": section_max,
        "section_mark": section_mark,
        "final_points": final_points,
        "final_mark": final_mark,
        "course_mark": course_mark,
        "band": band,
        "signed_off": signed_off,
        "pending": pending,
        "next_target": next_target,
        "attempts": attempt_entries(records),
        "history": integrity.chain_entries(records),
        "projects": projects,
        "project_entries": project_entries(records),
        "journal": journal,
        "portfolio_mark": portfolio_mark,
        "criterion_averages": averages,
        "weakest_criteria": weakest,
    }


def format_bar(points, points_possible, width=20):
    if points is None:
        return "[" + " " * width + "]"
    filled = int(round(width * points / points_possible))
    return "[" + "#" * filled + "." * (width - filled) + "]"


def summary_text(summary):
    lines = []
    lines.append("=" * 78)
    lines.append("GRADING RECORDS - Complete Python 3 Bootcamp")
    lines.append("=" * 78)
    for row in summary["rows"]:
        test = row["test"]
        best = row["best"]
        mark = ("%2d/%d" % (best, test["points_possible"])) if best is not None else "  -/%d" % test["points_possible"]
        status = "signed off" if best is not None and best >= PASS_MARK else (
            "attempted" if best is not None else "not attempted")
        lines.append("%-4s %-34s %-7s %4d%%  %s  %s" % (
            test["id"], test["title"][:34], mark, test["weight"], format_bar(best, test["points_possible"]), status))
    lines.append("-" * 78)
    lines.append("Section mark   : %5.1f / 100  (85%% of the course mark)" % (summary["section_mark"] * 100))
    if summary["final_points"] is None:
        lines.append("Final exam     : not attempted (15% of the course mark)")
    else:
        lines.append("Final exam     : %5.1f / 100  (pass %d/%d)" % (
            summary["final_mark"] * 100, FINAL_PASS, 60))
    lines.append("Course mark    : %5.1f / 100  ->  %s" % (summary["course_mark"] * 100, summary["band"]))
    lines.append("Signed off     : %d / %d modules (pass mark %d/%d)" % (
        len(summary["signed_off"]), len(summary["rows"]), PASS_MARK, 20))
    if summary["next_target"]:
        lines.append("Next target    : %s" % summary["next_target"])
    lines.append("Attempts logged: %d" % len(summary["attempts"]))
    if summary["projects"]:
        lines.append("Projects graded: %d (portfolio average %s%%)" % (
            len(summary["projects"]), summary["portfolio_mark"]))
        weakest = summary["weakest_criteria"][:2]
        if weakest:
            lines.append("Weakest areas  : %s" % ", ".join(
                "%s (%.1f/4)" % (item["name"], item["average"]) for item in weakest))
    else:
        lines.append("Projects graded: 0")
    lines.append("Journal entries: %d" % len(summary["journal"]))
    lines.append("Ledger chain   : %d entries, head %s" % (
        len(summary["history"]), summary["history"][-1]["hash"][:16] if summary["history"] else "-"))
    return "\n".join(lines)


def report_markdown(summary):
    lines = []
    lines.append("# Grading Record - Complete Python 3 Bootcamp")
    lines.append("")
    lines.append("Generated %s by `grade_records.py report`." % datetime.date.today().isoformat())
    lines.append("")
    lines.append("**Course mark: %.1f / 100 (%s)** - section mark %.1f / 100, final exam %s." % (
        summary["course_mark"] * 100,
        summary["band"],
        summary["section_mark"] * 100,
        ("%.1f / 100" % (summary["final_mark"] * 100)) if summary["final_points"] is not None else "not attempted",
    ))
    lines.append("")
    lines.append("## Module tests")
    lines.append("")
    lines.append("| Test | Module | Best | Weight | Result |")
    lines.append("| --- | --- | --- | --- | --- |")
    for row in summary["rows"]:
        test = row["test"]
        best = row["best"]
        mark = "%d / %d" % (best, test["points_possible"]) if best is not None else "- / %d" % test["points_possible"]
        result = "signed off" if best is not None and best >= PASS_MARK else (
            "attempted" if best is not None else "not attempted")
        lines.append("| %s | %s | %s | %d%% | %s |" % (test["id"], test["title"], mark, test["weight"], result))
    lines.append("")
    lines.append("## Attempt history")
    lines.append("")
    lines.append("Retakes are expected and are never deleted. Each attempt is an entry in the hash")
    lines.append("chain; a redo names the attempt it supersedes, and the best attempt per module")
    lines.append("is the one that counts.")
    lines.append("")
    if summary["attempts"]:
        best = summary["best"]
        lines.append("| Date | Test | Attempt | Coding | Prose | Total | Status | Supersedes | Ledger hash | Notes |")
        lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
        for attempt in summary["attempts"]:
            status = "current best" if best.get(attempt["test"]) == attempt["points"] else "superseded"
            lines.append("| %s | %s | %d | %d | %d | %d / %d | %s | %s | `%s` | %s |" % (
                attempt["date"], attempt["test"], attempt.get("attempt_number", 1),
                attempt["coding_points"], attempt["prose_points"],
                attempt["points"], attempt["points_possible"], status,
                ("#%d" % attempt["supersedes"]) if attempt.get("supersedes") else "-",
                attempt["hash"][:12], attempt["notes"].replace("|", "/") or "-"))
    else:
        lines.append("No attempts recorded yet.")
    lines.append("")
    lines.append("## Sign-off checklist")
    lines.append("")
    for row in summary["rows"]:
        test = row["test"]
        best = row["best"]
        done = best is not None and best >= PASS_MARK
        lines.append("- [%s] %s %s (%d%% weight)" % ("x" if done else " ", test["id"], test["title"], test["weight"]))
    lines.append("")

    lines.append("## Project work")
    lines.append("")
    if summary["projects"]:
        lines.append("| Project | Title | Mark | Level | Rubric scores | Date |")
        lines.append("| --- | --- | --- | --- | --- | --- |")
        for project_id, entry in sorted(summary["projects"].items()):
            scores = ", ".join("%s %d/%d" % (item["name"], item["score"], item["max"])
                               for item in entry.get("scores", []))
            lines.append("| %s | %s | %s | %s | %s | %s |" % (
                project_id, entry["title"], "%s%%" % entry["percent"], entry["level"],
                scores, entry.get("date", "-")))
        lines.append("")
        if summary["portfolio_mark"] is not None:
            lines.append("**Portfolio average: %s%%** across %d graded project(s). Project marks are "
                         "reported separately from the course mark and use the same rubric for every "
                         "project, so they are comparable." % (
                             summary["portfolio_mark"], len(summary["projects"])))
        lines.append("")
        if summary["weakest_criteria"]:
            lines.append("### Where the work is weakest")
            lines.append("")
            lines.append("| Criterion | Average score (0-4) | Projects |")
            lines.append("| --- | --- | --- |")
            for item in summary["weakest_criteria"]:
                lines.append("| %s | %.2f | %d |" % (
                    item["name"], item["average"], item["projects"]))
            lines.append("")
            lines.append("The lowest average is where a reviewer would look first - that is the "
                         "criterion to work on next.")
            lines.append("")
    else:
        lines.append("No projects graded yet. Score one with:")
        lines.append("")
        lines.append("```")
        lines.append("python 20-Testing-Syllabus/grade_records.py record-project P05 --scores 3,4,2,3,4,3")
        lines.append("```")
        lines.append("")

    lines.append("## Progress journal")
    lines.append("")
    if summary["journal"]:
        lines.append("| When | Note |")
        lines.append("| --- | --- |")
        for entry in summary["journal"]:
            lines.append("| %s | %s |" % (entry.get("date", "-"), entry.get("text", "").replace("|", "/")))
    else:
        lines.append("No journal entries yet. Add one with:")
        lines.append("")
        lines.append("```")
        lines.append('python 20-Testing-Syllabus/grade_records.py log "rebuilt the OOP model, still stuck on super()"')
        lines.append("```")
    lines.append("")

    lines.append("## Tamper evidence")
    lines.append("")
    history = summary["history"]
    if history:
        lines.append("Every row above is an entry in a hash chain: each entry carries the hash of its")
        lines.append("predecessor and of its own content, plus the SHA-256 of the notebook that was graded.")
        lines.append("")
        lines.append("| Seq | Date | Event | Test | Points | Chain hash |")
        lines.append("| --- | --- | --- | --- | --- | --- |")
        for entry in history:
            if entry.get("event") == "attempt":
                detail = "%d / %d" % (entry["points"], entry["points_possible"])
                subject = entry.get("test", "-")
            elif entry.get("event") == "project":
                detail = "%s%% (%s)" % (entry.get("percent"), entry.get("level"))
                subject = entry.get("project", "-")
            elif entry.get("event") == "journal":
                detail = entry.get("text", "")[:60]
                subject = entry.get("tag", "-")
            else:
                detail = "voided"
                subject = entry.get("test", "-")
            lines.append("| %d | %s | %s | %s | %s | `%s` |" % (
                entry["seq"], entry.get("date", "-"), entry.get("event", "attempt"),
                subject, detail, entry["hash"][:12]))
        lines.append("")
        lines.append("Verify it yourself: `python 20-Testing-Syllabus/integrity.py verify`")
    else:
        lines.append("No ledger entries yet.")
    lines.append("")
    return "\n".join(lines)


def parse_checks(text):
    """Parse '5/6' into (5, 6)."""
    parts = str(text).split("/")
    if len(parts) != 2:
        raise argparse.ArgumentTypeError("checks must look like 5/6")
    try:
        return int(parts[0]), int(parts[1])
    except ValueError:
        raise argparse.ArgumentTypeError("checks must look like 5/6")


# --------------------------------------------------------------------------
# projects: rubric scoring and the progress journal
# --------------------------------------------------------------------------

RUBRICS = os.path.join(HERE, "rubrics.json")
LEVELS = [
    (90, "excellent"),
    (75, "strong"),
    (60, "pass"),
    (40, "developing"),
    (0, "weak"),
]


def load_rubrics():
    with open(RUBRICS, encoding="utf-8") as handle:
        return json.load(handle)


def rubric_criteria(project_id):
    """The six criteria for a project, common ones first."""
    rubrics = load_rubrics()
    project = rubrics["projects"].get(project_id)
    if project is None:
        return None, None
    criteria = list(rubrics["common_criteria"]) + [project["skill_criterion"]]
    return project, criteria


def level_for(percent):
    for threshold, name in LEVELS:
        if percent >= threshold:
            return name
    return "weak"


def score_project(project_id, scores, notes="", repo=None):
    """Score a project against the rubric and append it to the chain."""
    project, criteria = rubric_criteria(project_id)
    if project is None:
        return None
    if len(scores) != len(criteria):
        raise ValueError("%s has %d criteria, %d scores given" % (project_id, len(criteria), len(scores)))
    for score in scores:
        if not 0 <= score <= 4:
            raise ValueError("scores must be between 0 and 4")
    weighted = sum(score * criterion["weight"] for score, criterion in zip(scores, criteria))
    maximum = 4 * sum(criterion["weight"] for criterion in criteria)
    percent = round(100.0 * weighted / maximum, 1)
    breakdown = [
        {"criterion": criterion["id"], "name": criterion["name"], "score": score,
         "weight": criterion["weight"], "max": criterion["weight"] * 4}
        for score, criterion in zip(scores, criteria)
    ]
    payload = {
        "event": "project",
        "date": datetime.date.today().isoformat(),
        "project": project_id,
        "title": project["title"],
        "scores": breakdown,
        "weighted": weighted,
        "maximum": maximum,
        "percent": percent,
        "level": level_for(percent),
        "notes": notes,
    }
    if repo:
        payload["repo"] = repo
        try:
            result = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True)
            commit = result.stdout.strip()
            if commit:
                payload["commit"] = commit
        except OSError:
            pass
    return integrity.append_entry(payload)


def project_entries(data=None):
    data = load_records() if data is None else data
    return [entry for entry in integrity.chain_entries(data) if entry.get("event") == "project"]


def journal_entries(data=None):
    data = load_records() if data is None else data
    return [entry for entry in integrity.chain_entries(data) if entry.get("event") == "journal"]


def best_projects(data=None):
    """Best percentage per project id."""
    best = {}
    for entry in project_entries(data):
        current = best.get(entry["project"])
        if current is None or entry["percent"] > current["percent"]:
            best[entry["project"]] = entry
    return best


def criterion_names():
    """Display names for the rubric criteria, keyed by id."""
    names = {}
    try:
        rubrics = load_rubrics()
    except OSError:
        return names
    for criterion in rubrics["common_criteria"]:
        names[criterion["id"]] = criterion["name"]
    for project in rubrics["projects"].values():
        criterion = project["skill_criterion"]
        names.setdefault(criterion["id"], criterion["name"])
    return names


def criterion_averages(data=None):
    """Average score per rubric criterion across every graded project."""
    totals = {}
    counts = {}
    for entry in project_entries(data):
        for item in entry.get("scores", []):
            key = item["criterion"]
            totals[key] = totals.get(key, 0) + item["score"]
            counts[key] = counts.get(key, 0) + 1
    return {key: (totals[key] / counts[key], counts[key]) for key in totals}


def append_journal(text, tag=None, extra=None):
    """Append a dated progress note to the chain."""
    payload = {
        "event": "journal",
        "date": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
        "text": text,
    }
    if tag:
        payload["tag"] = tag
    if extra:
        payload.update(extra)
    return integrity.append_entry(payload)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    p_record = sub.add_parser("record", help="record an attempt by hand")
    p_record.add_argument("test", help="test id (T03) or file name")
    p_record.add_argument("--checks", required=True, type=parse_checks, help="checks passed, e.g. 5/6")
    p_record.add_argument("--prose", type=int, default=None, help="points for the hand-marked questions")
    p_record.add_argument("--notes", default="")
    p_record.add_argument("--date", default=None)

    p_run = sub.add_parser("run", help="grade a notebook and record the result")
    p_run.add_argument("test", help="test id (T03) or file name")
    p_run.add_argument("--prose", type=int, default=None, help="points for the hand-marked questions")
    p_run.add_argument("--notes", default="")
    p_run.add_argument("--date", default=None)
    p_run.add_argument("--seal", action="store_true", help="re-seal after recording (agent key required)")

    sub.add_parser("list", help="show every attempt")
    sub.add_parser("summary", help="per-test best scores and the course mark")

    p_report = sub.add_parser("report", help="write a markdown report")
    p_report.add_argument("--out", default=os.path.join(HERE, "GRADE_REPORT.md"))

    p_reset = sub.add_parser("reset", help="void the attempts for one test (history is kept)")
    p_reset.add_argument("test")
    p_reset.add_argument("--all", action="store_true", help="void every attempt")

    p_rubric = sub.add_parser("rubric", help="show the rubric for a project")
    p_rubric.add_argument("project", help="project id (P05, P-PRACTICE) or 'all'")

    p_project = sub.add_parser("record-project", help="score a project against the rubric")
    p_project.add_argument("project", help="project id (P05, P-PRACTICE)")
    p_project.add_argument("--scores", required=True,
                           help="one score per criterion, 0-4, comma separated, e.g. 3,4,2,3,4,3")
    p_project.add_argument("--notes", default="")
    p_project.add_argument("--repo", default=None, help="path to the project repository")

    p_log = sub.add_parser("log", help="add a dated progress note to the journal")
    p_log.add_argument("text")
    p_log.add_argument("--tag", default=None)

    args = parser.parse_args(argv)
    tests, final = load_tests()

    if args.command == "record":
        test = find_test(args.test, tests, final)
        if test is None:
            print("unknown test: %s" % args.test)
            return 1
        passed, total = args.checks
        if total != test["checks"]:
            print("note: the notebook has %d check cells, you entered %d" % (test["checks"], total))
        prose = args.prose if args.prose is not None else 0
        if not 0 <= prose <= prose_max(test):
            print("prose points must be between 0 and %d for %s" % (prose_max(test), test["id"]))
            return 1
        entry = record_attempt(test, min(passed, total), prose, args.notes, args.date,
                               notebook=test["file"])
        print("recorded %s: %d/%d (%d/%d points) chain hash %s" % (
            test["id"], entry["checks_passed"], entry["checks_total"],
            entry["points"], entry["points_possible"], entry["hash"][:12]))
        return 0

    if args.command == "run":
        test = find_test(args.test, tests, final)
        if test is None:
            print("unknown test: %s" % args.test)
            return 1
        path = os.path.join(HERE, test["file"])
        sys.path.insert(0, HERE)
        import grade

        passed, failed, failures, problems = grade.grade(path, solutions=False)
        for label, error in failures:
            print("FAIL %s: %s" % (label, error))
        for problem in problems:
            print("PROBLEM %s" % problem)
        prose = args.prose
        if prose is None:
            limit = prose_max(test)
            prose = int(input("points for the hand-marked questions (0-%d)? " % limit) or 0)
        entry = record_attempt(test, passed, prose, args.notes, args.date,
                               notebook=test["file"],
                               failures=["%s: %s" % (label, error) for label, error in failures])
        print("recorded %s: checks %d/%d, total %d/%d, chain hash %s" % (
            test["id"], passed, passed + failed, entry["points"], entry["points_possible"],
            entry["hash"][:12]))
        if args.seal:
            integrity.build_manifest()
            integrity.seal()
        return 0

    if args.command == "list":
        records = load_records()
        history = integrity.chain_entries(records)
        if not history:
            print("no attempts recorded yet.")
            return 0
        best = best_scores(records, tests, final)
        projects = best_projects(records)
        for entry in history:
            event = entry.get("event", "attempt")
            if event == "reset":
                print("%s  %-8s  VOIDED by reset - the history above is kept" % (
                    entry.get("date", "-"), entry.get("test", "-")))
                continue
            if event == "project":
                status = "best" if projects.get(entry["project"], {}).get("hash") == entry["hash"] else "superseded"
                print("%s  %-8s  project %5.1f%% (%s)  %-10s %s  %s" % (
                    entry.get("date", "-"), entry["project"], entry["percent"], entry["level"],
                    status, entry["hash"][:12], entry.get("notes", "")))
                continue
            if event == "journal":
                print("%s  %-8s  journal: %s" % (
                    entry.get("date", "-"), entry.get("tag", "-"), entry.get("text", "")))
                continue
            status = "best" if best.get(entry["test"]) == entry["points"] else "superseded"
            print("%s  %-4s  attempt %d%s  %2d/%2d checks  %2d/%2d points  %-10s %s  %s" % (
                entry.get("date", "-"), entry["test"], entry.get("attempt_number", 1),
                (" (supersedes #%d)" % entry["supersedes"]) if entry.get("supersedes") else "",
                entry["checks_passed"], entry["checks_total"],
                entry["points"], entry["points_possible"], status, entry["hash"][:12],
                entry.get("notes", "")))
        return 0

    if args.command == "summary":
        print(summary_text(summarize()))
        return 0

    if args.command == "report":
        summary = summarize()
        with open(args.out, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(report_markdown(summary))
        print("wrote %s" % args.out)
        return 0

    if args.command == "rubric":
        rubrics = load_rubrics()
        if args.project.lower() == "all":
            for project_id, project in sorted(rubrics["projects"].items()):
                print("%-8s %s" % (project_id, project["title"]))
            print("\nShow one with: grade_records.py rubric P05")
            return 0
        project, criteria = rubric_criteria(args.project)
        if project is None:
            print("unknown project: %s" % args.project)
            return 1
        print("RUBRIC - %s (%s)" % (project["title"], args.project))
        print("=" * 70)
        print(project["pitch"])
        print()
        for index, criterion in enumerate(criteria, start=1):
            print("%d. %s  (weight %d, scored 0-4)" % (index, criterion["name"], criterion["weight"]))
            print("   %s" % criterion["prompt"])
        print()
        print("Deliverables:")
        for item in project["deliverables"]:
            print("  - %s" % item)
        print()
        print("Scale: " + ", ".join("%s = %s" % (key, value) for key, value in rubrics["scale"].items()))
        print()
        print("Record it with:")
        print("  grade_records.py record-project %s --scores 3,4,2,3,4,3" % args.project)
        return 0

    if args.command == "record-project":
        try:
            scores = [int(part) for part in args.scores.replace(" ", "").split(",") if part]
        except ValueError:
            print("--scores must be comma separated integers, e.g. 3,4,2,3,4,3")
            return 1
        try:
            entry = score_project(args.project, scores, args.notes, args.repo)
        except ValueError as error:
            print(error)
            return 1
        if entry is None:
            print("unknown project: %s (try: grade_records.py rubric all)" % args.project)
            return 1
        print("recorded %s: %s%% (%s), weighted %d/%d, chain hash %s" % (
            args.project, entry["percent"], entry["level"], entry["weighted"], entry["maximum"],
            entry["hash"][:12]))
        return 0

    if args.command == "log":
        entry = append_journal(args.text, args.tag)
        print("journal entry %d recorded, chain hash %s" % (entry["seq"], entry["hash"][:12]))
        return 0

    if args.command == "reset":
        if args.all:
            integrity.append_entry({
                "event": "reset",
                "date": datetime.date.today().isoformat(),
                "test": "*",
                "notes": "every attempt voided",
            })
            print("voided every attempt (history kept in the chain)")
            return 0
        test = find_test(args.test, tests, final)
        if test is None:
            print("unknown test: %s" % args.test)
            return 1
        integrity.append_entry({
            "event": "reset",
            "date": datetime.date.today().isoformat(),
            "test": test["id"],
            "notes": "attempts voided",
        })
        print("voided the attempts for %s (history kept in the chain)" % test["id"])
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
