"""professor.py - a local AI tutor for this course.

Talks to any OpenAI-compatible chat endpoint (OpenAI, OpenRouter, Together,
Ollama, LM Studio, vLLM) using the professor prompt in PROFESSOR.md, and
grounds every answer in this repository: the course notebooks, the test suite
and the learner's own grading records.

Standard library only.

Usage
-----
    python professor.py ask "why does my list comprehension drop the last item?"
    python professor.py ask --section 02 "explain range again, slower"
    python professor.py ask --check "T02 - Python Statements Test.ipynb" "why did Q7 fail?"
    python professor.py office-hours
    python professor.py check "T02 - Python Statements Test.ipynb"
    python professor.py explain --section 05
    python professor.py --offline ask "what is a decorator"      # show the payload, call nothing

Configuration (environment variables)
-------------------------------------
    PROFESSOR_API_KEY   API key. Falls back to OPENAI_API_KEY.
    PROFESSOR_BASE_URL  Base URL. Default https://api.openai.com/v1
                        For Ollama:  http://localhost:11434/v1
                        For LM Studio: http://localhost:1234/v1
    PROFESSOR_MODEL     Model name. Default gpt-4o-mini
                        For Ollama:  llama3.1
"""

import argparse
import datetime
import json
import os
import re
import sys
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

SECTION_CONTEXT_LIMIT = 24000  # characters of course material per request


# --------------------------------------------------------------------------
# repository context
# --------------------------------------------------------------------------

def read_text(path):
    try:
        with open(path, encoding="utf-8") as handle:
            return handle.read()
    except OSError:
        return ""


def professor_prompt():
    """The operating manual, with an explicit teaching instruction on top."""
    manual = ""
    for candidate in (os.path.join(ROOT, "PROFESSOR.md"), os.path.join(HERE, "PROFESSOR.md")):
        if os.path.exists(candidate):
            manual = read_text(candidate)
            break
    if not manual:
        manual = ("You are the professor for the Complete Python 3 Bootcamp course. "
                  "Teach using the diagnose, explain, practise, verify, record method.")
    return (
        "You are the professor for this course repository. Follow the operating "
        "manual below exactly: it defines your method, the Socratic ladder, the "
        "ground rules and the course map.\n\n"
        + manual
        + "\n\nAlways ground answers in the course material quoted in the context "
          "sections below. If the context does not contain what is needed, say so."
    )


def blueprint_table():
    """The test blueprint table from the syllabus, as plain text."""
    path = os.path.join(HERE, "00 - Testing Syllabus.ipynb")
    try:
        with open(path, encoding="utf-8") as handle:
            document = json.load(handle)
    except (OSError, ValueError):
        return ""
    lines = []
    for cell in document.get("cells", []):
        if cell.get("cell_type") != "markdown":
            continue
        text = "".join(cell.get("source", []))
        if "## 2. Test blueprint" in text:
            lines = [line for line in text.splitlines() if line.strip().startswith("|")]
            break
    return "\n".join(lines)


def section_dirs():
    """Map '02' -> the course folder that starts with '02-'."""
    mapping = {}
    for name in sorted(os.listdir(ROOT)):
        match = re.match(r"^(\d{2})-", name)
        if match and os.path.isdir(os.path.join(ROOT, name)):
            mapping[match.group(1)] = name
    return mapping


def notebook_text(path):
    """Markdown and code cells of a notebook, without outputs."""
    try:
        with open(path, encoding="utf-8") as handle:
            document = json.load(handle)
    except (OSError, ValueError):
        return ""
    parts = []
    for cell in document.get("cells", []):
        source = "".join(cell.get("source", [])).strip()
        if not source:
            continue
        if cell.get("cell_type") == "markdown":
            parts.append(source)
        else:
            parts.append("```python\n%s\n```" % source)
    return "\n\n".join(parts)


