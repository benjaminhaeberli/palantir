# CLAUDE.md — Conventions pour l'assistance IA

> Ce fichier guide les assistants IA (Claude Code, Copilot, etc.) travaillant sur ce dépôt.
> Il documente aussi les conventions éditoriales utiles à tout contributeur humain.

## Nature du projet

Site statique **Astro** publiant les règles d'un JdR OSR francophone. Tout le contenu vit dans `src/content/` en Markdown. Le site est rebuild et redéployé sur GitHub Pages à chaque push sur `main`.

## Règles d'or

1. **Le contenu est en français.** Écris en français correct, soigné, avec ponctuation française (espaces insécables avant `:` `;` `!` `?`, guillemets `«` `»` ou typographiques `"` `"`). N'introduis pas d'anglicismes inutiles.
2. **Le ton est ludique mais clair.** Knave est la référence : précis, concis, jouable en quelques lignes.
3. **Ne casse pas les `order` du frontmatter.** Ils déterminent l'ordre dans la sidebar. Si tu insères un chapitre au milieu, renumérote la suite.
4. **Ne renomme pas un fichier `.md` sans raison.** Le slug devient l'URL publique.
5. **Tu peux ajouter des composants MDX** (`src/components/`) si une règle gagne à être stylisée (dé, encadré, table interactive), mais reste sobre.
6. **Charte visuelle strictement monochrome.** Uniquement noir, blanc et nuances de gris. **Pas de couleurs chaudes** (parchemin, crème, beige) ni d'accent coloré (rouge, vert, bleu). Les variables CSS de référence sont `--color-bg` (blanc), `--color-ink` (noir), `--color-muted` / `--color-border` (gris), `--color-subtle` (gris très clair pour secondary panels). Le contraste sémantique (réussite/échec) passe par le **typographique** (gras, soulignement, texte barré) plutôt que par la couleur.

## Frontmatter obligatoire

```yaml
---
title: Combat
description: Initiative libre, actions, manœuvres et défense.
order: 7
status: stable   # ou 'wip' ou 'draft'
---
```

- `status: wip` → badge rouge "WIP" rendu automatiquement à côté du titre et dans la sidebar.
- `status: draft` → badge gris, à terme sera caché en production.

## Où vit quoi

| Tu veux… | Tu touches… |
|---|---|
| Modifier une règle | `src/content/regles/*.md` |
| Ajouter une extension officielle | `src/content/extensions/*.md` |
| Ajouter un outil / table utilisable en jeu | `src/content/ressources/*.md` |
| Modifier le layout / la sidebar | `src/layouts/`, `src/components/Sidebar.astro` |
| Changer la typo, les couleurs | `src/styles/global.css` (variables CSS en haut du fichier) |
| Modifier la landing | `src/pages/index.astro` |
| Modifier le déploiement | `.github/workflows/deploy.yml`, `astro.config.mjs` |

## Conventions de contenu

- **Dé du destin** : `1d12` (ou `d12`).
- **Dé de bravoure** : `1d6` (ou `d6`).
- **Dé d'usage** : `Δ4`, `Δ6`, `Δ8`, `Δ10`. Utilise toujours le caractère `Δ` (delta majuscule grec, U+0394).
- **Attributs abrégés** : `FOR`, `DEX`, `CON`, `ESP`, `CHA` (majuscules, italiques).
- **Concepts du jeu** : en *italique* lors d'une référence (`*Bravoure*`, `*Endurance*`, `*Inconscient*`).
- **Termes techniques en gras** lors de leur première définition.

## Workflow git

- Branche par défaut de travail : `develop`.
- Branche de déploiement : `main` (push → GH Action → publish).
- **Ne pas pousser directement sur `main`** sans validation locale (`npm run build`).
- Tester localement avant de pousser : `npm run dev` + checker la page modifiée.

## Build & vérifs

```bash
npm run build   # build Astro + indexation Pagefind
npm run preview # vérifier le rendu final
```

Si `npm run build` échoue, c'est souvent :
- Une erreur de frontmatter (champ manquant ou typo) → vérifier le schéma dans `src/content.config.ts`.
- Un lien Markdown cassé.
- Un composant Astro qui attend une prop manquante.

## Hors scope (encore)

- Pas d'export PDF pour l'instant (voir `docs/PDF_EXPORT.md` pour la roadmap).
- Pas d'i18n (français uniquement en v1).
- Pas de dark mode.
- Pas de base de données ni de backend.

## Demande à l'utilisateur

- Avant d'inventer une mécanique de jeu, demande confirmation.
- Avant un refactor de plus de 3 fichiers, propose un plan court.
