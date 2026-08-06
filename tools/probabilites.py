#!/usr/bin/env python3
"""
Palantír RPG — harnais de calibrage.

Toutes les probabilités de jet sont EXACTES (Fraction, pas de Monte-Carlo) : on
arbitre des écarts de 2-3 points, une simulation ne serait pas assez fine. Les
combats sont résolus par propagation de distribution, sans tirage aléatoire non
plus : deux exécutions donnent toujours le même résultat.

LE SYSTÈME EN VIGUEUR
    Jet = 1d12 (dé du destin) + Nd6 (dés de bravoure, N = attribut).
    Réussite          : d12 >= 10, OU au moins un 6 parmi les dés de bravoure.
    Réussite critique : d12 = 12.
    Échec critique    : d12 = 1 — aucun 6 ne le rattrape.
    Rien ne s'additionne jamais.
    → src/content/regles/03-regles-generales.md

    La difficulté ne passe jamais par un nombre annoncé : elle se règle en
    ajoutant ou retirant des d6 (outil, aide, situation). L'avantage et le
    désavantage, eux, jouent sur le d12 (2d12, on garde le meilleur ou le pire).

LE SYSTÈME HISTORIQUE (archive)
    Jet = 1d12 + Nd6 >= SR, avec SR = 10 + 2N. Remplacé en v0.2.0 parce qu'il
    imposait une addition à chaque jet. Conservé ici pour vérifier que la courbe
    de réussite n'a pas dérivé — le bestiaire, les dégâts et l'Endurance ont été
    calibrés dessus.

Usage :
    python3 tools/probabilites.py            # tout
    python3 tools/probabilites.py combat     # une section (voir SECTIONS)
"""

from __future__ import annotations

import sys
from fractions import Fraction
from itertools import product
from typing import Dict, Tuple

MODES = ("normal", "advantage", "disadvantage")
MODE_LABEL = {"normal": "normal", "advantage": "avantage", "disadvantage": "désavantage"}

FATE_THRESHOLD = 10   # le dé du destin tranche sur 10, 11, 12
CRIT_SUCCESS = 12
CRIT_FAIL = 1

# --- Progression du héros — src/content/heros/02-heros.md -------------------
# Attribut principal : 2 à la création, +1 aux niveaux 2, 4, 6, 8, 10.
# PA plafonnés à 3 : chaque PA ajoute 4 jets par tour à une table de quatre, soit
# ~50 s de lancers. À 4 PA, un combat de 4 tours dépassait 16 minutes de dés.
LEVELS = range(1, 11)
ATTR_GAIN_LEVELS = (2, 4, 6, 8, 10)
PA_BY_LEVEL = {1: 1, 2: 1, 3: 2, 4: 2, 5: 2, 6: 2, 7: 3, 8: 3, 9: 3, 10: 3}
TALENT_GAINS_BY_LEVEL = {1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 10, 10: 11}
XP_BY_LEVEL = {1: 0, 2: 5, 3: 12, 4: 22, 5: 35, 6: 50, 7: 68, 8: 88, 9: 110, 10: 135}

# --- Coûts en Bravoure -----------------------------------------------------
RANK_COSTS = {"Novice": 2, "Aguerri": 4, "Maître": 6}   # src/content/heros/05-atouts.md
FORCE_DESTIN = 1                                        # 1 PB = +1d6
TRAIN_COMPANION = 2                                     # 2 PB pour en donner 1


def attribute_at(level: int) -> int:
    """Attribut principal supposé : 2 à la création, +1 un niveau sur deux."""
    return 2 + sum(1 for lv in ATTR_GAIN_LEVELS if lv <= level)


def pb_cap(level: int) -> int:
    """Plafond de la réserve de Bravoure : 5 + niveau."""
    return 5 + level


# ---------------------------------------------------------------------------
# Briques de résolution
# ---------------------------------------------------------------------------


def d12_distribution(mode: str) -> Dict[int, Fraction]:
    """Probabilité de chaque face du dé du destin selon le mode."""
    if mode == "normal":
        return {v: Fraction(1, 12) for v in range(1, 13)}
    dist: Dict[int, Fraction] = {}
    op = max if mode == "advantage" else min
    for a, b in product(range(1, 13), repeat=2):
        v = op(a, b)
        dist[v] = dist.get(v, Fraction(0)) + Fraction(1, 144)
    return dist


def p_no_six(pool: int) -> Fraction:
    """Probabilité qu'aucun dé de bravoure n'affiche de 6."""
    return Fraction(5, 6) ** max(pool, 0)