def section_context(section):
    """Course material for one section, truncated to a sane size."""
    folders = section_dirs()
    folder = folders.get(section)
    if folder is None:
        return "No course folder found for section %s." % section
    pieces = []
    base = os.path.join(ROOT, folder)
    for name in sorted(os.listdir(base)):
        if not name.endswith(".ipynb"):
            continue
        if name.startswith("09-") or "Solution" in name or "solution" in name:
            continue  # skip the course's own answer keys
        text = notebook_text(os.path.join(base, name))
        if text:
            pieces.append("### %s\n\n%s" % (name, text))
    body = "\n\n".join(pieces)
    if len(body) > SECTION_CONTEXT_LIMIT:
        body = body[:SECTION_CONTEXT_LIMIT] + "\n\n[... truncated ...]"
    return "Course material for section %s (folder %s):\n\n%s" % (section, folder, body)


def record_context():
    """The learner's current mark sheet, so the professor knows where they are."""
    try:
        import grade_records as gr
    except ImportError:
        return ""
    summary = gr.summarize()
    lines = [
        "Learner record (from records.json):",
        "  course mark: %.1f / 100 (%s)" % (summary["course_mark"] * 100, summary["band"]),
        "  modules signed off: %d / %d" % (len(summary["signed_off"]), len(summary["rows"])),
    ]
    for row in summary["rows"]:
        test = row["test"]
        best = row["best"]
        if best is not None:
            lines.append("  %s %s: %d / %d" % (test["id"], test["title"], best, test["points_possible"]))
    if summary["next_target"]:
        lines.append("  next target: %s" % summary["next_target"])
    if summary["attempts"]:
        last = summary["attempts"][-1]
        lines.append("  last attempt: %s on %s (%d/%d) %s" % (
            last["test"], last["date"], last["points"], last["points_possible"], last["notes"]))
    return "\n".join(lines)


def check_context(notebook_name):
    """Grade the learner's saved attempt and report the result."""
    import grade

    path = os.path.join(HERE, notebook_name)
    if not os.path.exists(path):
        path = os.path.abspath(notebook_name)
    if not os.path.exists(path):
        return "Could not find notebook %s." % notebook_name
    passed, failed, failures, problems = grade.grade(path, solutions=False)
    lines = ["Grader result for %s: %d of %d checks passed." % (
        os.path.basename(path), passed, passed + failed)]
    for label, error in failures:
        lines.append("  FAIL %s: %s" % (label, error))
    for problem in problems:
        lines.append("  PROBLEM %s" % problem)
    if not failures and not problems:
        lines.append("  All checks passed.")
    return "\n".join(lines)


def build_context(section=None, notebook=None):
    """Everything the model should see besides the learner's question."""
    blocks = []
    table = blueprint_table()
    if table:
        blocks.append("Test blueprint (section -> weight, points):\n" + table)
    record = record_context()
    if record:
        blocks.append(record)
    if section:
        blocks.append(section_context(section))
    if notebook:
        blocks.append(check_context(notebook))
    return "\n\n".join(blocks)


# --------------------------------------------------------------------------
# model call
# --------------------------------------------------------------------------

def endpoint():
    base = os.environ.get("PROFESSOR_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    return base + "/chat/completions"


def api_key():
    for name in ("PROFESSOR_API_KEY", "OPENAI_API_KEY", "OLLAMA_API_KEY"):
        value = os.environ.get(name)
        if value:
            return value
    return None


def model_name():
    return os.environ.get("PROFESSOR_MODEL", "gpt-4o-mini")


def call_model(messages, stream=True):
    payload = {
        "model": model_name(),
        "messages": messages,
        "stream": bool(stream),
    }
    key = api_key()
    headers = {"Content-Type": "application/json"}
    if key:
        headers["Authorization"] = "Bearer %s" % key
    request = urllib.request.Request(
        endpoint(), data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST"
    )
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            if not stream:
                body = json.loads(response.read().decode("utf-8"))
                return body["choices"][0]["message"]["content"]
            collected = []
            for raw in response:
                line = raw.decode("utf-8").strip()
                if not line.startswith("data:"):
                    continue
                data = line[5:].strip()
                if data == "[DONE]":
                    break
                try:
                    chunk = json.loads(data)
                except ValueError:
                    continue
                choices = chunk.get("choices") or []
                if choices:
                    piece = choices[0].get("delta", {}).get("content")
                    if piece:
                        collected.append(piece)
                        sys.stdout.write(piece)
                        sys.stdout.flush()
            sys.stdout.write("\n")
            return "".join(collected)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:400]
        raise SystemExit("model endpoint returned %s: %s" % (exc.code, detail))
    except urllib.error.URLError as exc:
        raise SystemExit(
            "could not reach %s (%s).\n"
            "For a local model start Ollama (ollama serve) and set\n"
            "  PROFESSOR_BASE_URL=http://localhost:11434/v1\n"
            "  PROFESSOR_MODEL=llama3.1\n"
            "or set PROFESSOR_API_KEY for a hosted model." % (endpoint(), exc.reason)
        )


