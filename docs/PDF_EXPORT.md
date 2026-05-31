# Export PDF — notes & roadmap

L'objectif à terme : générer un **PDF A5 print-ready** à partir des mêmes sources Markdown que le site web, sans dupliquer le contenu. Cette feature n'est pas en v1 — ce document trace l'approche envisagée.

## Cibles

- **A5 portrait** (148 × 210 mm) — cohérent avec le format original du jeu.
- **2 colonnes** sur les chapitres denses (règles), 1 colonne sur les pages aérées (notes auteur, intro).
- **Polices embarquées** : Grenze (titres), Crimson Pro (body) — déjà chargées sur le site.
- **Numérotation de page** automatique, table des matières en début, index optionnel.
- **Liens internes** cliquables dans le PDF (références croisées entre règles).

## Approche envisagée : Paged.js

[Paged.js](https://pagedjs.org/) est un polyfill du module CSS *Paged Media* (CSS Print). Avantages :

- Tout en CSS, contrôle fin de la mise en page d'impression.
- Fonctionne dans Chromium → peut être driveable via Puppeteer.
- Couvre nativement : marges, headers/footers, breaks de page, références, TOC auto, compteurs de page.

### Workflow envisagé

```
1. npm run build          # build du site web normalement
2. node scripts/pdf.mjs   # lance Puppeteer sur une route /print dédiée
3. Puppeteer ouvre dist/print/index.html (contenu concaténé, single-page)
4. Paged.js (chargé dans cette page) paginate selon print.css
5. Puppeteer fait page.pdf({ format: 'A5', preferCSSPageSize: true })
6. → dist/palantir-rpg.pdf
```

### Fichiers à créer

- `src/pages/print.astro` : route qui concatène toutes les `regles/`, `extensions/`, `ressources/` en un seul long document.
- `src/styles/print.css` : règles `@page`, breaks, colonnes, headers/footers.
- `scripts/pdf.mjs` : script Node qui lance Puppeteer + Paged.js sur la route `/print`.
- Ajout `npm run pdf` au `package.json`.

## Alternatives écartées

- **Pandoc + LaTeX** : très puissant mais le contenu Markdown utilise déjà des features Astro/MDX (composants, frontmatter typé) que Pandoc ne comprend pas sans pipeline custom.
- **markdown-it + custom layout** : ré-implémenter les composants Astro côté print serait du travail dupliqué.
- **Typst** : élégant mais demanderait de réécrire le contenu en `.typ`.

Paged.js gagne parce que **le même HTML** sert le web ET le PDF, avec juste un CSS print différent.

## Considérations

- **Images & illustrations** : à terme, le jeu aura des illustrations. Prévoir des résolutions élevées (300 DPI) pour l'impression. Stockées dans `public/illustrations/`.
- **Polices** : Google Fonts → ne pas dépendre du réseau au moment du build PDF. Solution : self-host les `.woff2` dans `public/fonts/` et les `@font-face` dans `print.css`.
- **Index** : Paged.js supporte les `target-counter()` CSS, mais un index thématique demandera des `<span data-index="...">` semés dans le contenu. À évaluer.
- **Versionnage** : intégrer le numéro de version du jeu (alpha, 1.0…) en page de garde, lu depuis `package.json`.

## Quand attaquer ?

Après la v1.1 (sections WIP comblées). Inutile de figer la mise en page tant que le contenu bouge.