def resolve(pool: int, mode: str = "normal") -> dict:
    """
    Profil exact d'un jet du système en vigueur.

    `pool` = attribut + dés bonus (outil, aide, PB dépensés). Une valeur
    négative représente des conditions défavorables ; le pool plancher est 0,
    et le dé du destin laisse alors toujours sa chance sur quatre.
    """
    pool = max(pool, 0)
    none = p_no_six(pool)
    any_six = 1 - none

    success = fail = crit_success = crit_fail = Fraction(0)
    for v, p12 in d12_distribution(mode).items():
        if v == CRIT_SUCCESS:
            success += p12
            crit_success += p12
        elif v == CRIT_FAIL:
            fail += p12
            crit_fail += p12          # aucun 6 ne rattrape un 1
        elif v >= FATE_THRESHOLD:
            success += p12            # le destin tranche seul
        else:
            success += p12 * any_six  # sauvé par un 6
            fail += p12 * none

    return {
        "success": success,
        "fail": fail,
        "crit_success": crit_success,
        "crit_fail": crit_fail,
        "normal_success": success - crit_success,
        "normal_fail": fail - crit_fail,
    }


def resolve_legacy(attribute: int, mode: str = "normal") -> dict:
    """Système historique : 1d12 + Nd6 >= 10 + 2N. Archive de comparaison."""
    sr = 10 + 2 * attribute
    d6s: Dict[int, Fraction] = {0: Fraction(1)}
    if attribute:
        d6s = {}
        for outcome in product(range(1, 7), repeat=attribute):
            s = sum(outcome)
            d6s[s] = d6s.get(s, Fraction(0)) + Fraction(1, 6 ** attribute)

    success = fail = crit_success = crit_fail = Fraction(0)
    for v, p12 in d12_distribution(mode).items():
        for total_d6, p6 in d6s.items():
            joint = p12 * p6
            if v == CRIT_SUCCESS:
                success += joint
                crit_success += joint
            elif v == CRIT_FAIL:
                fail += joint
                crit_fail += joint
            elif v + total_d6 >= sr:
                success += joint
            else:
                fail += joint
    return {
        "sr": sr, "success": success, "fail": fail,
        "crit_success": crit_success, "crit_fail": crit_fail,
        "normal_success": success - crit_success, "normal_fail": fail - crit_fail,
    }


def pct(f) -> str:
    return f"{float(f) * 100:6.2f}%"


def rule(title: str) -> None:
    print("\n" + "=" * 78)
    print(f" {title}")
    print("=" * 78)


# ---------------------------------------------------------------------------
# 1. Courbe de réussite
# ---------------------------------------------------------------------------


def section_courbe() -> None:
    rule("Courbe de réussite — système en vigueur")
    print("  Le pool = attribut + dés bonus. Un attribut de 2 est le maximum à la création,")
    print("  un attribut de 7 le maximum atteignable au niveau 10.")

    for mode in MODES:
        print(f"\n  Mode : {MODE_LABEL[mode]}")
        header = (f"  {'pool':<6}{'Crit ✗':>9}{'Échec':>9}"
                  f"{'Réussite':>11}{'Crit ✓':>9}{'Total ✓':>10}")
        print(header)
        print("  " + "-" * (len(header) - 2))
        for pool in range(0, 11):
            r = resolve(pool, mode)
            print(f"  {pool:<6}{pct(r['crit_fail']):>9}{pct(r['normal_fail']):>9}"
                  f"{pct(r['normal_success']):>11}{pct(r['crit_success']):>9}"
                  f"{pct(r['success']):>10}")

    print("\n  Le plancher à 25 % (pool 0, mode normal) est structurel : le dé du destin")
    print("  tranche seul sur trois faces. Aucun cumul de malus ne descend en dessous —")
    print("  seul le désavantage casse ce plancher, à 6,25 %.")


def section_marginal() -> None:
    rule("Valeur marginale — un dé de plus, ou l'avantage")
    print("  Un modificateur lisible doit valoir à peu près la même chose partout.")
    print()
    header = f"  {'pool'.ljust(6)}{'+1 dé':>10}{'avantage':>12}{'désavantage':>14}"
    print(header)
    print("  " + "-" * (len(header) - 2))
    for pool in range(0, 9):
        base = float(resolve(pool)["success"])
        one_more = float(resolve(pool + 1)["success"]) - base
        adv = float(resolve(pool, "advantage")["success"]) - base
        dis = float(resolve(pool, "disadvantage")["success"]) - base
        print(f"  {pool:<6}{one_more * 100:>9.1f} {adv * 100:>11.1f} {dis * 100:>13.1f}")

    cf_n = float(resolve(2)["crit_fail"])
    cf_a = float(resolve(2, "advantage")["crit_fail"])
    print(f"\n  L'avantage vaut ~2 dés et divise l'échec critique par "
          f"{cf_n / cf_a:.0f} ({cf_n * 100:.2f} % → {cf_a * 100:.2f} %).")
    print("  C'est pourquoi il ne s'obtient jamais gratuitement : ni dans un effet")
    print("  permanent d'atout, ni ailleurs sur la fiche sans portée étroite.")


