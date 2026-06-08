# Plan de développement — Palantír RPG

Roadmap vivante du projet. Mise à jour au fil des versions.

## v1.0 — Site public (en cours)

**Objectif** : publier les règles existantes en site statique navigable et indexable.

- [x] Bootstrap Astro + content collections + GH Pages
- [x] Migration intégrale du contenu du Google Doc en Markdown
- [x] Typographie Grenze / Crimson Pro
- [x] Layout SRD-like (sidebar + contenu + TOC)
- [ ] Recherche Pagefind branchée en UI (composant `Search.astro`)
- [x] Acheter et brancher le domaine `palantir-rpg.com` (CNAME GitHub Pages)
- [ ] Première passe de relecture sur l'ensemble du contenu
- [ ] Fusionner les Historiques et les Traits et Désirs
- [ ] Ajouter un système de Blessure permanente (échec critique sur jet CON) avec une table aléatoire dédiée (perd 1 point d'attribut ? ou gagne un atout négatif pour que ce soit libre, plus narratif ?)
- [ ] Vérification par Claude (orthographe, cohérence des règles et des termes comme "héros/personnages/PJ/joueurs", simulation de combats avec des héros et adversaires de différents niveau pour voir s'il faut ajuster les dégâts des adversaires)
- [ ] Compléter le glossaire et le mettre dans une modal ou en draw qui s'ouvre depuis un bouton sur la sidebar de droite jsp, avec tous les termes spécifiques par exemple "convalescence" (dans les blessures) et ajouter un lien vers les pages concernées
- [ ] Ajouter un index au début (comme dans un livre -> plus complet que la sidebar car on mets tous les sous-chapitres, si possibles dynamiquement pour éviter de devoir le tenir à jour H24 je sais pas (avec les H1, H2 ?))
- [ ] Liens [`ROADMAP`](https://github.com/benjaminhaeberli/palantir/blob/develop/ROADMAP.md) avec icône "lien externe" et rajouter icône de GITHUB à côté du lien GITHUB (icon library déjà chargée ? sinon lucide-icons?)

- [x] Simplifier **Atouts** : 8 atouts avec effet de base + effet renforcé (PB)
- [x] Compléter **Combat** : actions non-offensives, dégâts 1d6 uniformes, coup critique = blessure
- [x] Compléter **Bestiaire** : 8 créatures de référence (niveaux 1–6), mécanique blessures/niveau
- [ ] Compléter **Équipement** : liste complète d'armes/armures avec propriétés
- [ ] Compléter **Mésaventures** : tables inspirées de Knave/Shadowdark
- [ ] Compléter **Bestiaire** : étendre à 20–30 créatures
- [ ] Compléter **Sortilèges** : système de magie freeform
- [ ] Rendre le site responsive pour mobile

## v1.x — Améliorations diverses

- [ ] ⁠Ajouter un système de versioning des règles (alpha ou beta ou v1 jsp voir semanting versioning) pour débuter) où je travaille à chaque fois sur develop pour avancer quand on ramène sur main on rajoute un numéro de version. Et mettre un petit sélecteur de numéro de version (avec date de publication entre parenthèses et du plus récent au plus vieux)
- [ ] Page "Contribuer" pointant vers `CONTRIBUTING.md`

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
