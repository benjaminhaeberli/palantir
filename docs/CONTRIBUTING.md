# Contribuer à Palantír RPG

Merci pour ton intérêt ! Palantír RPG est un jeu open source : les règles vivent dans ce dépôt et toute proposition est la bienvenue, qu'il s'agisse de corrections, de clarifications ou de nouvelles extensions.

## Types de contributions

| Type | Comment |
|---|---|
| **Coquille / typo** | PR directe sur le `.md` concerné. |
| **Clarification d'une règle existante** | PR avec une justification dans la description (exemple de partie, ambiguïté rencontrée). |
| **Nouvelle règle / mécanique** | Ouvre d'abord une *Issue* pour en discuter avant d'écrire la PR. |
| **Nouvelle extension** | Crée `src/content/extensions/<ton-slug>.md` avec le frontmatter requis. Ouvre une Issue d'abord pour valider le concept. |
| **Nouvelle ressource (table, fiche, outil)** | `src/content/ressources/<ton-slug>.md`. |
| **Setting / univers** | Pour l'instant, en attente d'une structure dédiée (v2.x). |

## Setup local

```bash
git clone git@github.com:benjaminhaeberli/palantir.git
cd palantir
npm install
npm run dev
```

Ouvrir <http://localhost:4321>, faire les modifs, vérifier le rendu, puis :

```bash
npm run build   # doit passer sans erreur
```

## Style éditorial

- **Français correct**, ponctuation française (espaces insécables avant `:` `;` `!` `?`).
- **Concision** : Palantír s'inspire de Knave, où chaque règle tient sur quelques lignes. Si tu écris un paragraphe de 10 lignes, demande-toi s'il peut tenir en 3.
- **Concepts du jeu en italique** lors d'une référence (`*Bravoure*`).
- **Termes techniques en gras** lors de leur définition.
- **Dé d'usage** : utiliser le caractère grec `Δ` (U+0394).
- **Pas d'emojis** dans le contenu du jeu.

## Frontmatter

Chaque fichier de contenu doit comporter :

```yaml
---
title: Mon titre
description: Une phrase qui résume.
order: 5
status: stable   # ou 'wip' ou 'draft'
---
```

Le champ `order` détermine la position dans la sidebar. Si tu insères un fichier au milieu, **renumérote la suite**.

## Process de PR

1. Fork → branche → commits clairs en français.
2. Ouvre la PR contre `main` (ou `develop` si l'auteur l'indique).
3. Décris brièvement *pourquoi* le changement (pas juste *quoi*).
4. Tag `@benjaminhaeberli` pour relecture si nécessaire.

## Code de conduite

Respect, bienveillance, écoute. Aucune contribution discriminatoire ou irrespectueuse ne sera acceptée.

Merci !