# ---------------------------------------------------------------------------
# 2. Progression et Bravoure
# ---------------------------------------------------------------------------


def pb_per_turn(level: int, defenses: int = 1) -> Fraction:
    """
    Bravoure gagnée par tour de combat.

    Un jet dont les dés de bravoure montrent au moins un 6 rapporte 1 PB, un
    seul, quel qu'en soit le nombre. L'espérance ne dépend donc que du nombre
    de JETS et de la taille du pool.

    Les jets de défense comptent double dans ce total : le MJ ne lance jamais
    de dés (src/content/regles/06-combat.md), donc chaque attaque ennemie fait
    lancer le héros.
    """
    rolls = PA_BY_LEVEL[level] + defenses
    return rolls * (1 - p_no_six(attribute_at(level)))


def section_progression() -> None:
    rule("Progression du héros sur 10 niveaux")
    print("  Un gain d'atout s'échange contre un nouvel atout au rang Novice, ou contre")
    print("  la montée d'un rang sur un atout déjà possédé. Onze gains sur la chronique.")
    print()
    header = (f"  {'Niv':<5}{'XP':>5}{'Attr':>6}{'PA':>4}{'Gains':>7}"
              f"{'Plaf. PB':>10}{'Réussite':>10}{'PB/tour':>9}{'PB/combat':>11}")
    print(header)
    print("  " + "-" * (len(header) - 2))
    for lv in LEVELS:
        attr = attribute_at(lv)
        turn = pb_per_turn(lv)
        print(f"  {lv:<5}{XP_BY_LEVEL[lv]:>5}{attr:>6}{PA_BY_LEVEL[lv]:>4}"
              f"{TALENT_GAINS_BY_LEVEL[lv]:>7}{pb_cap(lv):>10}"
              f"{pct(resolve(attr)['success']):>10}"
              f"{float(turn):>9.2f}{float(turn) * 4:>11.1f}")

    print("\n  (combat de 4 tours, 1 défense subie par tour, attribut principal investi")
    print("  à chaque gain — hypothèse haute)")
    print(f"\n  Attribut maximum au niveau 10 : {attribute_at(10)} — identique au maximum")
    print("  qu'atteignait un niveau 6 dans l'ancienne progression. La courbe est")
    print("  étirée, pas gonflée : c'est ce qui rend l'extension sûre.")


def section_rangs() -> None:
    rule("Calibrage des rangs d'atout — 2, 4 et 6 PB")
    print("  Règle : une dépense qui coûte MOINS que le revenu d'un tour cesse d'être")
    print("  un choix pour devenir un réflexe. On veut donc coût > PB/tour.")
    print()
    costs = sorted(set(RANK_COSTS.values()))
    header = (f"  {'Niv':<5}{'PB/tour':>9}{'PB/combat':>11}{'Plaf.':>7}  "
              + "".join(f"{f'{c} PB':>17}" for c in costs))
    print(header)
    print("  " + "-" * (len(header) - 2))
    for lv in LEVELS:
        turn = float(pb_per_turn(lv))
        fight = turn * 4
        line = f"  {lv:<5}{turn:>9.2f}{fight:>11.1f}{pb_cap(lv):>7}  "
        for c in costs:
            verdict = "arbitrage" if c > turn else "BANALISÉ"
            line += f"{f'{fight / c:.1f}× {verdict}':>17}"
        print(line)

    print("\n  Lecture : « × » = combien de fois le héros peut se l'offrir dans un combat")
    print("  de 4 tours. « BANALISÉ » = il se le paie à chaque tour, ce n'est plus un")
    print("  arbitrage — acceptable seulement si la cadence de l'effet est bornée")
    print("  (1×/tour, 1×/combat, 1×/scène, 1×/session).")
    print()
    for name, cost in RANK_COSTS.items():
        first = next((lv for lv in LEVELS if cost <= float(pb_per_turn(lv))), None)
        verdict = f"banalisé à partir du niveau {first}" if first else "jamais banalisé"
        cap_ok = next((lv for lv in LEVELS if pb_cap(lv) >= cost), None)
        print(f"  {name:<9} {cost} PB — {verdict}, payable dès le niveau {cap_ok}")

    print("\n  Un rang Maître coûte 2 gains d'atout, donc arrive au plus tôt au niveau 3 :")
    print(f"  6 PB y représentent {6 / pb_cap(3) * 100:.0f} % de la réserve. C'est la sensation voulue.")


