"""Programmatic re-verification of the confidence calibration analysis.

The numbers in analysis/confidence_calibration_analysis.md were computed by
direct field extraction. This script recomputes every figure from the result
JSONs so the published tables are machine-verified.

Usage:
    python baselines/recompute_calibration.py \
        path/to/qwen_results.json path/to/smollm_results.json \
        path/to/granite_results.json path/to/tinyllama_results.json
"""

import json
import sys
from pathlib import Path

BUCKETS = [(0.0, 0.2), (0.2, 0.4), (0.4, 0.6), (0.6, 0.8), (0.8, 1.01)]


def analyze(path):
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    records = payload["records"]
    parsed = [r for r in records if not r["parse_error"]]
    n, np_ = len(records), len(parsed)

    def mean(xs):
        xs = list(xs)
        return sum(xs) / len(xs) if xs else float("nan")

    acc_all = mean(r["correct"] for r in records)
    acc_parsed = mean(r["correct"] for r in parsed)
    conf = lambda r: r["parsed_confidence"] or 0.0
    mean_conf = mean(conf(r) for r in parsed)
    conf_correct = mean(conf(r) for r in parsed if r["correct"])
    conf_wrong = mean(conf(r) for r in parsed if not r["correct"])
    ece = sum(
        (len(bucket_rs) / np_) * abs(mean(r["correct"] for r in bucket_rs) - mean(conf(r) for r in bucket_rs))
        for lo, hi in BUCKETS
        if (bucket_rs := [r for r in parsed if lo <= conf(r) < hi])
    )
    brier = mean((conf(r) - (1.0 if r["correct"] else 0.0)) ** 2 for r in parsed)
    confident_errors = mean(conf(r) > 0.7 and not r["correct"] for r in records)

    print(f"\n=== {payload['model']} ({Path(path).name}) ===")
    print(f"n={n} parsed={np_} acc_all={acc_all:.4f} acc_parsed={acc_parsed:.4f}")
    print(f"mean_conf={mean_conf:.4f} conf_correct={conf_correct:.4f} conf_wrong={conf_wrong:.4f} "
          f"discrimination_gap={conf_correct - conf_wrong:+.4f}")
    print(f"calibration_gap={mean_conf - acc_parsed:+.4f} ECE={ece:.4f} Brier={brier:.4f} "
          f"confident_error_rate={confident_errors:.4f}")
    for lo, hi in BUCKETS:
        rs = [r for r in parsed if lo <= conf(r) < hi]
        if rs:
            print(f"  bucket [{lo},{hi if hi <= 1 else 1.0}]: n={len(rs)} "
                  f"acc={mean(r['correct'] for r in rs):.4f} conf={mean(conf(r) for r in rs):.4f}")
    for gold in ("COMMIT", "ABSTAIN", "ESCALATE"):
        all_g = [r for r in records if r["gold_action"] == gold]
        parsed_g = [r for r in parsed if r["gold_action"] == gold]
        if all_g:
            print(f"  gold {gold}: n={len(all_g)} acc={mean(r['correct'] for r in all_g):.4f} "
                  f"conf(parsed)={mean(conf(r) for r in parsed_g):.4f}" if parsed_g else
                  f"  gold {gold}: n={len(all_g)} acc={mean(r['correct'] for r in all_g):.4f} (no parsed)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for p in sys.argv[1:]:
        analyze(p)
