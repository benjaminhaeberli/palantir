# Palantír RPG

> Héroïsme et bravoure, armés de 1d12 face au destin ⚔️

Site officiel et règles open source de **Palantír RPG**, un jeu de rôle OSR francophone générique, modulable et simple à prendre en main.

- **Site public** : <https://palantir-rpg.com>
- **Sources** : ce dépôt — toutes les règles vivent dans `src/content/` en Markdown.
- **Communauté** : les PRs sont les bienvenues, voir [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md).

## Stack

- [Astro 5](https://astro.build/) (SSG)
- Content Collections + MDX
- [Pagefind](https://pagefind.app/) pour la recherche
- Déploiement automatique sur GitHub Pages

## Charte visuelle

Strictement **monochrome** — noir, blanc et nuances de gris. Pas de teintes chaudes (parchemin, beige) ni d'accent coloré. Inspirée du minimalisme de *Shadowdark*. Le contraste sémantique passe par la typographie (poids, soulignement, texte barré), pas par la couleur.

## Quickstart

```bash
npm install
npm run dev          # http://localhost:4321
npm run build        # build + indexation Pagefind dans dist/
npm run preview      # prévisualisation du build
```

## Structure

```
src/
├── content/
│   ├── regles/         # Le livre de base (14 chapitres)
│   ├── extensions/     # Extensions officielles (Espoir, Gloire)
│   └── ressources/     # Outils, fiches, tables
├── layouts/
├── components/
├── pages/
└── styles/
```

Pour proposer un changement de règle, modifier un chapitre ou ajouter une extension, voir [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md).

Pour comprendre la roadmap (PDF print, i18n, intégration Scribe AI), voir [`docs/DEVELOPMENT_PLAN.md`](docs/DEVELOPMENT_PLAN.md).

## Licence

Le contenu du jeu sera publié sous une licence ouverte permettant la photocopie pour usage personnel et la publication de matériel compatible — voir la mention de licence dans le site lui-même (chapitre Notes de l'auteur / page d'accueil). Détails de licence définitive à confirmer.

Palantír RPG © Benjamin Haeberli, 2025.