def section_depenses() -> None:
    rule("Les autres dépenses de Bravoure")
    print("  Forcer le destin (1 PB = +1d6) est l'étalon : tout effet renforcé doit")
    print("  valoir strictement mieux que le même nombre de PB dépensés ainsi.")
    print()
    header = f"  {'attribut':<10}" + "".join(f"{f'+{n} PB':>9}" for n in range(0, 7))
    print(header)
    print("  " + "-" * (len(header) - 2))
    for attr in (2, 4, 6, 7):
        line = f"  {attr:<10}"
        for spent in range(0, 7):
            line += f"{float(resolve(attr + spent)['success']) * 100:>8.1f} "
        print(line)

    print("\n  Rendements décroissants : vider dix PB sur un jet ne l'emmène jamais")
    print(f"  au-delà de {float(resolve(2 + 10)['success']) * 100:.0f} %. La certitude ne s'achète pas.")
    print()
    print(f"  Entraîner un compagnon : {TRAIN_COMPANION} PB pour en donner 1. Ce taux de change")
    print("  fixe le plancher de tout effet qui bénéficie à un allié — en dessous de")
    print(f"  {TRAIN_COMPANION} PB, l'effet court-circuiterait la règle générale.")


# ---------------------------------------------------------------------------
# 3. Combat
# ---------------------------------------------------------------------------

# Bestiaire — src/content/conseils-mj/03-bestiaire.md
def creature_endurance(level: int) -> int:
    return 5 * level


def creature_damage(level: int) -> int:
    return 3 + level


def hero_endurance(con: int) -> int:
    return 10 + 3 * con


def damage_distribution(die: int = 6, bonus: int = 0) -> Dict[int, Fraction]:
    """Distribution des dégâts d'une arme (1d6, ou 1d6+2 à deux mains)."""
    return {v + bonus: Fraction(1, die) for v in range(1, die + 1)}


def expected_attack_damage(pool: int, die: int = 6, bonus: int = 0,
                           mode: str = "normal") -> Tuple[float, float]:
    """
    Espérance de dégâts d'une attaque, et probabilité d'infliger une blessure.

    Réussite critique : dégâts maximum de l'arme, plus un dé supplémentaire, et
    une blessure à la cible. Réussite normale : le dé de l'arme.
    Échec : rien. — src/content/regles/06-combat.md
    """
    r = resolve(pool, mode)
    avg_die = (die + 1) / 2
    normal = float(r["normal_success"]) * (avg_die + bonus)
    crit = float(r["crit_success"]) * ((die + bonus) + avg_die)
    return normal + crit, float(r["crit_success"])


def section_degats() -> None:
    rule("Espérance de dégâts par attaque")
    print("  Une main / fronde / arc : 1d6. Deux mains : 1d6+2. Mains nues : 1d4.")
    print("  Le coup critique inflige le maximum de l'arme, plus un dé — et une blessure.")
    print()
    weapons = [("1d6 (une main)", 6, 0), ("1d6+2 (deux mains)", 6, 2), ("1d4 (mains nues)", 4, 0)]
    header = f"  {'pool':<6}" + "".join(f"{w[0]:>22}" for w in weapons)
    print(header)
    print("  " + "-" * (len(header) - 2))
    for pool in range(0, 9):
        line = f"  {pool:<6}"
        for _, die, bonus in weapons:
            dmg, _ = expected_attack_damage(pool, die, bonus)
            line += f"{dmg:>21.2f} "
        print(line)

    print("\n  Rappel : l'attaque puissante produit l'effet d'un coup critique au prix de")
    print("  l'arme. Espérance par pool, une arme à une main :")
    print(f"  {'  déclarée :':<16}{6 + 3.5:.2f} dégâts + 1 blessure, arme brisée")
    print(f"  {'  ordinaire :':<16}pool 2 → {expected_attack_damage(2)[0]:.2f}   pool 7 → "
          f"{expected_attack_damage(7)[0]:.2f}")


def _distribute(dist: Dict[int, float], endurance: int,
                dmg_dist: Dict[int, Fraction], p_hit: float) -> Dict[int, float]:
    """Propage une distribution d'Endurance après une attaque."""
    out: Dict[int, float] = {}
    for end, p in dist.items():
        if end <= 0:
            out[0] = out.get(0, 0.0) + p
            continue
        out[end] = out.get(end, 0.0) + p * (1 - p_hit)
        for d, pd in dmg_dist.items():
            nxt = max(end - d, 0)
            out[nxt] = out.get(nxt, 0.0) + p * p_hit * float(pd)
    return out


