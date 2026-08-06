# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/) and this project adheres to [Semantic Versioning](https://semver.org/).

## [Non publié]

Les *Peuples* deviennent les **Lignées** et quittent la Terre du Milieu : six lignées maison — Astrubaliens, Vœrn, Nains, Elfes, Centaures, Lutins — proposant chacune quatre pouvoirs, dont un seul est retenu. Les *Atouts* passent de 9 exemples à **24 atouts jouables**, et gagnent surtout ce qui leur manquait : ils **progressent** désormais sur trois rangs. La campagne s'étend à **10 niveaux**, où chaque palier laisse choisir entre apprendre un atout de plus ou approfondir un atout déjà acquis.

### ⚠️ Critique

- **lignées** : le chapitre *Peuples* devient **Lignées**. L'ancre publique change : `palantir-rpg.com/#peuples` ne résout plus, remplacée par `#lignees`. Les douze peuples empruntés à la Terre du Milieu et à Westeros disparaissent au profit de six lignées propres au jeu.
- **progression** : la campagne passe de **6 à 10 niveaux**. Les seuils d'XP des six premiers niveaux sont **inchangés** — une table en cours ne perd rien — mais l'attribut ne monte plus qu'**un niveau sur deux** et les *PA* **plafonnent à 4**. Un héros de niveau 10 atteint donc exactement le même attribut maximum qu'un héros de niveau 6 auparavant : la courbe est étirée, pas gonflée.
- **atouts** : un atout se joue désormais à l'un de **trois rangs** — *Novice*, *Aguerri*, *Maître* — dont les effets renforcés coûtent **2, 4 puis 6 PB**. Le gain de niveau devient une monnaie unique : un nouvel atout, ou la montée d'un rang.
- **combat** : les *points d'action* **plafonnent à 3** au lieu de 4, et se gagnent plus tard — le 2ᵉ au niveau 3, le 3ᵉ au niveau 7. Chaque PA ajoute un jet par héros et par tour : à quatre joueurs, le 4ᵉ PA portait un combat de quatre tours à plus de seize minutes de lancers.

### ✨ Ajouté

- **lignées** : six lignées jouables avec quatre pouvoirs au choix chacune, soit **24 pouvoirs**. Gobelins, Fées et Dragons sont explicitement rangés du côté des PNJ.
- **atouts** : la liste passe à **24 atouts**, six par catégorie, sur trois rangs — soit 72 rangs et 144 effets. Quatre leviers jusque-là inexploités sont couverts : les *points d'action*, l'initiative libre, les manœuvres (pousser, immobiliser, intimider) et les *Premiers soins*.
- **ressources** : section **Calibrer un atout maison** dans *Adapter à votre univers*, qui publie le barème chiffré — combien de *PB* un héros gagne par tour à chaque niveau, et pourquoi 2, 4 et 6 restent des arbitrages.
- **glossaire** : entrées **Atout**, **Gain d'atout** et **Lignée**.
- **bestiaire** : section **Adversaire solitaire**. Une créature seule ne tient jamais face à une compagnie — quatre héros lancent jusqu'à douze attaques par tour, elle en lance trois — et aucune *Endurance* ne rattrape ce rapport. Deux correctifs : doubler son Endurance, et lui donner une **attaque de zone** un tour sur deux. Le dragon les applique (Endurance 60, souffle régulier).
- **outils** : `tools/probabilites.py` réécrit autour du système en vigueur, avec onze sections appelables séparément — dont la simulation de combat que la ROADMAP réclamait : espérance de dégâts, duel, matrice héros × créature, rencontres de groupe, adversaire solitaire et chaîne de létalité.

### 🔨 Changé

- **héros** : l'étape 1 de la création choisit une *Lignée* et l'un de ses pouvoirs ; l'étape 8 ne renvoie plus à « la liste générale », qui contredisait la création libre.
- **atouts** : le garde-fou « les atouts gagnés à partir du niveau 4 coûtent 3 à 4 PB » disparaît — le barème de rangs fait le même travail plus proprement. La création libre reste possible, résumée dans *Atouts* et détaillée dans *Adapter à votre univers*.
- **bravoure** : le plafond `5 + niveau` **ne bouge pas**, malgré les effets à 6 PB. Vérifié : un rang *Maître* arrive au plus tôt au niveau 3, où 6 PB représentent 75 % de la réserve, et reste un vrai coût jusqu'au niveau 10.

### 🐛 Corrigé

- **glossaire** : l'entrée *Tour* annonçait encore « deux actions », en contradiction avec le système de *PA* qui en donne 1 au niveau 1.

