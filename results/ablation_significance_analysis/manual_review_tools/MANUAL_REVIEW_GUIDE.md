# Guide de notation — Revue manuelle architecturale (20 instances)

Référence : Réponse au Reviewer 2, Commentaire 5
Artefact attendu dans le dépôt : `results/manual_architectural_review_20instances/`

## ⚠️ Avant de commencer — point important

Votre lettre de réponse contient déjà des chiffres agrégés précis :

- **6/20 instances (30%)** entièrement correctes pour **les deux** configurations (ArchPipeline et Direct Evolution)
- **14/20** présentant au moins un problème architectural sur au moins une des deux configurations
- **0 cas** où une configuration est jugée correcte et l'autre non
- Parmi les 14 cas en échec : **8/14** = injection de token parasite, **3/14** = mutation non sollicitée (dont **1 cas**, Direct Evolution / DELETE_COMPONENT, où un bloc de propriétés entier est supprimé)

➡️ Ce gabarit sert à **formaliser par écrit la revue que vous avez déjà effectuée** pour produire ces chiffres, pas à refaire une revue indépendante à l'aveugle. Si en remplissant le tableau vous obtenez des totaux différents de ceux ci-dessus, il faudra soit revoir vos jugements pour qu'ils correspondent à l'analyse déjà décrite, soit corriger le manuscrit et la lettre de réponse pour refléter les vrais chiffres — ne laissez jamais les deux diverger, un reviewer peut recompter.

## Les 5 catégories de jugement (par instance, par configuration)

Pour **chaque** instance et **chaque** configuration (ArchPipeline / Direct Evolution), noter `Correct` / `Incorrect` / `N/A` :

| # | Catégorie | Question à se poser |
|---|---|---|
| 1 | **Identifier preservation** | Pour ADD/MODIFY : l'identifiant exact demandé dans la requête (nom du port, composant, connecteur) apparaît-il bien dans la sortie ? Pour DELETE : l'identifiant visé est-il bien absent ? |
| 2 | **Port/connector binding correctness** | Tous les bindings port↔connecteur↔composant restent-ils cohérents (pas de binding pointant vers un élément supprimé ou inexistant) ? |
| 3 | **Property value correctness** | Le nom et la valeur de propriété sont-ils exactement ceux attendus, sans modification non sollicitée d'une propriété non concernée ? (N/A si l'opération ne touche aucune propriété) |
| 4 | **Structural placement** | Le nouvel élément / élément modifié est-il positionné au bon endroit dans la hiérarchie, sans perturber une structure non concernée (séquences de transition, blocs d'attachement) ? |
| 5 | **Formalism-specific constraint satisfaction** | La sortie respecte-t-elle les règles de bonne formation du formalisme (ACME ou AADL) — mots-clés corrects, accolades équilibrées, pas de fuite de mot-clé d'un formalisme vers l'autre ? |

**`fully_correct`** = `Yes` uniquement si les 5 catégories sont `Correct` (un `N/A` ne bloque pas).

## Taxonomie des modes d'échec (à remplir seulement si `fully_correct = No`)

Utilisez exactement ces valeurs (vocabulaire contrôlé, pour rester cohérent avec le texte déjà soumis) :

- `spurious_token_injection` — un caractère ou token isolé, parasite, apparaît entre deux lignes ADL ; pas de sens sémantique ; artefact de décodage.
- `unrelated_mutation` — l'opération demandée est correctement effectuée, mais un identifiant/port/propriété/binding non concerné est modifié ailleurs dans la sortie, sans que cela ait été demandé.
- `dropped_block` — un bloc entier (ex. bloc de propriétés) est silencieusement supprimé alors qu'il n'était pas visé par la requête. Cas particulier et plus sévère de `unrelated_mutation` — n'utilisez cette étiquette que pour ce cas précis (Direct Evolution, DELETE_COMPONENT).
- `other` — tout autre problème non couvert ci-dessus ; décrivez-le dans la justification.

## Colonnes du fichier

| Colonne | Contenu |
|---|---|
| `id` | ID positionnel de l'instance dans le test set (les 20 IDs sont déjà fixés par votre échantillonnage stratifié seed=42) |
| `operation`, `adl_type` | Métadonnées de l'instance |
| `request`, `reference` | Requête en langage naturel et cible de référence |
| `archpipeline_prediction`, `direct_evolution_prediction` | Sorties des deux modèles |
| `arch_*` (5 colonnes) | Jugements pour ArchPipeline |
| `arch_fully_correct`, `arch_failure_mode`, `arch_justification` | Synthèse + justification courte pour ArchPipeline |
| `de_*` (5 colonnes) | Jugements pour Direct Evolution |
| `de_fully_correct`, `de_failure_mode`, `de_justification` | Synthèse + justification courte pour Direct Evolution |
| `rater`, `review_date` | Qui a noté, quand (traçabilité — utile si un co-auteur fait une seconde passe) |

## Étapes pratiques

1. Exécutez `build_review_template.py` (fourni) : il lit `manual_review_20instances.json` (déjà produit par votre notebook 08) et génère automatiquement `manual_review_20instances.csv` avec les colonnes de données déjà remplies (id, operation, adl_type, request, reference, prédictions) — vous n'avez **que les colonnes de jugement** à compléter à la main.
2. Ouvrez le CSV dans Excel ou Google Sheets, remplissez les jugements ligne par ligne.
3. Exportez/sauvegardez en `.csv` (et idéalement aussi en `.json` pour cohérence avec les autres artefacts du dépôt).
4. Lancez `validate_manual_review.py` sur le fichier complété : il recalcule les agrégats et les compare aux chiffres de la lettre de réponse.
5. Placez le résultat final dans `results/manual_architectural_review_20instances/`.
