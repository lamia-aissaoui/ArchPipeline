# results/ — guide de lecture

Ce dossier contient les fichiers de résultats bruts (JSON/CSV) qui servent de preuve
vérifiable aux affirmations de la lettre de réponse aux reviewers. Tous les noms de
fichiers ci-dessous ont été **confirmés contre les vraies sorties d'exécution** (logs
Colab et captures d'écran du Drive), pas seulement déduits du code — plusieurs noms
supposés au départ se sont révélés incorrects et ont été corrigés.

---

## `comprehension_backbone_selection/` — issu de `04_comprehension_finetuning.ipynb`

### `recap_global.json`
- **Contenu** : ré-évaluation unifiée des 6 backbones (T5-base, CodeT5-base, UniXcoder, Flan-T5-base, CodeT5+770M, BART-large) avec la même suite de métriques (EM, BLEU, ROUGE-1/2/L, METEOR, BERT-F1).
- **Sert à** : source directe du **Tableau 1**.
- **⚠️ Ne pas confondre avec** les fichiers `results_{model_name}.json` sauvegardés pendant l'entraînement de chaque modèle — ceux-ci utilisent un calcul de métriques potentiellement légèrement différent d'un modèle à l'autre et ne doivent pas être utilisés comme source.

### `sensitivity_backbone_selection.json`
- **Contenu** : test de robustesse du classement des 6 backbones à différents schémas de pondération des métriques.
- **Sert à** : justifier que CodeT5-base n'a pas été choisi arbitrairement.

---

## `evolution_finetuning/` — issu de `05_Evolution_Finetuning.ipynb`

5 configurations, chacune dans son propre sous-dossier (à reproduire tel quel) :

| Fichier | Sous-dossier | Configuration |
|---|---|---|
| `resultats_CodeT5base_StratA_FullFT.json` | `evo_CodeT5base_fullFT/` | CodeT5-base, Full FT — **modèle retenu pour ArchPipeline** |
| `resultats_CodeT5base_StratB_FrozenEnc.json` | `evo_CodeT5base_frozenEnc/` | CodeT5-base, Frozen Encoder |
| `resultats_CodeT5plus_StratA_FullFT.json` | `evo_CodeT5plus_fullFT/` | CodeT5+ 770M, Full FT |
| `resultats_CodeT5plus_StratB_FrozenEnc.json` | `evo_CodeT5plus_frozenEnc/` | CodeT5+ 770M, Frozen Encoder |
| `resultats_Ablation_DirectEvolution_CodeT5base_FullFT.json` | `evo_ablation_DirectEvolution_CodeT5base_FullFT/` | Ablation — Direct Evolution (sans phase 1) |

Plus, à la racine de ce dossier :

### `sensitivity_analysis_weights.json`
- **Contenu** : robustesse du classement des 5 configurations à différents schémas de pondération.

### `evolution_selection_finale_v2.json`
- **Contenu** : rapport de sélection officiel du modèle final (CodeT5-base StratA).
- **Note** : le print associé mentionne "ArchAgent" / "Module 3" / "Module 5" — noms de code internes antérieurs au renommage du projet en "ArchPipeline". Sans impact sur les résultats.

---

## `paired_comparison_20/` — issu de la **dernière section** de `05_Evolution_Finetuning.ipynb`

> Cette analyse répond au Reviewer 2, Commentaire 2. Elle ne vient pas d'un notebook séparé
> ("07_Paired_Comparison_20_Instances.ipynb" n'existe pas comme artefact réel — voir
> `REPRODUCIBILITY.md`) mais de la cellule finale de `05_Evolution_Finetuning.ipynb`,
> exécutée dans son contexte normal (modèle déjà chargé en mémoire).

### `resultats_CodeT5base_StratA_PAIRED20.json`, `sampled_20_instance_ids.json`, `archpipeline_scores_n20_paired.json`, `archpipeline_scores_n120_full.json`, `comparison_n120_vs_n20.json` (+ `.txt`)
- **Contenu** : ré-évaluation d'ArchPipeline sur les mêmes 20 instances stratifiées (seed=42, IDs 0,5,6,8,15,17,18,21,22,25,26,36,41,44,46,86,88,102,114,119) utilisées pour les baselines LLM.
- **Sert à** : source de la ligne ArchPipeline du **Tableau 5** — **vérifié mot pour mot** : EM=0.3000, BLEU=0.7948, ROUGE-L=0.9614, METEOR=0.9406, BERT-F1=0.9996, identiques au manuscrit.

---

## `fewshot_baselines/` — issu de `06_FewShot_Comparison_LLMs.ipynb`