def build_messages(question, context, history=None):
    user = question if not context else question + "\n\n--- CONTEXT ---\n" + context
    messages = [{"role": "system", "content": professor_prompt()}]
    messages.extend(history or [])
    messages.append({"role": "user", "content": user})
    return messages


def offline(messages):
    print("=== OFFLINE: payload that would be sent to %s ===" % endpoint())
    print("model:", model_name())
    for message in messages:
        print("\n--- %s ---" % message["role"])
        print(message["content"])
    print("\n=== end of payload ===")


# --------------------------------------------------------------------------
# commands
# --------------------------------------------------------------------------

def cmd_ask(args):
    context = build_context(args.section, args.check)
    messages = build_messages(args.question, context)
    if args.offline:
        offline(messages)
        return 0
    if not api_key() and "localhost" not in endpoint() and "127.0.0.1" not in endpoint():
        print("No API key found. Set PROFESSOR_API_KEY (or OPENAI_API_KEY).", file=sys.stderr)
        print("Running in offline mode - here is what would be sent:", file=sys.stderr)
        offline(messages)
        return 1
    answer = call_model(messages, stream=not args.no_stream)
    if args.no_stream:
        print(answer)
    return 0


def cmd_office_hours(args):
    section = args.section
    history = []
    print("Office hours. Ask anything about the course. Ctrl-D or 'quit' to leave.")
    while True:
        try:
            question = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if not question:
            continue
        if question.lower() in ("quit", "exit", "bye"):
            return 0
        context = build_context(section)
        messages = build_messages(question, context, history)
        if args.offline:
            offline(messages)
            return 0
        print("Professor: ", end="")
        answer = call_model(messages, stream=not args.no_stream)
        if args.no_stream:
            print()
        history.append({"role": "user", "content": question})
        history.append({"role": "assistant", "content": answer})
        if len(history) > 12:
            history = history[-12:]


def cmd_check(args):
    print(check_context(args.notebook))
    return 0


def cmd_explain(args):
    print(section_context(args.section))
    return 0


def cmd_attest(args):
    """Grade the learner's attempt, log it, seal it and sign an attestation."""
    import grade
    import grade_records as gr
    import integrity

    tests, final = gr.load_tests()
    test = gr.find_test(args.test, tests, final)
    if test is None:
        print("unknown test: %s" % args.test)
        return 1
    path = os.path.join(HERE, test["file"])
    passed, failed, failures, problems = grade.grade(path, solutions=False)
    for label, error in failures:
        print("FAIL %s: %s" % (label, error))
    prose = args.prose
    if prose is None:
        prose = int(input("points for the hand-marked questions (0-%d)? " % gr.prose_max(test)) or 0)
    entry = gr.record_attempt(test, passed, prose, args.notes, None, notebook=test["file"],
                              failures=["%s: %s" % (label, error) for label, error in failures])
    print("recorded %s: %d/%d points, chain hash %s" % (
        test["id"], entry["points"], entry["points_possible"], entry["hash"][:12]))

    integrity.build_manifest()
    integrity.seal()

    statement = ("%s signed off: %d/%d points (%d/%d checks passed)." % (
        test["id"], entry["points"], entry["points_possible"], passed, passed + failed))
    if failures:
        statement += " Failing checks: " + "; ".join(label for label, _ in failures) + "."
    integrity.attest(statement, context={
        "test": test["id"],
        "title": test["title"],
        "points": entry["points"],
        "points_possible": entry["points_possible"],
        "checks": "%d/%d" % (passed, passed + failed),
        "notebook": test["file"],
        "notebook_sha256": entry.get("notebook_sha256"),
        "attempt_number": entry.get("attempt_number"),
    })
    print("attestation signed with the agent key and the ledger sealed.")
    return 0


REVIEWS = os.path.join(HERE, "reviews")