## v0.2.0 - 2026-08-06

Le jeu n'additionne plus rien : un jet se lit désormais sur les trois faces les plus hautes du *dé du destin*, ou sur un 6 parmi les *dés de bravoure*. Cette refonte du moteur a entraîné dans son sillage le plafonnement de la *Bravoure*, la fusion des Traits dans les Historiques, le découpage du livre en trois volumes et une passe complète sur le combat. Le site gagne au passage un système de magie freeform, un chapitre pour adapter le jeu à son propre univers, un vrai menu mobile et une illustration d'ouverture.

**Contributeurs :** @benjaminhaeberli, @claude
**Comparer sur GitHub :** https://github.com/benjaminhaeberli/palantir/compare/v0.1.0...v0.2.0

### ⚠️ Critique

- **règles** : le jet d'attribut n'additionne plus `1d12 + Nd6` contre un seuil. On lit le *dé du destin* — réussite sur 10, 11 ou 12 — et s'il ne suffit pas, on cherche un 6 sur les *dés de bravoure*. Le **seuil de réussite** `10 + (2 × attribut)` disparaît du jeu ; il ne survit qu'en capacité de charge. Les courbes de réussite ont été calibrées pour rester à quelques points de l'ancien système, afin que bestiaire, dégâts et *Endurance* restent justes.
- **combat** : un *échec critique* sur un *jet de défense* rend **Blessé** sur-le-champ, sans jet de blessure intermédiaire. Le *jet de blessure* ne concerne plus que les périls du monde — froid, chute, feu, suffocation, poison.
- **bravoure** : un jet n'inspire qu'**une fois**, quel que soit le nombre de 6, et la réserve est plafonnée à `5 + niveau`. Au-delà, il faut donner à un compagnon (2 PB pour en offrir 1) ou perdre le surplus.

### ✨ Ajouté

- **sorcellerie** : système freeform *Verbe* + *Forme*, avec une *Ampleur* de 1 à 4 qui fixe la difficulté et le coût en `Δ`. Cinq Verbes universels, Formes libres, `Δ` de Sorcellerie sur le sorcier ou sur un objet qui se consume.
- **combat** : une *réussite critique* en défense ouvre une **contre-attaque gratuite** (0 PA), symétrique de l'échec critique.
- **héros** : nouvel atout d'exemple **Rompu aux coups**, qui absorbe une fois par combat la *Blessure* d'un échec critique en défense.
- **ressources** : chapitre **Adapter à votre univers**, qui sépare le socle mécanique intransportable du contenu qui tient au décor.
- **héros** : table des **Désirs**, distincte du But narratif — le Désir est permanent, le But est l'objectif de la campagne.
- **mobile** : menu plein écran avec tous les chapitres groupés, et sommaire inline injecté sous chaque titre de chapitre.
- **site** : illustration d'ouverture sur la landing, servie via `astro:assets` (4,1 Mo ramenés à 71–274 Ko selon l'écran) ; version du jeu lue depuis le dernier tag git et affichée en topbar et au colophon.
- **analytics** : suivi Plausible sur `palantir-rpg.com`, bundlé par Astro plutôt que chargé en script tiers, avec liens sortants et téléchargements suivis et capture désactivée sur `localhost`.
- **ressources** : tables aléatoires des extensions converties en `RollableTable` interactives (panique, folie, mésaventures magiques) ; colophon crédits et remerciements.

### 🔨 Changé

