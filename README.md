# Palantír RPG

> Héroïsme et bravoure, armés de 1d12 face au destin.

**Palantír RPG** est un système de jeu de rôle OSR générique, francophone et open source. Minimaliste et modulable : 5 attributs, une mécanique centrale (1d12 + dés de bravoure), pas de classes. Conçu pour être joué en quelques minutes d'explication et adapté à n'importe quel univers médiéval-fantastique.

- **Site officiel** : [palantir-rpg.com](https://palantir-rpg.com) — les règles complètes, lisibles en ligne
- **Licence** : [CC BY 4.0](LICENSE.md) — libre d'utilisation, y compris commerciale, avec attribution

---

## Matériel compatible

Vous pouvez créer et **vendre** des suppléments basés sur ce système (aventures, listes d'atouts, peuples, monstres, settings…). Mentionnez simplement :

> *« Compatible avec Palantír RPG de Benjamin Haeberli — [palantir-rpg.com](https://palantir-rpg.com) »*

Le nom **Palantír RPG** et le logo officiel sont réservés. Voir [`LICENSE.md`](LICENSE.md) pour le détail.

---

## Contribuer aux règles

Les contributions sont les bienvenues — corrections, clarifications, nouvelles extensions. Voir [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md) pour le processus détaillé.

En résumé :
- **Typo / coquille** → PR directe
- **Clarification de règle** → PR avec justification
- **Nouvelle mécanique** → Issue d'abord, PR ensuite

---

## Avis aux développeurs

Vous voulez adapter les règles à votre propre univers, corriger une typo ou héberger votre propre version du site ? Les sources sont là pour ça.

### Prérequis

- [Node.js](https://nodejs.org/) ≥ 20
- `npm` (inclus avec Node)

### Installation

```bash
git clone https://github.com/benjaminhaeberli/palantir.git
cd palantir
npm install
npm run dev        # → http://localhost:4321
```

### Modifier les règles

Tout le contenu du jeu vit dans `src/content/` en Markdown :

```
src/content/
├── regles/         # Chapitres du livre de base (01-introduction.md, etc.)
├── extensions/     # Extensions officielles (espoir-et-tourment.md, etc.)
├── conseils-mj/    # Conseils pour les maîtres de jeu
└── ressources/     # Outils, fiches, tables aléatoires
```

Chaque fichier a un frontmatter minimal :

```yaml
---
title: Combat
description: Initiative libre, actions et défense.
order: 13          # Détermine la position dans la sidebar
status: stable     # ou 'wip' (badge WIP affiché) ou 'draft'
---
```

### Adapter à votre univers

Pour publier votre propre SRD ou livre de règles :

1. Forkez ce dépôt
2. Remplacez le contenu de `src/content/regles/` par vos propres règles
3. Ajustez les variables CSS dans `src/styles/global.css` (couleurs, typographie)
4. Mettez à jour `astro.config.mjs` avec votre propre domaine
5. Déployez sur GitHub Pages, Netlify, Vercel ou votre propre serveur

### Build et déploiement

```bash
npm run build      # Build Astro + indexation Pagefind → dist/
npm run preview    # Prévisualiser le build final
```

Le site est un **site statique** (aucun backend, aucune base de données). Le dossier `dist/` peut être déposé sur n'importe quel hébergement.

Le déploiement sur GitHub Pages se fait automatiquement à chaque push sur `main` via `.github/workflows/deploy.yml`.

### Stack technique

| Outil | Rôle |
|---|---|
| [Astro 5](https://astro.build/) | Framework SSG |
| Content Collections + MDX | Contenu structuré en Markdown |
| [Pagefind](https://pagefind.app/) | Recherche full-text côté client |
| GitHub Pages | Hébergement |

---

## Licence

**[CC BY 4.0](LICENSE.md)** — Palantír RPG © Benjamin Haeberli, 2025.