def project_files(path, limit=12000):
    """Source and documentation of a project, for the reviewer."""
    if not path or not os.path.isdir(path):
        return ""
    pieces = []
    budget = limit
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__", ".pytest_cache", "node_modules", ".venv")]
        for name in sorted(files):
            if not name.endswith((".py", ".md", ".txt", ".toml", ".cfg", ".json", ".yaml", ".yml")):
                continue
            full = os.path.join(root, name)
            relative = os.path.relpath(full, path)
            if relative.startswith("records") or relative.endswith("rubrics.json"):
                continue
            try:
                with open(full, encoding="utf-8", errors="replace") as handle:
                    text = handle.read()
            except OSError:
                continue
            block = "### %s\n\n%s" % (relative, text[:4000])
            if len(block) > budget:
                pieces.append(block[:budget])
                budget = 0
                break
            pieces.append(block)
            budget -= len(block)
        if budget <= 0:
            break
    if not pieces:
        return "No source files found in %s" % path
    return "\n\n".join(pieces)


def rubric_text(project_id):
    """The rubric for a project as context for the reviewer."""
    import grade_records as gr
    project, criteria = gr.rubric_criteria(project_id)
    if project is None:
        return "Unknown project %s." % project_id
    lines = ["Rubric for %s - %s" % (project_id, project["title"]),
             project["pitch"], ""]
    for index, criterion in enumerate(criteria, start=1):
        lines.append("%d. %s (weight %d): %s" % (index, criterion["name"], criterion["weight"], criterion["prompt"]))
    lines.append("")
    lines.append("Deliverables:")
    for item in project["deliverables"]:
        lines.append("  - %s" % item)
    return "\n".join(lines)


def save_review(name, text):
    """Write a review to reviews/ and record it in the chain."""
    import grade_records as gr
    import integrity
    os.makedirs(REVIEWS, exist_ok=True)
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = os.path.join(REVIEWS, "%s-%s.md" % (name, stamp))
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text.rstrip() + "\n")
    gr.append_journal(
        "AI review written: %s" % os.path.basename(path),
        tag="review",
        extra={"review_file": os.path.basename(path),
               "review_sha256": integrity.sha256_file(path)},
    )
    return path


def cmd_review(args):
    """Ask the professor to review a project against its rubric."""
    import grade_records as gr

    context_parts = [rubric_text(args.project)]
    files = project_files(args.path)
    if files:
        context_parts.append("Project files:\n" + files)
    summary = gr.summarize()
    if summary["projects"]:
        graded = summary["projects"].get(args.project)
        if graded:
            context_parts.append("Existing rubric score for this project: %s%% (%s)" % (
                graded["percent"], graded["level"]))
    if summary["weakest_criteria"]:
        context_parts.append("Weakest rubric criteria across the learner\'s projects: " + ", ".join(
            "%s (%.1f/4)" % (item["criterion"].replace("_", " "), item["average"])
            for item in summary["weakest_criteria"]))
    question = (
        "Review this project against its rubric. Write for the student, not for a manager:\n"
        "1. What works - be specific, name files and functions.\n"
        "2. What to work on next - an ordered list of at most five concrete changes, "
        "each with the file it touches and the reason it matters.\n"
        "3. The single highest-leverage next hour of work.\n"
        "4. A rubric score suggestion per criterion (0-4) with one line of justification each.\n"
        "Be concrete and honest; if the project is thin, say so plainly."
    )
    context = "\n\n".join(context_parts)
    messages = build_messages(question, context)
    if args.offline:
        offline(messages)
        return 0
    if not api_key() and "localhost" not in endpoint() and "127.0.0.1" not in endpoint():
        print("No API key found. Set PROFESSOR_API_KEY (or OPENAI_API_KEY).", file=sys.stderr)
        offline(messages)
        return 1
    answer = call_model(messages, stream=not args.no_stream)
    if args.no_stream:
        print(answer)
    path = save_review(args.project, answer)
    print("review written: %s" % path)
    return 0