def simulate_fight(level: int, con: int = 2, armour: int = 1,
                   creature_level: int | None = None, max_turns: int = 20) -> dict:
    """
    Confrontation d'un héros et d'une créature, résolue par propagation de
    distribution — aucun tirage aléatoire, le résultat est reproductible.

    Le héros attaque autant de fois qu'il a de PA ; la créature attaque une fois
    par tour, ce qui déclenche un jet de défense du héros.

    Approximation assumée : les deux camps frappent en parallèle sur le tour,
    et l'état Blessé (désavantage) est appliqué dès la première Blessure.
    """
    creature_level = creature_level if creature_level is not None else level
    attr = attribute_at(level)
    pa = PA_BY_LEVEL[level]
    c_end0 = creature_endurance(creature_level)
    c_dmg = creature_damage(creature_level)
    h_end0 = hero_endurance(con)

    hero: Dict[int, float] = {h_end0: 1.0}
    crea: Dict[int, float] = {c_end0: 1.0}
    p_hero_dead = p_crea_dead = 0.0
    wounds = 0.0                      # espérance de blessures accumulées
    turns_to_kill = None
    dmg_dist = damage_distribution()

    for turn in range(1, max_turns + 1):
        # --- le héros frappe -------------------------------------------------
        r_att = resolve(attr)
        p_hit = float(r_att["success"])
        for _ in range(pa):
            crea = _distribute(crea, c_end0, dmg_dist, p_hit)
            wounds += float(r_att["crit_success"])
        p_crea_dead = crea.get(0, 0.0)
        if turns_to_kill is None and p_crea_dead >= 0.5:
            turns_to_kill = turn

        # --- la créature frappe, le héros se défend --------------------------
        r_def = resolve(attr)
        p_fail = float(r_def["normal_fail"])      # dégâts réduits par l'armure
        p_critfail = float(r_def["crit_fail"])    # dégâts pleins + Blessé
        survive = 1 - p_crea_dead
        eff = max(c_dmg - armour, 0)
        nxt: Dict[int, float] = {}
        for end, p in hero.items():
            if end <= 0:
                nxt[0] = nxt.get(0, 0.0) + p
                continue
            nxt[end] = nxt.get(end, 0.0) + p * (1 - survive * (p_fail + p_critfail))
            nxt[max(end - eff, 0)] = nxt.get(max(end - eff, 0), 0.0) + p * survive * p_fail
            nxt[max(end - c_dmg, 0)] = nxt.get(max(end - c_dmg, 0), 0.0) + p * survive * p_critfail
        hero = nxt
        p_hero_dead = hero.get(0, 0.0)
        if p_hero_dead >= 0.5 or p_crea_dead >= 0.99:
            break

    return {
        "turns": turns_to_kill or max_turns,
        "p_crea_dead": p_crea_dead,
        "p_hero_down": p_hero_dead,
        "wounds": wounds,
        "crea_wounds_needed": creature_level,
        "hero_end": h_end0,
        "crea_end": c_end0,
        "crea_dmg": c_dmg,
    }


def section_combat() -> None:
    rule("Simulation de combat — héros contre créature de même niveau")
    print("  Héros CON 2 (Endurance 16), une pièce d'armure, arme à une main.")
    print("  Créature : Endurance 5×niveau, dégâts 3+niveau, 1 PA.")
    print("  Résolu par propagation de distribution — reproductible, sans tirage.")
    print()
    header = (f"  {'Niv':<5}{'Attr':>5}{'PA':>4}  {'Créature':<26}"
              f"{'tours':>7}{'P(héros à terre)':>18}{'blessures':>11}")
    print(header)
    print("  " + "-" * (len(header) - 2))
    for lv in LEVELS:
        r = simulate_fight(lv)
        crea = f"niv {lv} — {r['crea_end']} END / {r['crea_dmg']} dég."
        print(f"  {lv:<5}{attribute_at(lv):>5}{PA_BY_LEVEL[lv]:>4}  {crea:<26}"
              f"{r['turns']:>7}{r['p_hero_down'] * 100:>17.1f}%{r['wounds']:>11.1f}")

    print("\n  « blessures » = réussites critiques accumulées. Une créature meurt aussi")
    print("  quand elle en encaisse autant que son niveau — un bandit de niveau 1 tombe")
    print("  au premier coup critique, même à pleine Endurance.")
    print("\n  Un déséquilibre visible ici signifie qu'il faut ajuster les dégâts ou")
    print("  l'Endurance du bestiaire, pas le moteur de résolution.")


