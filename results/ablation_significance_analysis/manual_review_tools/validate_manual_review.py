"""
validate_manual_review.py

Checks a completed manual_architectural_review CSV against the aggregate
numbers already claimed in the response letter to Reviewer 2, Comment 5:

    - 6/20 (30%) instances fully correct for BOTH configurations
    - 14/20 instances with at least one architectural issue in at least
      one configuration
    - 0 instances where one configuration is judged correct and the
      other is not
    - Among the 14 failing instances: 8/14 = spurious_token_injection,
      3/14 = unrelated_mutation (including exactly 1 case of
      dropped_block, Direct Evolution / DELETE_COMPONENT)

Usage:
    python validate_manual_review.py manual_review_20instances.csv
"""

import csv
import sys
from collections import Counter


EXPECTED = {
    "both_correct": 6,
    "n_total": 20,
    "n_failing": 14,
    "split_disagreement": 0,  # instances where arch and de disagree on fully_correct
    "spurious_token_injection": 8,   # out of 14 failing
    "unrelated_mutation": 3,         # out of 14 failing (includes the dropped_block case)
    "dropped_block_cases": 1,        # subset of unrelated_mutation
}


def to_bool(value):
    return str(value).strip().lower() in ("yes", "true", "1", "correct")


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)

    path = sys.argv[1]
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    if len(rows) != EXPECTED["n_total"]:
        print(f"⚠️  Expected {EXPECTED['n_total']} rows, found {len(rows)}.")

    both_correct = 0
    disagreement = 0
    failure_modes_arch = Counter()
    failure_modes_de = Counter()
    incomplete_rows = []

    for r in rows:
        arch_ok = to_bool(r.get("arch_fully_correct", ""))
        de_ok = to_bool(r.get("de_fully_correct", ""))

        if not r.get("arch_fully_correct") or not r.get("de_fully_correct"):
            incomplete_rows.append(r.get("id"))
            continue

        if arch_ok and de_ok:
            both_correct += 1
        if arch_ok != de_ok:
            disagreement += 1

        if not arch_ok:
            mode = r.get("arch_failure_mode", "").strip()
            if mode:
                failure_modes_arch[mode] += 1
        if not de_ok:
            mode = r.get("de_failure_mode", "").strip()
            if mode:
                failure_modes_de[mode] += 1

    n_failing = len(rows) - both_correct
    combined_modes = failure_modes_arch + failure_modes_de
    dropped_block_total = combined_modes.get("dropped_block", 0)

    print("="*70)
    print("RESULTS FROM YOUR FILLED REVIEW")
    print("="*70)
    print(f"Both configurations fully correct : {both_correct}/{len(rows)}")
    print(f"At least one issue (either config): {n_failing}/{len(rows)}")
    print(f"Disagreement (one correct, other not): {disagreement}")
    print(f"Failure modes (ArchPipeline)  : {dict(failure_modes_arch)}")
    print(f"Failure modes (Direct Evolution): {dict(failure_modes_de)}")
    print(f"Combined 'dropped_block' cases  : {dropped_block_total}")
    if incomplete_rows:
        print(f"⚠️  Incomplete rows (fully_correct not set): {incomplete_rows}")

    print()
    print("="*70)
    print("COMPARISON WITH RESPONSE LETTER CLAIMS")
    print("="*70)

    checks = [
        ("Both correct = 6/20", both_correct == EXPECTED["both_correct"]),
        ("Failing = 14/20", n_failing == EXPECTED["n_failing"]),
        ("0 disagreement between configs", disagreement == EXPECTED["split_disagreement"]),
        ("dropped_block cases = 1", dropped_block_total == EXPECTED["dropped_block_cases"]),
    ]

    all_ok = True
    for label, ok in checks:
        status = "✅" if ok else "❌ MISMATCH"
        print(f"{status:12s} {label}")
        all_ok = all_ok and ok

    print()
    if all_ok:
        print("✅ Your filled review is consistent with the response letter. "
              "Safe to commit to results/manual_architectural_review_20instances/.")
    else:
        print("❌ Mismatch detected. Before committing, either:")
        print("   (a) re-check your judgments — this template should formalize")
        print("       the review you already performed, not a fresh independent one, or")
        print("   (b) if your real judgments differ from the letter, update the")
        print("       manuscript and response letter to report the actual numbers.")


if __name__ == "__main__":
    main()
