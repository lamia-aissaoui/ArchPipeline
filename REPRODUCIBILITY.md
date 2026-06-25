# Reproducibility checklist — mapping response-letter claims to repository artifacts

This file cross-references every reproducibility claim made in the response letter
to reviewers against its actual location in this repository, using filenames
**confirmed against real Google Drive output**, not just notebook source code
(several discrepancies between code-assumed names and real saved files were found
and corrected during preparation — see notes marked ⚠️ below).

Status legend: ✅ present and verified · ⚠️ partially present / needs action · ❌ not yet created

| # | Claim in response letter | Reviewer comment | Artifact | Status |
|---|---|---|---|---|
| 1 | Exact train/val/test splits, both datasets | R1-C7, R1-C9 | Zenodo records (DOI 10.5281/zenodo.20508689, 10.5281/zenodo.20508742) — `train.jsonl`/`val.jsonl`/`test_v2.jsonl` already split, no local copy needed | ✅ |
| 2 | Preprocessing / diversity-filtering pipeline | R1-C7, R1-C9 | `notebooks/01_Comprehension_dataset.ipynb`, `02_Evolution_dataset.ipynb`, `03_testset_cleaning.ipynb` | ✅ |
| 3 | Backbone selection (6 models, comprehension phase) | R1-C7, R1-C9 | `notebooks/04_comprehension_finetuning.ipynb` → `results/comprehension_backbone_selection/recap_global.json` (unified re-evaluation, source of Table 1) + `sensitivity_backbone_selection.json` (ranking robustness check) | ✅ |
| 4 | Training commands & hyperparameters (evolution model + ablation) | R1-C7, R1-C9 | `notebooks/05_Evolution_Finetuning.ipynb` | ✅ inline |
| 5 | Random seed = 42 used consistently | R1-C7, R1-C9 | Verified across notebooks 01, 02, 04, 05, 06, 07 | ✅ |
| 6 | Model checkpoints / checkpoint identifiers | R1-C7, R1-C9 | `README.md` → 11 HuggingFace Hub repos under [lamia24](https://huggingface.co/lamia24) | ✅ all 6 comprehension + 5 evolution checkpoints uploaded and linked |
| 7 | Metric scripts (EM, BLEU, ROUGE-1/2/L, METEOR, BERT-F1, Vsyn, Pop, Scomp) | R1-C7, R1-C9 | Inline in notebooks 04, 05, 07 | ✅ present, slightly duplicated across notebooks — acceptable, not blocking |
| 8 | Evolution model selection across 5 configurations (4 strategies + ablation) | R1-C7, R1-C9 | `results/evolution_finetuning/`: `resultats_CodeT5base_StratA_FullFT.json`, `resultats_CodeT5base_StratB_FrozenEnc.json`, `resultats_CodeT5plus_StratA_FullFT.json`, `resultats_CodeT5plus_StratB_FrozenEnc.json`, `resultats_Ablation_DirectEvolution_CodeT5base_FullFT.json`, `sensitivity_analysis_weights.json`, `evolution_selection_finale_v2.json` | ✅ all 7 files confirmed by real Drive logs |
| 9 | Bootstrap / significance scripts (Wilcoxon, B=2000, seed=42) | R1-C7, R2-C4 | `notebooks/07_Ablation_Significance_Analysis.ipynb` → `results/ablation_significance_analysis/significance_results.json`, `per_instance_scores.json` | ✅ confirmed against real Drive folder listing |
| 10 | Baseline prompts, system prompt, decoding params, API model IDs | R1-C7, R2-C3 | `notebooks/06_FewShot_Comparison_LLMs.ipynb` (inline) | ✅ |
| 11 | No API key leaked in shared notebook | (security) | `06_FewShot_Comparison_LLMs.ipynb` | ✅ verified — key read via Colab userdata/getpass, never hardcoded |
| 12 | LLM baseline results, 6 models, n=20, with 95% bootstrap CI | R2-C3 | `results/fewshot_baselines/fewshot_new_results.json` | ✅ **verified word-for-word against Table 5** of the manuscript (all 6 models, all 5 metrics match exactly) |
| 12b | — | — | ⚠️ An earlier run (`resultats_baselines_vs_pipeline.json`, 4 models only) produced **different, non-matching** point estimates for the same models (e.g. Llama-3.3-70B EM 0.1500 vs. 0.0998). This file is a superseded intermediate run and **must not** be added to the repository — only `fewshot_new_results.json` should be published. |
| 13 | Paired re-evaluation of ArchPipeline on same 20 instances (Table 5, ArchPipeline row) | R2-C2 | `notebooks/05_Evolution_Finetuning.ipynb` (final section) → `results/paired_comparison_20/`: `resultats_CodeT5base_StratA_PAIRED20.json`, `sampled_20_instance_ids.json`, `archpipeline_scores_n20_paired.json`, `archpipeline_scores_n120_full.json`, `comparison_n120_vs_n20.json`, `comparison_n120_vs_n20.txt` | ✅ **verified**: real execution output matches Table 5's footnoted ArchPipeline row exactly (EM=0.3000, BLEU=0.7948, ROUGE-L=0.9614, METEOR=0.9406, BERT-F1=0.9996) |
| 13b | — | — | ⚠️ This analysis was previously assumed to live in a separate, independently-executed notebook ("07_Paired_Comparison_20_Instances.ipynb"). That separate notebook was never actually run — it was a reconstruction, not a validated artifact, and has been **discarded**. The real, working version is the cell at the end of `05_Evolution_Finetuning.ipynb`, confirmed by real execution output. |
| 14 | Stratified 20-instance subset IDs (seed=42) | R2-C2, R2-C3 | `results/paired_comparison_20/sampled_20_instance_ids.json` | ✅ |
| 15 | Identifier-level operational precision (type vs. strict) | R2-C5 | `results/ablation_significance_analysis/operational_precision_strict_vs_original.json` (+ `.txt`) | ✅ confirmed against real Drive folder listing |
| 16 | ADD_COMPONENT failure log, all 20 instances, per-instance category | R2-C6 | `results/ablation_significance_analysis/add_component_all_20_cases.json` | ✅ completed with verified categories (7 context_inconsistency, 3 structural_simplification, 1 structural_displacement, 1 truncation) — corrected from the letter's original 3/1 split between the latter two categories |
| 17 | **Manual architectural review, 20 instances, 5 judgment categories** | R2-C5 | `results/ablation_significance_analysis/manual_review_20instances.json` | ✅ completed — 6/20 fully correct for both configurations, 14/20 with at least one issue, 0 disagreement between configurations. Response letter and manuscript Table 8 surrounding text updated to report verified failure-mode proportions. |
| 18 | Qualitative differing cases between ArchPipeline and Direct Evolution | R2-C4 (support) | `results/ablation_significance_analysis/qualitative_differences.json` | ✅ confirmed (code assumed `qualitative_differing_cases.json` — real filename is `qualitative_differences.json`) |
| 19 | Related-work positioning vs. 2025-2026 agentic methods | R2-C1 | Manuscript Section 2.5 only (no code artifact expected) | ✅ N/A for repo |

## Before publishing the repository — action items

1. **Decouple notebooks from Google Drive**: replace hardcoded `/content/drive/...` paths with a configurable `BASE_DIR`/`EVO_DIR` variable, and document the expected folder layout in the README.
2. **Pin dependency versions**: run `pip freeze` in the working Colab session and commit it alongside `requirements.txt`.
3. **Add model cards** to the 11 HuggingFace Hub checkpoints (currently showing "No model card") — optional polish, not blocking.