def simulate_party(level: int, party: int = 4, creature_level: int | None = None,
                   creatures: int = 1, con: int = 2, armour: int = 1,
                   max_turns: int = 20) -> dict:
    """
    Compagnie contre rencontre — le vrai cas d'usage, le duel n'en est pas un.

    Les dégâts ennemis sont répartis sur la compagnie : chaque créature attaque
    un héros par tour, donc chaque héros subit `creatures / party` attaques.
    On suit l'Endurance d'un héros représentatif.
    """
    creature_level = creature_level if creature_level is not None else level
    attr = attribute_at(level)
    pa = PA_BY_LEVEL[level]
    pool_end = creature_endurance(creature_level) * creatures
    c_dmg = creature_damage(creature_level)
    hero: Dict[int, float] = {hero_endurance(con): 1.0}
    dmg_dist = damage_distribution()
    r = resolve(attr)
    p_hit, p_fail, p_critfail = (float(r["success"]), float(r["normal_fail"]),
                                 float(r["crit_fail"]))
    avg_dmg = sum(float(pd) * d for d, pd in dmg_dist.items())
    dpr = party * pa * p_hit * avg_dmg          # dégâts de la compagnie par tour

    remaining = float(pool_end)
    turns = None
    attacks_per_hero = creatures / party
    for turn in range(1, max_turns + 1):
        remaining = max(remaining - dpr, 0.0)
        alive = remaining / pool_end if pool_end else 0.0
        if turns is None and remaining <= 0:
            turns = turn
        eff = max(c_dmg - armour, 0)
        nxt: Dict[int, float] = {}
        share = attacks_per_hero * alive
        for end, p in hero.items():
            if end <= 0:
                nxt[0] = nxt.get(0, 0.0) + p
                continue
            nxt[end] = nxt.get(end, 0.0) + p * (1 - share * (p_fail + p_critfail))
            nxt[max(end - eff, 0)] = nxt.get(max(end - eff, 0), 0.0) + p * share * p_fail
            nxt[max(end - c_dmg, 0)] = nxt.get(max(end - c_dmg, 0), 0.0) + p * share * p_critfail
        hero = nxt
        if turns is not None:
            break
    return {"turns": turns or max_turns, "p_down": hero.get(0, 0.0)}


def section_groupe() -> None:
    rule("Rencontres de groupe — compagnie de 4 héros")
    print("  C'est le cas d'usage réel : le jeu n'est pas calibré pour du duel héroïque.")
    print("  Un héros représentatif est suivi ; les attaques ennemies sont réparties.")
    print()
    scenarios = [("1 créature de niveau égal", 1, 0), ("4 créatures de niveau égal", 4, 0),
                 ("8 créatures de niveau −2", 8, -2), ("1 « boss » de niveau +4", 1, +4)]
    header = f"  {'Niv':<5}" + "".join(f"{s[0]:>28}" for s in scenarios)
    print(header)
    print("  " + "-" * (len(header) - 2))
    for lv in LEVELS:
        line = f"  {lv:<5}"
        for _, count, delta in scenarios:
            cl = max(1, min(10, lv + delta))
            r = simulate_party(lv, creature_level=cl, creatures=count)
            cell = "{} t. · {:.0f} % à terre".format(r["turns"], r["p_down"] * 100)
            line += f"{cell:>28}"
        print(line)
    print("\n  Lecture : « 3 t. · 12 % à terre » = la rencontre se règle en 3 tours, et")
    print("  chaque héros a 12 % de chances d'y tomber. Au-delà de 30 %, la rencontre")
    print("  est meurtrière pour un groupe qui ne dépense ni atout ni Bravoure.")
    print()
    print("  DEUX CONSTATS DE DESIGN :")
    print("    · L'adversaire SOLO ne fonctionne pas, même très au-dessus du niveau du")
    print("      groupe : quatre héros à 3 PA lancent douze attaques par tour contre les")
    print("      trois d'un dragon. Voir la section « solo » — la correction passe par")
    print("      l'Endurance doublée et une attaque de ZONE, pas par les dégâts.")
    print("    · La HORDE est le vrai danger, et il croît avec le niveau : ce sont les")
    print("      attaques subies qui tuent, pas les dégâts par attaque. Une rencontre se")
    print("      durcit bien plus vite en ajoutant des corps qu'en montant le niveau.")
    print()
    print("  ⚠ LIMITES DU MODÈLE — à garder en tête avant d'ajuster quoi que ce soit :")
    print("    · aucun atout n'est joué, aucun PB dépensé — c'est une BORNE BASSE ;")
    print("    · pas de Premiers soins, pas de fuite, pas de terrain, pas de tactique ;")
    print("    · le bouclier n'est pas porté (il diviserait l'échec critique par douze) ;")
    print("    · les blessures de créature (réussites critiques) ne raccourcissent pas")
    print("      la rencontre ici, alors qu'elles tuent un adversaire de bas niveau.")
    print("  Les chiffres ci-dessus surestiment donc le danger. Ils servent à comparer")
    print("  des paliers entre eux, pas à prédire une table.")


