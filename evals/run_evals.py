#!/usr/bin/env python3
"""Run the behavioural evals, score them, and print the with-skill delta.

Three subcommands:

    python3 evals/run_evals.py run  [--arm both] [--eval ID ...] [--model M]
    python3 evals/run_evals.py score [--model M]
    python3 evals/run_evals.py report

`run` plays each eval twice, once with the package available through a load_skill tool and once
with no package at all. The analyst is scripted: the canned lines are sent in order, verbatim, and
an uncovered question gets "you decide for now", exactly as evals/README.md says a person should.

`score` judges every assertion from the transcript and writes scores.json beside the transcripts.
`report` prints the two arms side by side, which is the only number that means anything: an
assertion the package passes and the baseline fails is an instruction doing work.

Standard library only, like the rest of the package. Needs OPENROUTER_API_KEY, or any
OpenAI-compatible endpoint via BISON_EVAL_BASE_URL.
"""
import argparse
import datetime
import json
import os
import re
import sys
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVALS = os.path.join(ROOT, "evals", "evals.json")
SKILLS = os.path.join(ROOT, "skills")
RUNS = os.path.join(ROOT, "evals", "runs")
BASE_URL = os.environ.get("BISON_EVAL_BASE_URL", "https://openrouter.ai/api/v1")
DEFAULT_MODEL = os.environ.get("BISON_EVAL_MODEL", "openrouter/auto")
MAX_TOOL_CALLS = 14
ONE_LINE = "you decide for now"


# -- package access ---------------------------------------------------------------------
def skill_catalog():
    """[(name, description)] for every skill, read from its frontmatter."""
    out = []
    for name in sorted(os.listdir(SKILLS)):
        path = os.path.join(SKILLS, name, "SKILL.md")
        if not os.path.isfile(path):
            continue
        text = open(path, encoding="utf-8").read()
        match = re.search(r"^description:\s*(.+)$", text, re.M)
        desc = match.group(1).strip().strip('"') if match else ""
        out.append((name, desc))
    return out


def read_skill(name, relpath=None):
    """SKILL.md for a skill, or one of its own files."""
    if relpath is None or relpath in ("", "SKILL.md"):
        path = os.path.join(SKILLS, name, "SKILL.md")
    else:
        path = os.path.normpath(os.path.join(SKILLS, name, relpath))
        if not path.startswith(os.path.join(SKILLS, name)):
            return "That path is outside the skill."
    if not os.path.isfile(path):
        return "No such file in the %s skill. Its files are: %s" % (name, ", ".join(sorted(
            os.path.relpath(os.path.join(dirpath, f), os.path.join(SKILLS, name))
            for dirpath, _dirs, files in os.walk(os.path.join(SKILLS, name)) for f in files)))
    return open(path, encoding="utf-8").read()


TOOLS = [
    {"type": "function", "function": {
        "name": "load_skill",
        "description": "Load an installed skill's instructions. Call this when a skill applies, "
                       "before doing the work it covers.",
        "parameters": {"type": "object", "properties": {
            "name": {"type": "string", "description": "skill name"}},
            "required": ["name"]}}},
    {"type": "function", "function": {
        "name": "read_skill_file",
        "description": "Read a file the loaded skill points at, such as references/foo.md.",
        "parameters": {"type": "object", "properties": {
            "skill": {"type": "string"}, "path": {"type": "string"}},
            "required": ["skill", "path"]}}},
]


def system_prompt(arm):
    base = ("You are helping a finance student build an equity pitch for their fund. Answer in "
            "plain, direct English. Never mention being an AI or a language model.")
    if arm == "without-skill":
        return base
    catalog = "\n".join("- %s: %s" % (name, desc) for name, desc in skill_catalog())
    return base + ("\n\nThe following skills are installed. When one applies to what the student "
                   "asks, call load_skill with its name and follow it, including any file it "
                   "points at that you need. Do not announce that you are loading a skill.\n\n"
                   + catalog)


