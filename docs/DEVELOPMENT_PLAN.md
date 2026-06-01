# Plan de développement — Palantír RPG

Roadmap vivante du projet. Mise à jour au fil des versions.

## v1.0 — Site public (en cours)

**Objectif** : publier les règles existantes en site statique navigable et indexable.

- [x] Bootstrap Astro + content collections + GH Pages
- [x] Migration intégrale du contenu du Google Doc en Markdown
- [x] Typographie Grenze / Crimson Pro
- [x] Layout SRD-like (sidebar + contenu + TOC)
- [ ] Recherche Pagefind branchée en UI (composant `Search.astro`)
- [ ] Acheter et brancher le domaine `palantir-rpg.com` (CNAME GitHub Pages)
- [ ] Première passe de relecture sur l'ensemble du contenu
- [ ] Page "Contribuer" pointant vers `CONTRIBUTING.md`

## v1.1 — Compléter les sections WIP

- [x] Simplifier **Atouts** : 8 atouts avec effet de base + effet renforcé (PB)
- [x] Compléter **Combat** : actions non-offensives, dégâts 1d6 uniformes, coup critique = blessure
- [x] Compléter **Bestiaire** : 8 créatures de référence (niveaux 1–6), mécanique blessures/niveau
- [ ] Compléter **Équipement** : liste complète d'armes/armures avec propriétés
- [ ] Compléter **Mésaventures** : tables inspirées de Knave/Shadowdark
- [ ] Compléter **Bestiaire** : étendre à 20–30 créatures
- [ ] Compléter **Sortilèges** : liste de référence

## v2.0 — Export PDF print-ready

Voir [`PDF_EXPORT.md`](PDF_EXPORT.md) pour le détail technique.

- [ ] Pipeline Paged.js ou Puppeteer pour générer un PDF A5
- [ ] Stylesheet `print.css` dédiée (mise en page 2 colonnes, marges A5, polices embarquées)
- [ ] Script `npm run pdf` qui produit `dist/palantir-rpg.pdf`
- [ ] Lien de téléchargement sur la landing

## v2.x — Communauté & contenus tiers

- [ ] Section "Univers communautaires" : settings type Terre du Milieu, Westeros, Robin Hood
- [ ] Fiches PJ téléchargeables (PDF + version interactive HTML)
- [ ] Galerie d'aventures officielles et amateures (collection Astro `aventures`)

## v3.0 — Internationalisation

- [ ] Activer `i18n` natif d'Astro
- [ ] Traduire la base FR → EN
- [ ] Switcher de langue dans le header
- [ ] Slugs localisés (`/en/rules/combat` / `/regles/combat`)

## Idées long-terme (parking)

- Intégration **Scribe AI** : permettre d'importer le book Palantír directement dans Scribe pour les MJ qui préparent leurs sessions.
- Simulateur de dés en JS (1d12 + Xd6 + bravoure cumulée).
- Générateurs aléatoires intégrés (PNJ, oracle, donjon).
- Fiches PJ interactives (sauvegarde locale, export).
- Dark mode.
- Mode "live session" partagé (suivi d'initiative, Bravoure du groupe).

## Idées de design / mécaniques (notes éparses)

- Marques de blessure légère style Grimwild (prochain jet avec malus).
- Pools de dice pour adversité côté MJ (Grimwild).
- Aide entre joueurs : le compagnon qui aide jette le dé (Grimwild).
- Dés "épineux" d8 — un 8 = échec, permet d'infliger un malus même sans point d'attribut.
- Suspense : point si on fait réussir un PJ malgré son échec (à dépenser plus tard en adversité).
- Système Principe & Compétence (Dune) pour l'extension Westeros.
- Force vs Dextérité pour la distance, capacités spéciales par espèce.
- Extension "batailles à grande échelle" avec machines de siège.