def simulate_solo(hero_level: int, endurance_mult: int = 1, zone_dice: int = 0,
                  zone_every: int = 2, party: int = 4, con: int = 2,
                  armour: int = 1, max_turns: int = 12) -> Tuple:
    """
    Adversaire solitaire contre une compagnie — le cas que le bestiaire doit corriger.

    Une attaque de zone touche TOUS les héros pour une seule action : c'est le
    seul levier qui contourne l'arithmétique des actions. Renvoie (tours pour
    l'abattre, héros à terre).
    """
    attr = attribute_at(hero_level)
    r = resolve(attr)
    p_hit, p_fail = float(r["success"]), float(r["fail"])
    dpr = party * PA_BY_LEVEL[hero_level] * p_hit * 3.5
    endurance = creature_endurance(hero_level) * endurance_mult
    dmg = creature_damage(hero_level)
    pa = min(3, 1 + hero_level // 3)
    heroes = [float(hero_endurance(con))] * party
    eff = max(dmg - armour, 0)

    for turn in range(1, max_turns + 1):
        endurance -= dpr
        if endurance <= 0:
            return turn, sum(1 for e in heroes if e <= 0)
        if zone_dice and turn % zone_every == 0:
            for i in range(party):
                heroes[i] -= p_fail * zone_dice * 3.5
        for _ in range(pa):
            heroes[turn % party] -= p_fail * eff
        if all(e <= 0 for e in heroes):
            return None, party
    return None, sum(1 for e in heroes if e <= 0)


def section_solo() -> None:
    rule("Adversaire solitaire — vérification de la règle du Bestiaire")
    print("  Quatre héros contre une créature seule de leur niveau. Cible : un combat")
    print("  de 3 à 5 tours qui met au moins un héros à terre. 0 = trop mou, 4 = TPK.")
    print()
    variants = [
        ("aucune correction", 1, 0),
        ("Endurance ×2", 2, 0),
        ("Endurance ×2 + zone 3d6 un tour sur deux", 2, 3),
        ("Endurance ×2 + zone 4d6 un tour sur deux", 2, 4),
        ("Endurance ×3 + zone 3d6 un tour sur deux", 3, 3),
    ]
    header = f"  {'Variante':<44}" + "".join("{:>18}".format(f"niveau {lv}") for lv in (3, 6, 10))
    print(header)
    print("  " + "-" * (len(header) - 2))
    for name, mult, zone in variants:
        line = f"  {name:<44}"
        for lv in (3, 6, 10):
            turns, down = simulate_solo(lv, mult, zone)
            cell = "{} t. · {} à terre".format(turns if turns else ">12", down)
            line += f"{cell:>18}"
        print(line)

    print("\n  La règle retenue au Bestiaire est « Endurance ×2 + attaque de zone un tour")
    print("  sur deux ». Elle fait passer le combat de 2 à 4 tours.")
    print()
    print("  ⚠ Le modèle applique des espérances déterministes, sans variance : le")
    print("  passage de « aucun héros à terre » à « trois » se joue sur un cheveu, ce")
    print("  qui est un artefact de calcul et non une prédiction. La FRÉQUENCE de la")
    print("  zone est le curseur à régler en playtest, pas l'Endurance.")


def section_combat_matrice() -> None:
    rule("Matrice héros × créature — tours pour l'emporter")
    print("  Lecture : combien de tours avant que la créature tombe (P >= 50 %).")
    print("  « — » = le héros tombe le premier, ou n'y arrive pas en 20 tours.")
    print()
    header = f"  {'héros \\ créa':<14}" + "".join(f"{f'niv {c}':>8}" for c in LEVELS)
    print(header)
    print("  " + "-" * (len(header) - 2))
    for lv in LEVELS:
        line = f"  {f'niveau {lv}':<14}"
        for cl in LEVELS:
            r = simulate_fight(lv, creature_level=cl)
            line += f"{'—' if r['p_hero_down'] >= 0.5 else str(r['turns']):>8}"
        print(line)
    print("\n  La diagonale doit rester jouable : un héros doit pouvoir vaincre seul une")
    print("  créature de son niveau, sans que ce soit acquis. Au-dessus de la diagonale,")
    print("  c'est le rôle du groupe — le jeu n'est pas calibré pour du duel héroïque.")


def section_letalite() -> None:
    rule("Létalité — la chaîne qui mène à la mort")
    print("  1. Échec critique sur un jet de défense (1 sur le dé du destin)")
    print("  2. → dégâts pleins, armure ignorée, état Blessé sur-le-champ")
    print("  3. → une seconde Blessure rend Inconscient")
    print("  4. → jet sur la Table du dernier espoir : 1-3 sur 1d12 = mort")
    print()
    p_death_on_table = Fraction(3, 12)
    header = (f"  {'Mode'.ljust(14)}{'P(crit ✗)':>12}{'par défense':>14}"
              f"{'sur 4 défenses':>16}{'sur un combat de 4 tours':>26}")
    print(header)
    print("  " + "-" * (len(header) - 2))
    for mode in MODES:
        p = resolve(2, mode)["crit_fail"]
        four = 1 - (1 - float(p)) ** 4
        print(f"  {MODE_LABEL[mode].ljust(14)}{pct(p):>12}{pct(p):>14}"
              f"{four * 100:>15.1f}%{four * 100:>25.1f}%")

    p_normal = float(resolve(2)["crit_fail"])
    p_shield = float(resolve(2, "advantage")["crit_fail"])
    print(f"\n  Le bouclier (avantage en parade) fait passer le risque de {p_normal * 100:.2f} % à")
    print(f"  {p_shield * 100:.2f} % par défense — il divise la létalité par {p_normal / p_shield:.0f}, au prix du")
    print("  bouclier lui-même, brisé quand ce 1 finit par tomber.")

    print(f"\n  Mort effective : deux Blessures puis {float(p_death_on_table) * 100:.0f} % sur la Table du dernier")
    print("  espoir. Un héros déjà Blessé qui rate ainsi une défense joue sa vie —")
    print("  c'est le moment où il faut fuir ou soigner, et le jeu le dit.")

    print("\n  Comparaison avec la règle abandonnée (jet de blessure CON intermédiaire) :")
    header = f"  {'CON':<6}{'P(rater le jet)':>18}{'ancienne règle':>17}{'règle actuelle':>17}{'×':>6}"
    print(header)
    print("  " + "-" * (len(header) - 2))
    crit = Fraction(1, 12)
    for con in range(0, 5):
        p_fail = resolve(con)["fail"]
        old = crit * p_fail
        print(f"  {con:<6}{pct(p_fail):>18}{pct(old):>17}{pct(crit):>17}"
              f"{float(crit / old):>6.2f}")


# ---------------------------------------------------------------------------
# 4. Archive
# ---------------------------------------------------------------------------


def section_archive() -> None:
    rule("Archive — dérive par rapport au système historique")
    print("  Le bestiaire, les dégâts et l'Endurance ont été calibrés sur l'ancien")
    print("  système (1d12 + Nd6 >= 10 + 2N). La refonte devait rester à quelques")
    print("  points près, sans quoi tout le contenu chiffré aurait été à refaire.")
    print()
    header = (f"  {'attribut':<10}{'historique':>12}{'en vigueur':>12}{'écart':>10}")
    print(header)
    print("  " + "-" * (len(header) - 2))
    deviations = []
    for attr in range(0, 8):
        old = float(resolve_legacy(attr)["success"]) * 100
        new = float(resolve(attr)["success"]) * 100
        deviations.append(new - old)
        marker = "   ← plage de création" if attr == 2 else ""
        print(f"  {attr:<10}{old:>11.1f}%{new:>11.1f}%{new - old:>+9.1f}{marker}")

    def rms(vals) -> float:
        return (sum(d * d for d in vals) / len(vals)) ** 0.5

    print(f"\n  Écart quadratique moyen sur les attributs 0-3 : {rms(deviations[:4]):.1f} points")
    print(f"  Écart quadratique moyen sur les attributs 0-7 : {rms(deviations):.1f} points")
    print()
    print("  ⚠ La dérive n'est PAS négligeable, et elle croît avec l'attribut : le")
    print("  système en vigueur plafonne nettement plus bas que l'historique")
    print(f"  ({float(resolve(7)['success']) * 100:.0f} % contre {float(resolve_legacy(7)['success']) * 100:.0f} % à l'attribut 7). C'est structurel — le dé du")
    print("  destin garde toujours son mot à dire — et c'est voulu : un héros de haut")
    print("  niveau ne devient jamais infaillible, ce qui préserve la létalité OSR.")
    print()
    print("  Conséquence pratique : le bestiaire hérité de l'ancien système est")
    print("  légèrement TROP DUR à haut niveau, puisque les héros y réussissent moins")
    print("  souvent qu'à l'époque du calibrage. C'est le premier endroit à regarder")
    print("  si les playtests de haut niveau se révèlent trop meurtriers.")


# ---------------------------------------------------------------------------

SECTIONS = {
    "courbe": section_courbe,
    "marginal": section_marginal,
    "progression": section_progression,
    "rangs": section_rangs,
    "depenses": section_depenses,
    "degats": section_degats,
    "combat": section_combat,
    "groupe": section_groupe,
    "solo": section_solo,
    "matrice": section_combat_matrice,
    "letalite": section_letalite,
    "archive": section_archive,
}


def main() -> None:
    args = [a for a in sys.argv[1:] if a in SECTIONS]
    if sys.argv[1:] and not args:
        print(f"Sections : {', '.join(SECTIONS)}")
        return
    print("=" * 78)
    print(" PALANTÍR RPG — harnais de calibrage")
    print("=" * 78)
    for name in (args or SECTIONS):
        SECTIONS[name]()


if __name__ == "__main__":
    main()
