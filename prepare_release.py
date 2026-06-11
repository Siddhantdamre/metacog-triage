"""One-shot preparation script for the MetaCog-Triage release package.

Copies the frozen v1 task set and existing result files from the
Emotion_and_AI repo when available, then validates the packaged artifacts.

Run from the package root:

    python prepare_release.py

The public repository is self-contained. When the parent repo is unavailable,
the script keeps the packaged frozen artifacts and continues validation.
To refresh from a parent checkout, pass its root explicitly:

    python prepare_release.py --repo-root /path/to/Emotion_and_AI
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent

COPIES = [
    # (source relative to repo root, destination relative to package root)
    ("benchmarks/exec_meta_adapt/frontier/frontier_tasks_metacog.jsonl", "tasks/metacog_tasks_v1.jsonl"),
    ("results/frontier_local/full_40/comparison_table.md", "results/v1_two_model/comparison_table.md"),
    ("results/frontier_local/full_40/qwen_results.json", "results/v1_two_model/qwen_results.json"),
    ("results/frontier_local/full_40/smollm_results.json", "results/v1_two_model/smollm_results.json"),
    ("results/frontier_local/open_model_expansion/full_40_single/comparison_table.md", "results/v1_four_model/comparison_table.md"),
    ("submission/frontier_local_metacognition/frontier_local_metacognition_behavior.svg", "paper/figures/behavior_v1.svg"),
]

OPTIONAL_GLOB_COPIES = [
    ("results/frontier_local/open_model_expansion/full_40_single", "results/v1_four_model", "*_results.json"),
]


def copy_one(repo_root: Path, src_rel: str, dst_rel: str) -> bool:
    src = repo_root / src_rel
    dst = PACKAGE_ROOT / dst_rel
    if not src.exists():
        if dst.exists():
            print(f"  using packaged artifact: {dst_rel}")
            return True
        print(f"  MISSING (skipped): {src_rel}")
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    print(f"  copied: {src_rel} -> {dst_rel}")
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=str(PACKAGE_ROOT.parent))
    args = parser.parse_args()
    repo_root = Path(args.repo_root)

    print(f"Repo root: {repo_root}")
    print("Copying frozen artifacts...")
    copied = sum(copy_one(repo_root, s, d) for s, d in COPIES)

    for src_dir_rel, dst_dir_rel, pattern in OPTIONAL_GLOB_COPIES:
        src_dir = repo_root / src_dir_rel
        if src_dir.exists():
            for path in sorted(src_dir.glob(pattern)):
                dst = PACKAGE_ROOT / dst_dir_rel / path.name
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, dst)
                print(f"  copied: {src_dir_rel}/{path.name} -> {dst_dir_rel}/{path.name}")

    print(f"\n{copied}/{len(COPIES)} required artifacts copied.")

    v1 = PACKAGE_ROOT / "tasks" / "metacog_tasks_v1.jsonl"
    if v1.exists():
        print("\nValidating v1 task set...")
        result = subprocess.run(
            [sys.executable, str(PACKAGE_ROOT / "tasks" / "validate_tasks.py"), str(v1)],
        )
        if result.returncode != 0:
            sys.exit("v1 task validation FAILED")

    print("\nGenerating v2 task set...")
    result = subprocess.run(
        [sys.executable, str(PACKAGE_ROOT / "tasks" / "generate_tasks_v2.py")],
    )
    if result.returncode != 0:
        sys.exit("v2 generation FAILED")

    v2 = PACKAGE_ROOT / "tasks" / "metacog_tasks_v2.jsonl"
    print("\nValidating v2 task set...")
    result = subprocess.run(
        [sys.executable, str(PACKAGE_ROOT / "tasks" / "validate_tasks.py"), str(v2), "--expect-v2"],
    )
    if result.returncode != 0:
        sys.exit("v2 task validation FAILED")

    print("\nRelease package prepared. Next: see RELEASE_CHECKLIST.md")


if __name__ == "__main__":
    main()
