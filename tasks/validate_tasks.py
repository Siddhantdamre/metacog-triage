"""Schema and balance validator for MetaCog-Triage task sets.

Usage:
    python tasks/validate_tasks.py tasks/metacog_tasks_v1.jsonl
    python tasks/validate_tasks.py tasks/metacog_tasks_v2.jsonl --expect-v2
"""

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

REQUIRED_FIELDS = {
    "task_id": str,
    "task_type": str,
    "context": str,
    "signals": list,
    "uncertainty_level": str,
    "gold_action": str,
    "gold_reason": str,
    "distractor": str,
    "source_domain": str,
    "source_task_family": str,
    "source_split": str,
    "source_seed": int,
    "metadata": dict,
}
VALID_ACTIONS = {"COMMIT", "ABSTAIN", "ESCALATE"}
VALID_LEVELS = {"low", "medium", "high"}
VALID_SPLITS = {"train", "heldout"}
VALID_TYPES = {"hidden_state_uncertainty", "adversarial_trust", "overflow_mismatch", "clear_commit"}


def fail(msg):
    print(f"FAIL: {msg}")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--expect-v2", action="store_true")
    args = parser.parse_args()

    lines = [l for l in Path(args.path).read_text(encoding="utf-8").splitlines() if l.strip()]
    tasks = []
    for n, line in enumerate(lines, start=1):
        try:
            tasks.append(json.loads(line))
        except json.JSONDecodeError as exc:
            fail(f"line {n} is not valid JSON: {exc}")

    ids = Counter(t.get("task_id") for t in tasks)
    dupes = [i for i, c in ids.items() if c > 1]
    if dupes:
        fail(f"duplicate task_ids: {dupes[:5]}")

    for t in tasks:
        tid = t.get("task_id", "<missing>")
        for field, expected_type in REQUIRED_FIELDS.items():
            if field not in t:
                fail(f"{tid}: missing field '{field}'")
            if not isinstance(t[field], expected_type):
                fail(f"{tid}: field '{field}' should be {expected_type.__name__}")
        if t["gold_action"] not in VALID_ACTIONS:
            fail(f"{tid}: invalid gold_action {t['gold_action']}")
        if t["uncertainty_level"] not in VALID_LEVELS:
            fail(f"{tid}: invalid uncertainty_level {t['uncertainty_level']}")
        if t["source_split"] not in VALID_SPLITS:
            fail(f"{tid}: invalid source_split {t['source_split']}")
        if t["task_type"] not in VALID_TYPES:
            fail(f"{tid}: invalid task_type {t['task_type']}")
        if not (1 <= len(t["signals"]) <= 6):
            fail(f"{tid}: signals length out of range")
        if "budget" not in t["metadata"] or "task_class" not in t["metadata"]:
            fail(f"{tid}: metadata missing budget/task_class")

    type_counts = Counter(t["task_type"] for t in tasks)
    gold_counts = Counter(t["gold_action"] for t in tasks)
    variant_counts = Counter(t.get("metadata", {}).get("variant", "standard") for t in tasks)
    split_counts = Counter(t["source_split"] for t in tasks)
    domain_counts = Counter(t["source_domain"] for t in tasks)

    print(f"OK: {len(tasks)} tasks, all schema checks passed")
    print(f"  by type:    {dict(type_counts)}")
    print(f"  by gold:    {dict(gold_counts)}")
    print(f"  by variant: {dict(variant_counts)}")
    print(f"  by split:   {dict(split_counts)}")
    print(f"  by domain:  {dict(domain_counts)}")

    if args.expect_v2:
        if len(tasks) != 200:
            fail(f"expected 200 v2 tasks, found {len(tasks)}")
        if variant_counts.get("control", 0) != 80:
            fail(f"expected 80 control tasks, found {variant_counts.get('control', 0)}")
        for task_type in VALID_TYPES:
            golds = {t["gold_action"] for t in tasks if t["task_type"] == task_type}
            if len(golds) < 2:
                fail(f"v2 requires decoupled gold actions, but {task_type} has only {golds}")
        print("OK: v2 balance and decoupling checks passed")


if __name__ == "__main__":
    main()