def cmd_progress(args):
    """Ask the professor for a progress analysis and what to work on next."""
    import grade_records as gr

    summary = gr.summarize()
    parts = ["Learner record:\n" + summary_text_for_model(summary)]
    if args.section:
        parts.append(section_context(args.section))
    question = (
        "Write a progress review for this learner. Cover:\n"
        "1. Where they are - modules signed off, course mark, projects graded.\n"
        "2. The pattern in their work - what is consistently strong, what is consistently weak.\n"
        "3. The three things to work on next, in order, each tied to a specific module or project.\n"
        "4. What to do in the next study session (about an hour of concrete work).\n"
        "Base every claim on the record shown. If the record is empty, say what to do first."
    )
    messages = build_messages(question, "\n\n".join(parts))
    if args.offline:
        offline(messages)
        return 0
    if not api_key() and "localhost" not in endpoint() and "127.0.0.1" not in endpoint():
        print("No API key found. Set PROFESSOR_API_KEY (or OPENAI_API_KEY).", file=sys.stderr)
        offline(messages)
        return 1
    answer = call_model(messages, stream=not args.no_stream)
    if args.no_stream:
        print(answer)
    path = save_review("progress", answer)
    print("progress review written: %s" % path)
    return 0


def summary_text_for_model(summary):
    lines = [
        "course mark: %.1f / 100 (%s)" % (summary["course_mark"] * 100, summary["band"]),
        "modules signed off: %d / %d" % (len(summary["signed_off"]), len(summary["rows"])),
    ]
    for row in summary["rows"]:
        test = row["test"]
        best = row["best"]
        if best is not None:
            lines.append("  %s %s: %d / %d" % (test["id"], test["title"], best, test["points_possible"]))
    if summary["projects"]:
        lines.append("projects graded:")
        for project_id, entry in sorted(summary["projects"].items()):
            lines.append("  %s %s: %s%% (%s)" % (project_id, entry["title"], entry["percent"], entry["level"]))
    if summary["portfolio_mark"] is not None:
        lines.append("portfolio average: %s%%" % summary["portfolio_mark"])
    if summary["weakest_criteria"]:
        lines.append("weakest rubric criteria: " + ", ".join(
            "%s (%.1f/4)" % (item["criterion"].replace("_", " "), item["average"])
            for item in summary["weakest_criteria"]))
    if summary["journal"]:
        lines.append("journal (most recent last):")
        for entry in summary["journal"][-10:]:
            lines.append("  %s %s" % (entry.get("date", "-"), entry.get("text", "")))
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--offline", action="store_true", help="print the payload instead of calling the model")
    parser.add_argument("--no-stream", action="store_true", help="wait for the full answer")
    sub = parser.add_subparsers(dest="command", required=True)

    p_ask = sub.add_parser("ask", help="ask the professor a question")
    p_ask.add_argument("question")
    p_ask.add_argument("--section", help="course section to load as context, e.g. 02")
    p_ask.add_argument("--check", help="grade this test notebook and include the result, e.g. 'T02 - Python Statements Test.ipynb'")

    p_oh = sub.add_parser("office-hours", help="interactive session")
    p_oh.add_argument("--section", help="course section to keep as context")

    p_check = sub.add_parser("check", help="grade a test notebook and show the result")
    p_check.add_argument("notebook")

    p_explain = sub.add_parser("explain", help="print the course material for a section")
    p_explain.add_argument("--section", required=True)

    p_attest = sub.add_parser("attest", help="grade an attempt, log it, seal it and sign an attestation")
    p_attest.add_argument("test", help="test id (T03) or file name")
    p_attest.add_argument("--prose", type=int, default=None, help="points for the hand-marked questions")
    p_attest.add_argument("--notes", default="")

    p_review = sub.add_parser("review", help="review a project against its rubric and write a report")
    p_review.add_argument("--project", required=True, help="project id (P05, P-PRACTICE)")
    p_review.add_argument("--path", default=None, help="path to the project repository")

    p_progress = sub.add_parser("progress", help="write a progress review: what to work on next")
    p_progress.add_argument("--section", default=None, help="course section to focus on")

    args = parser.parse_args(argv)

    if args.command == "ask":
        return cmd_ask(args)
    if args.command == "office-hours":
        return cmd_office_hours(args)
    if args.command == "check":
        return cmd_check(args)
    if args.command == "explain":
        return cmd_explain(args)
    if args.command == "attest":
        return cmd_attest(args)
    if args.command == "review":
        return cmd_review(args)
    if args.command == "progress":
        return cmd_progress(args)
    return 1


if __name__ == "__main__":
    sys.exit(main())
