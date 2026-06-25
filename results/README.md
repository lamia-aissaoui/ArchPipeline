# results/ — file guide

This folder contains the raw result files (JSON/CSV) that serve as verifiable
evidence for the claims made in the response letter to reviewers. All filenames
below have been **confirmed against real execution output** (Colab logs and Drive
screenshots), not merely inferred from notebook source code — several initially
assumed names turned out to be incorrect and were corrected accordingly.

---

## `comprehension_backbone_selection/` — from `04_comprehension_finetuning.ipynb`

### `recap_global.json`
- **Content**: unified re-evaluation of the 6 backbones (T5-base, CodeT5-base, UniXcoder, Flan-T5-base, CodeT5+770M, BART-large) using the same metric suite (EM, BLEU, ROUGE-1/2/L, METEOR, BERT-F1).
- **Used for**: direct source of **Table 1**.
- ** Do not confuse with** the `results_{model_name}.json` files saved during each model's training run — those may use slightly inconsistent metric computation across models and should not be used as the source.

### `sensitivity_backbone_selection.json`
- **Content**: robustness check of the 6-backbone ranking against different metric-weighting schemes.
- **Used for**: justifying that CodeT5-base was not chosen arbitrarily.

---

## `evolution_finetuning/` — from `05_Evolution_Finetuning.ipynb`

5 configurations, each in its own subfolder (reproduced as-is):

| File | Subfolder | Configuration |
|---|---|---|
| `resultats_CodeT5base_StratA_FullFT.json` | `evo_CodeT5base_fullFT/` | CodeT5-base, Full FT — **model selected for ArchPipeline** |
| `resultats_CodeT5base_StratB_FrozenEnc.json` | `evo_CodeT5base_frozenEnc/` | CodeT5-base, Frozen Encoder |
| `resultats_CodeT5plus_StratA_FullFT.json` | `evo_CodeT5plus_fullFT/` | CodeT5+ 770M, Full FT |
| `resultats_CodeT5plus_StratB_FrozenEnc.json` | `evo_CodeT5plus_frozenEnc/` | CodeT5+ 770M, Frozen Encoder |
| `resultats_Ablation_DirectEvolution_CodeT5base_FullFT.json` | `evo_ablation_DirectEvolution_CodeT5base_FullFT/` | Ablation — Direct Evolution (no Phase 1 transfer) |

Plus, at the root of this folder:

### `sensitivity_analysis_weights.json`
- **Content**: robustness of the 5-configuration ranking against different metric-weighting schemes.

### `evolution_selection_finale_v2.json`
- **Content**: official selection report for the final model (CodeT5-base StratA).
- **Note**: the associated console output references "ArchAgent" / "Module 3" / "Module 5" — internal code names predating the project's renaming to "ArchPipeline". No impact on the results themselves.

---

## `paired_comparison_20/` — from the **final section** of `05_Evolution_Finetuning.ipynb`

> This analysis responds to Reviewer 2, Comment 2. It does not come from a separate
> notebook ("07_Paired_Comparison_20_Instances.ipynb" does not exist as a real,
> independently-executed artifact — see `REPRODUCIBILITY.md`) but from the final
> cell of `05_Evolution_Finetuning.ipynb`, run in that notebook's own session
> (with the model already loaded in memory).

### `resultats_CodeT5base_StratA_PAIRED20.json`, `sampled_20_instance_ids.json`, `archpipeline_scores_n20_paired.json`, `archpipeline_scores_n120_full.json`, `comparison_n120_vs_n20.json` (+ `.txt`)
- **Content**: re-evaluation of ArchPipeline on the same 20 stratified instances (seed=42, IDs 0,5,6,8,15,17,18,21,22,25,26,36,41,44,46,86,88,102,114,119) used for the LLM baselines.
- **Used for**: source of the ArchPipeline row in **Table 5** — **verified word-for-word**: EM=0.3000, BLEU=0.7948, ROUGE-L=0.9614, METEOR=0.9406, BERT-F1=0.9996, matching the manuscript exactly.

---

## `fewshot_baselines/` — from `06_FewShot_Comparison_LLMs.ipynb`

