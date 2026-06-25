# ArchPipeline

**A Two-Phase Transfer-Learning Framework for Software Architecture Comprehension and Evolution**

Lamia Aissaoui, Fadila Atil, Saida Gherbi, Sonia Achiri
*LISCO Laboratory, Badji Mokhtar-Annaba University & National Higher School of Technology and Engineering, Annaba, Algeria*

Submitted to *International Journal of Intelligent Engineering and Systems (IJIES)*.

---

## Overview

ArchPipeline is a two-phase transfer-learning framework that:
1. **Comprehension phase** — fine-tunes encoder-decoder backbones to generate natural language descriptions from ACME/AADL architecture specifications.
2. **Evolution phase** — initializes from the best comprehension checkpoint and fine-tunes a model to evolve ADL specifications in response to natural language change requests, across six atomic operations (ADD_PORT, MODIFY_PROPERTY, ADD_COMPONENT, DELETE_COMPONENT, ADD_CONNECTOR, DELETE_CONNECTOR).

Best configuration: **CodeT5-base, Strategy A (full fine-tuning)** — composite score 0.9431 on the full evolution test set (n=120), outperforming six one-shot LLM baselines (8B–120B parameters) on five structure-sensitive metrics under a sample-matched (n=20, paired) comparison.

## Repository structure

```
ArchPipeline/
├── notebooks/
│   ├── 01_Comprehension_dataset.ipynb       # Cleaning, annotation, augmentation, split
│   ├── 02_Evolution_dataset.ipynb           # Synthetic generation of 6 operations, split
│   ├── 03_testset_cleaning.ipynb            # Max-diversity test set reconstruction (Eq. 1)
│   ├── 04_comprehension_finetuning.ipynb    # 6 backbones, composite score selection
│   ├── 05_Evolution_Finetuning.ipynb        # 4 configs (2 backbones x 2 strategies) + ablation
│   │                                         # + paired 20-instance re-evaluation (final section,
│   │                                         #   Reviewer 2 response — see note below)
│   ├── 06_FewShot_Comparison_LLMs.ipynb     # 6 LLM baselines via Groq API, 1-shot, n=20
│   └── 07_Ablation_Significance_Analysis.ipynb  # Wilcoxon + bootstrap CI, identifier-level
│                                                  # precision, ADD_COMPONENT failure analysis
├── results/
│   ├── comprehension_backbone_selection/     # Notebook 04 outputs — Table 1 source
│   ├── evolution_finetuning/                 # Notebook 05 outputs — 5 configs + selection
│   ├── paired_comparison_20/                 # Notebook 05 (final section) — Table 5 ArchPipeline row
│   ├── fewshot_baselines/                    # Notebook 06 output — Table 5 LLM rows
│   └── ablation_significance_analysis/       # Notebook 07 outputs — Tables 6/7/8
├── checkpoints/                              # Links to hosted model weights (see below)
├── requirements.txt
├── REPRODUCIBILITY.md                        # Maps each reviewer response to its artifact
├── results_README.md                         # File-by-file guide to results/
└── LICENSE
```

> **Note on notebook numbering:** an earlier internal draft referenced an additional
> "07_Paired_Comparison_20_Instances.ipynb". That notebook was never an independently
> executed artifact — the corresponding analysis is the final section of
> `05_Evolution_Finetuning.ipynb` ("Paired Comparison on 20 Instances — Reviewer 2 Response"),
> run in that notebook's own session. It is documented here as part of notebook 05, not as
> a separate file, to avoid publishing code that was never independently validated.

## Datasets

Both datasets, **including the exact train/validation/test splits used in the paper**,
are permanently archived on Zenodo. No local copies are kept in this repository —
download directly from Zenodo:

- **Comprehension dataset**: https://doi.org/10.5281/zenodo.20508689
  `train.jsonl` (640), `val.jsonl` (80), `test.jsonl` (80, raw), `test_v2.jsonl`
  (66, Jaccard-filtered — used in all reported experiments), `dataset_full.jsonl`
  (1,092, before AADL/ACME rebalancing).
- **Evolution dataset**: https://doi.org/10.5281/zenodo.20508742
  `train.jsonl` (1,754), `val.jsonl` (220), `test.jsonl` (218, raw), `test_v2.jsonl`
  (120, Jaccard-filtered, 20 per operation — used in all reported experiments),
  `dataset_full.csv` (2,192).

`test_v2.jsonl` in each archive is the output of the max-diversity test-set
reconstruction (Eq. 1) implemented in `03_testset_cleaning.ipynb`.

## Model checkpoints

Trained checkpoints (6 comprehension backbones + 5 evolution configurations, including
the Direct Evolution ablation) are hosted on HuggingFace Hub:
- `<org>/archpipeline-comprehension-<backbone>` (6 repos)
- `<org>/archpipeline-evolution-<backbone>-<strategy>` (5 repos)

*(Replace the placeholders above with your actual HuggingFace Hub repo IDs once uploaded.)*

## Reproducing the results

1. Clone the repo and install dependencies: `pip install -r requirements.txt`
2. Download `train.jsonl` / `val.jsonl` / `test_v2.jsonl` from the two Zenodo records linked above.
3. Each notebook currently assumes a Google Colab environment with Google Drive mounted at a fixed path. **Before running locally**, edit the `BASE_DIR` / `EVO_DIR` variable at the top of each notebook to point to your local clone of this repository.
4. Run notebooks in numerical order (01 → 07); each consumes artifacts produced by the previous one. Expected runtime and hardware: single NVIDIA T4 GPU (15GB VRAM), as used in the original experiments.
5. To reproduce only the statistical analyses without retraining, download the checkpoints from HuggingFace Hub and start directly from notebook 06 or 07.

Random seed `42` is used consistently across all stratified sampling, train/val/test splitting, bootstrap resampling, and baseline subsampling procedures.

## LLM baseline reproduction — important caveat

Notebook `06_FewShot_Comparison_LLMs.ipynb` queries six LLMs through the Groq API rather
than locally-hosted, version-frozen checkpoints. **Re-running this notebook may not
reproduce the exact published numbers**, because the model provider can update served
weights, quantization, or serving infrastructure without notice — this is a known limitation
of API-based baselines, not a bug in the evaluation code. The authoritative values reported
in Table 5 are those in `results/fewshot_baselines/fewshot_new_results.json`; an earlier
run with different point estimates exists in the authors' working files but is intentionally
excluded from this repository to avoid presenting two inconsistent sets of baseline numbers.

A Groq API key is required (set as the Colab secret `GROQ_API_KEY`, or entered via prompt
when run outside Colab). Model identifiers, prompt template, decoding parameters
(temperature=0.0), and post-processing rules are documented inline in the notebook. No API
key is stored in this repository.

## Citation

If you use this code or data, please cite:

```
[Add full BibTeX entry once the paper is accepted / assigned a DOI]
```

## License

Code released under the [MIT License](LICENSE). Datasets are released separately on Zenodo under their own license terms (see Zenodo records). The accompanying manuscript is licensed under CC BY-SA 4.0.

## Contact

lamia.aissaoui@univ-annaba.dz / l.aissaoui@ensti-annaba.dz