- **règles** : l'encadré « Dé ou avantage ? » oppose désormais ce qui vient de la **situation** (toujours ±1d6) à ce qui est **écrit sur la fiche**, où la portée tranche — un métier étroit donne l'avantage, un domaine large donne +1d6. L'ancienne formule contredisait la table des Historiques.
- **combat** : l'**attaque puissante** produit exactement l'effet d'un *coup critique* au lieu de doubler les dés — un seul effet à retenir, et l'arme se brise toujours. Elle inflige donc aussi une blessure à la cible.
- **héros** : Traits & Désirs fusionnés dans les **Historiques**, qui deviennent le chapitre d'identité (métier, domaine, caractère, désirs, but). Les 100 métiers reçoivent une **portée écrite et bornée**, jamais martiale : la contrainte vit dans la table, plus dans la tête du MJ.
- **structure** : le livre est découpé en **trois volumes** — Règles, Héros, MJ — via une nouvelle collection `heros`. Les 24 ancres publiques sont préservées, `cleanId` strippant le préfixe numérique.
- **site** : le cadre **médiéval** est assumé partout (introduction, landing, README). C'est le moteur qui est générique, pas le contenu — peuples, bestiaire, équipement et métiers sont de la fantasy médiévale.
- **règles** : franchir une catégorie de distance est **gratuit une fois par tour**, chaque catégorie suivante coûte 1 PA — un héros de niveau 1 peut donc avancer *et* agir. La distance *Distant* passe à 10 cases.
- **bestiaire** : créatures exprimées en PA (1 attaque = 1 PA), niveau découplé des PA ; *vulnérabilité* et *résistance* (×2 ou ½) appliquées discrètement par le MJ.
- **règles** : *Forcer le destin* est déplafonné, ses rendements décroissants absorbant seuls le surplus de Bravoure ; l'XP est mis en commun, ce qui supprime la variance et le biais du bouclier ; *Pessimiste* devient un état de fait qui se lève seul.
- **équipement** : armes de mêlée à deux mains à `1d6+2`, bouclier porté à 2 emplacements de *Charge*.
- **atouts** : création libre en session 0 plutôt que liste fermée ; un *avantage* se paie toujours en PB, et les atouts gagnés à partir du niveau 4 coûtent plus cher.
- **blessures** : jet simplifié, convalescence, *Table du dernier espoir* à 1/4 de mortalité, premiers soins ajustés.
- **header** : le hamburger cède la place à un bouton « Menu » plein noir, et l'overlay s'ouvre instantanément.
- **mise en page** : lecture sur une seule colonne ; règles générales réorganisées autour de « Système de résolution » et « Jets spéciaux ».

### 🐛 Corrigé

- **layout** : zone vide d'une hauteur de viewport et scroll bloqué sous 1100 px — la colonne de sommaire restait affichée sans grille et retombait sous le contenu.
- **mobile** : tables débordantes rendues scrollables horizontalement, contenu contraint à 100 %, et menu rendu accessible au clavier (piège à Tab, gestion du focus, `:focus-visible`).
- **outils** : l'export « Copier pour un LLM » ignorait la collection `heros` et amputait donc les six chapitres du Livre du héros.
- **règles** : le chapitre Tours annonçait « deux PA », en contradiction avec la table de progression.
- **interface** : icône JSON du panneau de copie qui se coupait sur deux lignes.

### 🔥 Supprimé

- Le **seuil de réussite**, l'addition des dés et le malus `-1d6` des *États*, devenus sans objet avec le comptage de succès.
- Le **jet de blessure au combat**, remplacé par la Blessure immédiate — sa ligne disparaît de la table interactive.
- Les styles morts du hamburger et le fondu d'ouverture de l'overlay.

### ⚙️ Technique

- `tools/probabilites.py` étendu en harnais de comparaison exacte : systèmes candidats, fidélité à la courbe, valeur marginale d'un dé, revenu de *Bravoure* par combat. Le calculateur `/outils/probabilites` documente la bascule chiffrée.
- Plugin rehype maison enveloppant chaque `<table>` dans `.table-scroll` — scroll horizontal seulement si nécessaire, desktop intact.
- `fetch-depth: 0` sur le workflow de déploiement, sans quoi le clone arrive sans tags et la version ne peut pas être lue.
- Montée en **Astro 7** (MDX 7, sitemap 3.7), qui exige désormais **Node ≥ 22.12**. Un `.nvmrc` fixe la version pour le local comme pour la CI, et `engines` la déclare dans `package.json` : le déploiement échouait, le workflow étant resté sur Node 20.
- Actions du workflow montées en `checkout@v7` et `setup-node@v7`, qui tournent sur Node 24 — les versions `v4` étaient dépréciées par GitHub.
- ROADMAP réorganisée (jalons v1.0 et v1.x) et README illustré ; piste du proxy Plausible documentée — DNS Cloudflare et route Worker suffisent, sans quitter GitHub Pages.

## v0.1.0 - 2026-06-03

Première version publique de **Palantír**, le site de règles du JdR OSR francophone. Site statique Astro, contenu en Markdown, recherche intégrée (Pagefind) et déploiement automatique sur GitHub Pages.

### ✨ Ajouté
- Squelette du site Astro avec l'intégralité du contenu des règles *Palantír* et les outils de jeu (#3)
- Navigation par ancres et refonte des chapitres *Inconscience* et personnalité (#3)
- Refonte du système : atouts, sections, combat et bestiaire (#1)
- Restructuration des livres ; équipement, peuples et combat étoffés
- Widgets : copie des règles/tables et lecteur de musique en overlay
