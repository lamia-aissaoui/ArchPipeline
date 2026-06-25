"""
build_review_template.py

Builds a fillable CSV template for the manual architectural review
(Reviewer 2, Comment 5) from the JSON file already produced by
08_Ablation_Significance_Analysis.ipynb (cell "STEP B — Extract 20
instances for manual review").

Usage:
    python build_review_template.py \
        --input manual_review_20instances.json \
        --output manual_review_20instances.csv

If --input is not found, an empty template with the 20 known instance
IDs is created instead (data columns left blank for manual completion).
"""

import argparse
import csv
import json
import os

# The 20 stratified instance IDs (seed=42), as produced by notebook 08.
# Kept here as a fallback so the template can still be generated even
# without the JSON file on hand.
KNOWN_IDS = [0, 5, 6, 8, 15, 17, 18, 21, 22, 25, 26, 36, 41, 44, 46, 86, 88, 102, 114, 119]

DATA_COLUMNS = [
    "id", "operation", "adl_type", "request", "reference",
    "archpipeline_prediction", "direct_evolution_prediction",
]

JUDGMENT_COLUMNS_TEMPLATE = [
    "{prefix}_identifier_preservation",
    "{prefix}_port_connector_binding",
    "{prefix}_property_value_correctness",
    "{prefix}_structural_placement",
    "{prefix}_formalism_constraint_satisfaction",
    "{prefix}_fully_correct",
    "{prefix}_failure_mode",
    "{prefix}_justification",
]

FOOTER_COLUMNS = ["rater", "review_date"]

ALLOWED_JUDGMENT_VALUES = "Correct / Incorrect / N/A"
ALLOWED_FAILURE_MODES = "none / spurious_token_injection / unrelated_mutation / dropped_block / other"


def build_columns():
    cols = list(DATA_COLUMNS)
    for prefix in ("arch", "de"):
        cols += [c.format(prefix=prefix) for c in JUDGMENT_COLUMNS_TEMPLATE]
    cols += FOOTER_COLUMNS
    return cols


def load_source(path):
    if path and os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        # normalize field names in case the JSON keys differ slightly
        rows = []
        for item in data:
            rows.append({
                "id": item.get("id"),
                "operation": item.get("operation", ""),
                "adl_type": item.get("adl_type", ""),
                "request": item.get("request", ""),
                "reference": item.get("reference", ""),
                "archpipeline_prediction": item.get("archpipeline_pred", item.get("archpipeline_prediction", "")),
                "direct_evolution_prediction": item.get("ablation_pred", item.get("direct_evolution_prediction", "")),
            })
        rows.sort(key=lambda r: r["id"])
        return rows
    # Fallback: empty rows for the 20 known IDs
    print(f"[WARN] '{path}' not found — generating an EMPTY template "
          f"for the {len(KNOWN_IDS)} known instance IDs. "
          f"Fill in operation/adl_type/request/reference/predictions manually, "
          f"or re-run notebook 08 to produce the JSON file first.")
    return [{"id": i, "operation": "", "adl_type": "", "request": "",
             "reference": "", "archpipeline_prediction": "",
             "direct_evolution_prediction": ""} for i in KNOWN_IDS]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="manual_review_20instances.json")
    parser.add_argument("--output", default="manual_review_20instances.csv")
    args = parser.parse_args()

    rows = load_source(args.input)
    columns = build_columns()

    with open(args.output, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            full_row = {c: "" for c in columns}
            full_row.update(row)
            writer.writerow(full_row)

    print(f"✅ Template written to: {args.output}")
    print(f"   {len(rows)} rows, {len(columns)} columns.")
    print(f"   Judgment columns accept: {ALLOWED_JUDGMENT_VALUES}")
    print(f"   Failure mode columns accept: {ALLOWED_FAILURE_MODES}")
    print(f"   See MANUAL_REVIEW_GUIDE.md for the full rubric before filling it in.")


if __name__ == "__main__":
    main()
