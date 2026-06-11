"""Trivial baselines for MetaCog-Triage.

Baselines: random, always-commit, always-abstain, always-escalate,
majority-class, and a surface-keyword policy that deliberately reads only
shallow vocabulary (no evidence-state reasoning). The keyword baseline is
the important one: on v1 (where gold action correlates with task type) it
should score HIGH, and on v2 control variants it should collapse — that
contrast quantifies how much of any model's score is surface matching.

Usage:
    python baselines/baselines.py --tasks tasks/metacog_tasks_v1.jsonl \
        --output analysis/baseline_results_v1.csv
    python baselines/baselines.py --tasks tasks/metacog_tasks_v2.jsonl \
        --output analysis/baseline_results_v2.csv
"""

import argparse
import csv
import json
import random
from collections import Counter
from pathlib import Path

ACTIONS = ["COMMIT", "ABSTAIN", "ESCALATE"]

ESCALATE_KEYWORDS = (
    "trust", "deceptive", "conflict", "contradiction", "adversarial",
    "stale", "suspicion", "irreconcilable", "overflow", "capacity",
    "insufficiency", "family",
)
ABSTAIN_KEYWORDS = (
    "unchecked", "unqueried", "unobserved", "incomplete", "remain",
    "not locked", "provisional", "ambiguous", "untouched",
)
COMMIT_KEYWORDS = (
    "locked", "one surviving", "single surviving", "full coverage",
    "no contradiction remains", "converged",
)


def keyword_policy(task):
    text = (task["context"] + " " + " ".join(task["signals"])).lower()
    scores = {
        "ESCALATE": sum(text.count(k) for k in ESCALATE_KEYWORDS),
        "ABSTAIN": sum(text.count(k) for k in ABSTAIN_KEYWORDS),
        "COMMIT": sum(text.count(k) for k in COMMIT_KEYWORDS),
    }
    best = max(scores.values())
    if best == 0:
        return "ABSTAIN"
    # deterministic tie-break: ESCALATE > ABSTAIN > COMMIT
    for action in ("ESCALATE", "ABSTAIN", "COMMIT"):
        if scores[action] == best:
            return action


def evaluate(tasks, predict):
    rows = []
    for task in tasks:
        pred = predict(task)
        rows.append({
            "gold": task["gold_action"],
            "pred": pred,
            "correct": pred == task["gold_action"],
            "variant": task.get("metadata", {}).get("variant", "standard"),
        })
    return rows


def summarize(name, rows):
    n = len(rows)
    acc = sum(r["correct"] for r in rows) / n
    out = {"baseline": name, "n": n, "accuracy": round(acc, 4)}
    for gold in ACTIONS:
        sub = [r for r in rows if r["gold"] == gold]
        out[f"acc_gold_{gold}"] = round(sum(r["correct"] for r in sub) / len(sub), 4) if sub else ""
    for variant in ("standard", "control"):
        sub = [r for r in rows if r["variant"] == variant]
        out[f"acc_{variant}"] = round(sum(r["correct"] for r in sub) / len(sub), 4) if sub else ""
    out["over_escalation"] = round(
        sum(r["pred"] == "ESCALATE" and r["gold"] == "ABSTAIN" for r in rows) / n, 4)
    out["over_abstention"] = round(
        sum(r["pred"] == "ABSTAIN" and r["gold"] == "ESCALATE" for r in rows) / n, 4)
    out["bluff"] = round(
        sum(r["pred"] == "COMMIT" and r["gold"] != "COMMIT" for r in rows) / n, 4)
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tasks", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--random-seed", type=int, default=17)
    parser.add_argument("--random-trials", type=int, default=1000)
    args = parser.parse_args()

    tasks = [json.loads(l) for l in Path(args.tasks).read_text(encoding="utf-8").splitlines() if l.strip()]
    gold_counts = Counter(t["gold_action"] for t in tasks)
    majority = gold_counts.most_common(1)[0][0]
    print(f"{len(tasks)} tasks; gold distribution {dict(gold_counts)}; majority class {majority}")

    summaries = []
    for action in ACTIONS:
        summaries.append(summarize(f"always_{action.lower()}", evaluate(tasks, lambda t, a=action: a)))
    summaries.append(summarize("majority_class", evaluate(tasks, lambda t: majority)))

    rng = random.Random(args.random_seed)
    trial_summaries = []
    for _ in range(args.random_trials):
        trial_summaries.append(summarize("random", evaluate(tasks, lambda t: rng.choice(ACTIONS))))
    random_summary = {"baseline": f"random_uniform_mean_of_{args.random_trials}", "n": len(tasks)}
    for key in trial_summaries[0]:
        if key in ("baseline", "n"):
            continue
        vals = [s[key] for s in trial_summaries if s[key] != ""]
        random_summary[key] = round(sum(vals) / len(vals), 4) if vals else ""
    summaries.append(random_summary)

    summaries.append(summarize("surface_keyword", evaluate(tasks, keyword_policy)))

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(summaries[0].keys()))
        writer.writeheader()
        writer.writerows(summaries)
    for s in summaries:
        print(s)
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