# -- model calls ------------------------------------------------------------------------
def chat(messages, model, tools=None, temperature=0.7):
    payload = {"model": model, "messages": messages, "temperature": temperature}
    if tools:
        payload["tools"] = tools
    request = urllib.request.Request(
        BASE_URL + "/chat/completions",
        data=json.dumps(payload).encode(),
        headers={"Authorization": "Bearer " + os.environ["OPENROUTER_API_KEY"],
                 "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=300) as response:
        body = json.loads(response.read().decode())
    return body


def call_with_tools(messages, model, tools, log):
    """One assistant turn, running any tool calls until it answers in prose."""
    calls = 0
    while True:
        body = chat(messages, model, tools)
        message = body["choices"][0]["message"]
        used = body.get("model") or model
        wanted = message.get("tool_calls") or []
        if not wanted or calls >= MAX_TOOL_CALLS:
            messages.append({"role": "assistant", "content": message.get("content") or ""})
            log.append({"role": "assistant", "content": message.get("content") or "",
                        "model": used})
            return message.get("content") or "", used
        messages.append({"role": "assistant", "content": message.get("content") or "",
                         "tool_calls": wanted})
        for call in wanted:
            name = call["function"]["name"]
            try:
                args = json.loads(call["function"].get("arguments") or "{}")
            except ValueError:
                args = {}
            if name == "load_skill":
                result = read_skill(args.get("name", ""))
            elif name == "read_skill_file":
                result = read_skill(args.get("skill", ""), args.get("path", ""))
            else:
                result = "unknown tool"
            calls += 1
            log.append({"role": "tool", "name": name, "arguments": args,
                        "chars": len(result)})
            messages.append({"role": "tool", "tool_call_id": call.get("id", ""),
                             "content": result})


def run_one(eval_spec, arm, model, scripts):
    lines = list(scripts[eval_spec["script"]]["lines"])
    tools = TOOLS if arm == "with-skill" else None
    messages = [{"role": "system", "content": system_prompt(arm)},
                {"role": "user", "content": eval_spec["prompt"]}]
    transcript = [{"role": "user", "content": eval_spec["prompt"]}]
    used_models = []
    extra = 0
    for turn in range(1, 21):
        text, used = call_with_tools(messages, model, tools, transcript)
        used_models.append(used)
        if lines:
            reply = lines.pop(0)
        elif "?" in text and extra < 2:
            reply = ONE_LINE
            extra += 1
        else:
            break
        messages.append({"role": "user", "content": reply})
        transcript.append({"role": "user", "content": reply})
    return transcript, sorted(set(used_models))


def write_transcript(eval_spec, arm, model, transcript, models, stamp):
    os.makedirs(os.path.join(RUNS, stamp), exist_ok=True)
    path = os.path.join(RUNS, stamp, "%s.%s.%s.md" % (eval_spec["id"], arm, stamp))
    out = ["# %s, %s" % (eval_spec["id"], arm), "",
           "- prompt: %s" % eval_spec["prompt"],
           "- model: %s" % ", ".join(models),
           "- date: %s" % stamp, ""]
    for turn in transcript:
        who = "Analyst" if turn["role"] == "user" else "Assistant"
        if turn["role"] == "tool":
            out.append("_%s called %s %s, %d characters returned_" % (
                "Assistant", turn["name"], json.dumps(turn.get("arguments", {})), turn["chars"]))
            out.append("")
            continue
        out.append("**%s.** %s" % (who, turn["content"]))
        out.append("")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(out))
    return path


# -- scoring ----------------------------------------------------------------------------
JUDGE_PROMPT = """You are scoring one assertion from a behavioural eval of an AI assistant for a
student building an equity pitch.

Score pass or fail from the transcript alone. Judge what the transcript does, not what it intends. A
correct rule stated in a sentence that also contains a violation is a fail. Do not give the
assistant credit for something it did not do.

Assertion: {statement}

Pass/fail rule: {judge}

Transcript:

{transcript}

Answer with JSON only, no prose around it:
{{"pass": true or false, "quote": "<the line that decided it, at most 30 words>"}}"""


def score_one(transcript_text, assertion, model):
    prompt = JUDGE_PROMPT.format(statement=assertion["statement"], judge=assertion["judge"],
                                 transcript=transcript_text)
    body = chat([{"role": "user", "content": prompt}], model, temperature=0)
    text = body["choices"][0]["message"].get("content") or ""
    match = re.search(r"\{.*\}", text, re.S)
    if not match:
        return {"pass": None, "quote": text[:200]}
    try:
        verdict = json.loads(match.group(0))
    except ValueError:
        return {"pass": None, "quote": text[:200]}
    return {"pass": bool(verdict.get("pass")), "quote": str(verdict.get("quote", ""))[:300]}


def transcripts_by_run():
    out = {}
    for stamp in sorted(os.listdir(RUNS)) if os.path.isdir(RUNS) else []:
        folder = os.path.join(RUNS, stamp)
        for name in sorted(os.listdir(folder)):
            if not name.endswith(".md"):
                continue
            eval_id, arm = name.split(".")[0], name.split(".")[1]
            out.setdefault(eval_id, {})[arm] = open(os.path.join(folder, name),
                                                    encoding="utf-8").read()
    return out


def do_score(model):
    specs = json.load(open(EVALS, encoding="utf-8"))
    found = transcripts_by_run()
    scores = {}
    for spec in specs["evals"]:
        for arm, text in sorted(found.get(spec["id"], {}).items()):
            rows = []
            for assertion in spec["assertions"]:
                verdict = score_one(text, assertion, model)
                verdict["id"] = assertion["id"]
                verdict["level"] = assertion.get("level", "must")
                verdict["statement"] = assertion["statement"]
                rows.append(verdict)
                print("  %-22s %-13s %-28s %s" % (spec["id"], arm, assertion["id"],
                                                  "pass" if verdict["pass"] else "FAIL"))
            scores.setdefault(spec["id"], {})[arm] = rows
    path = os.path.join(RUNS, "scores.json")
    with open(path, "w", encoding="utf-8") as handle:
        json.dump({"scored": datetime.date.today().isoformat(), "judge": model,
                   "scores": scores}, handle, indent=1)
    return path


def do_report():
    path = os.path.join(RUNS, "scores.json")
    if not os.path.isfile(path):
        sys.exit("No scores yet. Run: python3 evals/run_evals.py score")
    data = json.load(open(path, encoding="utf-8"))["scores"]
    print("%-24s %-30s %-6s %-9s %s" % ("eval", "assertion", "base", "with", "verdict"))
    total = {"without-skill": 0, "with-skill": 0}
    count = 0
    wins = losses = ties_pass = ties_fail = 0
    for eval_id, arms in data.items():
        base = {row["id"]: row["pass"] for row in arms.get("without-skill", [])}
        skill = {row["id"]: row["pass"] for row in arms.get("with-skill", [])}
        for row in arms.get("with-skill", []) or arms.get("without-skill", []):
            name = row["id"]
            b, s = base.get(name), skill.get(name)
            count += 1
            total["without-skill"] += 1 if b else 0
            total["with-skill"] += 1 if s else 0
            if b is False and s is True:
                verdict, wins = "gain", wins + 1
            elif b is True and s is False:
                verdict, losses = "REGRESSION", losses + 1
            elif b is True and s is True:
                verdict, ties_pass = "both pass", ties_pass + 1
            else:
                verdict, ties_fail = "both fail", ties_fail + 1
            print("%-24s %-30s %-6s %-9s %s" % (eval_id, name, b, s, verdict))
    print()
    print("assertions: %d" % count)
    print("baseline pass: %d  with-skill pass: %d" % (total["without-skill"], total["with-skill"]))
    print("gain %d, regression %d, both pass %d, both fail %d" % (wins, losses, ties_pass, ties_fail))
    if total["without-skill"]:
        print("ratio of passing assertions: %.1fx" % (
            total["with-skill"] / float(total["without-skill"])))


def main(argv=None):
    parser = argparse.ArgumentParser(description="Run, score, and report the behavioural evals.")
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run")
    run.add_argument("--arm", choices=["with-skill", "without-skill", "both"], default="both")
    run.add_argument("--eval", action="append", default=None)
    run.add_argument("--model", default=DEFAULT_MODEL)
    run.add_argument("--stamp", default=datetime.date.today().isoformat())
    score = sub.add_parser("score")
    score.add_argument("--model", default=DEFAULT_MODEL)
    sub.add_parser("report")
    args = parser.parse_args(argv)

    if args.command == "run":
        specs = json.load(open(EVALS, encoding="utf-8"))
        scripts = specs["analysis_scripts"]
        arms = ["with-skill", "without-skill"] if args.arm == "both" else [args.arm]
        for spec in specs["evals"]:
            if args.eval and spec["id"] not in args.eval:
                continue
            for arm in arms:
                print("running %s %s" % (spec["id"], arm))
                transcript, models = run_one(spec, arm, args.model, scripts)
                path = write_transcript(spec, arm, args.model, transcript, models, args.stamp)
                print("  -> %s (%d turns, model %s)" % (
                    os.path.relpath(path, ROOT), len(transcript), ", ".join(models)))
        return 0
    if args.command == "score":
        path = do_score(args.model)
        print("wrote %s" % os.path.relpath(path, ROOT))
        return 0
    do_report()
    return 0


if __name__ == "__main__":
    sys.exit(main())