### `fewshot_new_results.json`
- **Contenu** : résultats des 6 baselines LLM (Llama-3.1-8B, GPT-OSS-20B, Qwen3-32B, Llama-3.3-70B, Llama-4-Scout-17B, GPT-OSS-120B) en 1-shot sur n=20, avec IC95% bootstrap (B=2000, seed=42).
- **Sert à** : source des lignes LLM du **Tableau 5** — **vérifié mot pour mot** contre le manuscrit, les 6 modèles × 5 métriques correspondent exactement.
- **⚠️ Important** : un run antérieur (`resultats_baselines_vs_pipeline.json`) a produit des chiffres différents pour les mêmes modèles (ex. Llama-3.3-70B EM=0.15 au lieu de 0.0998) — probablement dû à la non-déterminisme de l'API Groq (versions de modèle non figées côté fournisseur). **Ce fichier ne doit pas être ajouté au dépôt** ; seul `fewshot_new_results.json` est publié, avec une note de transparence dans le README sur cette limite des baselines via API.

---

## `ablation_significance_analysis/` — issu de `07_Ablation_Significance_Analysis.ipynb` (ancien notebook 08, renommé)

Confirmé directement par capture d'écran du dossier Drive — 8 fichiers :

| Fichier | Sert à |
|---|---|
| `per_instance_scores.json` | Scores par instance (n=120), ArchPipeline vs Direct Evolution — base de tous les tests statistiques |
| `significance_results.json` | Wilcoxon signé-rang + IC bootstrap par métrique — **Tableau 6**, réponse R2-C4 |
| `qualitative_differences.json` | Instances où les deux modèles divergent, prédictions côte à côte (⚠️ le code suggérait `qualitative_differing_cases.json` — le vrai nom est `qualitative_differences.json`) |
| `operational_precision_strict_vs_original.json` (+ `.txt`) | Précision opérationnelle "type" vs "stricte" par opération — réponse R2-C5, montre la faiblesse d'ADD_COMPONENT (~0.40) |
| `manual_review_20instances.json` | Extraction brute des 20 instances pour revue manuelle — **réponse R2-C5** |
| `add_component_all_20_cases.json` | 20 instances ADD_COMPONENT avec score EM par instance (8/20 = 0.40, confirmé) — **Tableau 8**, réponse R2-C6 |
| `SUMMARY.txt` | Résumé lisible en clair (fichier bonus non anticipé par le code, à garder) |

### ⚠️ Deux fichiers de ce dossier restent incomplets

- **`manual_review_20instances.json`** : ne contient encore aucun jugement humain (colonnes `arch_*`/`de_*` de `MANUAL_REVIEW_GUIDE.md` à remplir — voir `manual_review_20instances_TO_FILL.csv`).
- **`add_component_all_20_cases.json`** : les scores EM sont corrects, mais les catégories d'échec (incohérence contextuelle, déplacement structurel, etc.) décrites pour le Tableau 8 ne sont pas encore des champs explicites — à ajouter selon le même principe que la revue manuelle.

---

## Tableau récapitulatif

| Fichier | Notebook source | Tableau / Section du papier | Commentaire reviewer | Statut |
|---|---|---|---|---|
| `recap_global.json` | 04 | Tableau 1 | R1-C7/C9 | ✅ |
| `sensitivity_backbone_selection.json` | 04 | Section 4.1 (méthodologie) | R1-C7/C9 | ✅ |
| `resultats_*StratA/StratB*.json` (×4) + ablation | 05 | Tableaux 6/7 | R1-C7/C9, R2-C4 | ✅ |
| `sensitivity_analysis_weights.json`, `evolution_selection_finale_v2.json` | 05 | Section 4.2 (méthodologie) | R1-C7/C9 | ✅ |
| `resultats_CodeT5base_StratA_PAIRED20.json` + fichiers associés | 05 (section finale) | Tableau 5 (ligne ArchPipeline) | R2-C2 | ✅ vérifié |
| `fewshot_new_results.json` | 06 | Tableau 5 (lignes LLM) | R2-C2, R2-C3 | ✅ vérifié |
| `per_instance_scores.json`, `significance_results.json` | 07 | Tableau 6 | R2-C4 | ✅ |
| `qualitative_differences.json` | 07 | Tableau 6/7 (support qualitatif) | R2-C4 | ✅ |
| `operational_precision_strict_vs_original.*` | 07 | Section 4.4 | R2-C5 | ✅ |
| `manual_review_20instances.json` | 07 | — (jugements à ajouter) | R2-C5 | ⚠️ à compléter |
| `add_component_all_20_cases.json` | 07 | Tableau 8 | R2-C6 | ⚠️ catégories à ajouter |
| `SUMMARY.txt` | 07 | — | — | ✅ bonus |