### `fewshot_new_results.json`
- **Content**: results for the 6 LLM baselines (Llama-3.1-8B, GPT-OSS-20B, Qwen3-32B, Llama-3.3-70B, Llama-4-Scout-17B, GPT-OSS-120B) under 1-shot prompting on n=20, with 95% bootstrap CI (B=2000, seed=42).
- **Used for**: source of the LLM rows in **Table 5** — **verified word-for-word** against the manuscript; all 6 models × 5 metrics match exactly.
- **⚠️ Important**: an earlier run (`resultats_baselines_vs_pipeline.json`) produced different point estimates for the same models (e.g. Llama-3.3-70B EM=0.15 instead of 0.0998) — most likely due to non-determinism in the Groq API (model versions are not version-frozen on the provider's side). **This file must not be added to the repository**; only `fewshot_new_results.json` is published, with a transparency note in the main README about this limitation of API-based baselines.

---

## `ablation_significance_analysis/` — from `07_Ablation_Significance_Analysis.ipynb` (formerly notebook 08, renumbered)

Confirmed directly via a screenshot of the Drive folder — 8 files:

| File | Used for |
|---|---|
| `per_instance_scores.json` | Per-instance scores (n=120), ArchPipeline vs. Direct Evolution — basis for all statistical tests |
| `significance_results.json` | Wilcoxon signed-rank + bootstrap CI per metric — **Table 6**, response to R2-C4 |
| `qualitative_differences.json` | Instances where the two models diverge, predictions side by side (⚠️ the code suggested `qualitative_differing_cases.json` — the real filename is `qualitative_differences.json`) |
| `operational_precision_strict_vs_original.json` (+ `.txt`) | "Type-level" vs. "strict" operational precision per operation — response to R2-C5, shows the ADD_COMPONENT weakness (~0.40) |
| `manual_review_20instances.json` | Raw extraction of the 20 instances for manual review — **response to R2-C5** |
| `add_component_all_20_cases.json` | 20 ADD_COMPONENT instances with per-instance EM score (8/20 = 0.40, confirmed) — **Table 8**, response to R2-C6 |
| `SUMMARY.txt` | Plain-text summary (bonus file, not anticipated from the code, worth keeping) |

### ⚠️ Two files in this folder remain incomplete

- **`manual_review_20instances.json`**: contains no human judgments yet (the `arch_*`/`de_*` columns from `MANUAL_REVIEW_GUIDE.md` still need to be filled in — see `manual_review_20instances_TO_FILL.csv`).
- **`add_component_all_20_cases.json`**: EM scores are correct, but the failure categories (context inconsistency, structural displacement, etc.) described for Table 8 are not yet explicit fields — to be added following the same principle as the manual review.

---

## Summary table

| File | Source notebook | Paper table / section | Reviewer comment | Status |
|---|---|---|---|---|
| `recap_global.json` | 04 | Table 1 | R1-C7/C9 | ✅ |
| `sensitivity_backbone_selection.json` | 04 | Section 4.1 (methodology) | R1-C7/C9 | ✅ |
| `resultats_*StratA/StratB*.json` (×4) + ablation | 05 | Tables 6/7 | R1-C7/C9, R2-C4 | ✅ |
| `sensitivity_analysis_weights.json`, `evolution_selection_finale_v2.json` | 05 | Section 4.2 (methodology) | R1-C7/C9 | ✅ |
| `resultats_CodeT5base_StratA_PAIRED20.json` + related files | 05 (final section) | Table 5 (ArchPipeline row) | R2-C2 | ✅ verified |
| `fewshot_new_results.json` | 06 | Table 5 (LLM rows) | R2-C2, R2-C3 | ✅ verified |
| `per_instance_scores.json`, `significance_results.json` | 07 | Table 6 | R2-C4 | ✅ |
| `qualitative_differences.json` | 07 | Table 6/7 (qualitative support) | R2-C4 | ✅ |
| `operational_precision_strict_vs_original.*` | 07 | Section 4.4 | R2-C5 | ✅ |
| `manual_review_20instances.json` | 07 | — (judgments to be added) | R2-C5 | ⚠️ incomplete |
| `add_component_all_20_cases.json` | 07 | Table 8 | R2-C6 | ⚠️ categories to be added |
| `SUMMARY.txt` | 07 | — | — | ✅ bonus |
