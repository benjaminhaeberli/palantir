#!/usr/bin/env python3
"""
Palantír RPG — harnais de calibrage du système de résolution.

Toutes les probabilités sont EXACTES (Fraction, pas de Monte-Carlo) : on arbitre
des écarts de 2-3 points, une simulation ne serait pas assez fine.

Trois familles de systèmes sont modélisées :

  S0 — ACTUEL (étalon)
      Jet = 1d12 (dé du destin) + Nd6 (dés de bravoure, N = attribut).
      Réussite          : total >= SR (SR = 10 + 2*N).
      Réussite critique : d12 = 12 (toujours, même si total < SR).
      Échec critique    : d12 = 1  (toujours, même si total >= SR).
      → C'est le système à remplacer : il impose une addition à chaque jet.

  S1 — DESTIN + RATTRAPAGE
      Réussite si d12 >= T (seuil constant, jamais annoncé par le MJ)
      OU si au moins un 6 sort des dés de bravoure. Aucune addition.
      Le d12 garde son rôle de destin et de critique, les d6 portent la compétence.

  S2 — POOL PUR (façon Year Zero)
      Réussite si au moins un 6 sur (attribut + dés de base) d6.
      Le d12 ne sert plus qu'aux critiques — ou disparaît (`fate_die=False`),
      auquel cas les critiques peuvent venir du pool (`crit_from_pool=True`).

Dans S1 comme S2, la difficulté ne passe JAMAIS par un nombre annoncé : elle se
règle en ajoutant ou retirant des d6 (objet, aide d'un compagnon, situation).

Usage :
    python3 tools/probabilites.py
"""

from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from typing import Dict, List, Optional

MODES = ("normal", "advantage", "disadvantage")

# Tableau de progression — src/content/regles/11-heros.md:46-53
PA_BY_LEVEL = {1: 1, 2: 2, 3: 2, 4: 3, 5: 3, 6: 4}


# ---------------------------------------------------------------------------
# Briques de base (conservées telles quelles : elles définissent l'étalon S0)
# ---------------------------------------------------------------------------


def d12_distribution(mode: str) -> Dict[int, Fraction]:
    """Probabilité de chaque face du d12 selon le mode."""
    if mode == "normal":
        return {v: Fraction(1, 12) for v in range(1, 13)}
    dist: Dict[int, Fraction] = {}
    op = max if mode == "advantage" else min
    for a, b in product(range(1, 13), repeat=2):
        v = op(a, b)
        dist[v] = dist.get(v, Fraction(0)) + Fraction(1, 144)
    return dist


def nd6_distribution(n: int) -> Dict[int, Fraction]:
    """Distribution de la somme de Nd6 (n = 0 → {0: 1})."""
    if n == 0:
        return {0: Fraction(1)}
    dist: Dict[int, Fraction] = {}
    for outcome in product(range(1, 7), repeat=n):
        s = sum(outcome)
        dist[s] = dist.get(s, Fraction(0)) + Fraction(1, 6 ** n)
    return dist


def analyze(attribute: int, mode: str = "normal", sr_override: Optional[int] = None) -> dict:
    """Système ACTUEL (S0) : 1d12 + Nd6 >= SR. Sert d'étalon de comparaison."""
    sr = sr_override if sr_override is not None else 10 + 2 * attribute
    d12 = d12_distribution(mode)
    d6s = nd6_distribution(attribute)

    p_crit_success = Fraction(0)
    p_crit_fail = Fraction(0)
    p_success = Fraction(0)  # inclut crits réussis
    p_fail = Fraction(0)     # inclut crits ratés

    for d12_val, p12 in d12.items():
        for sum_d6, p6 in d6s.items():
            total = d12_val + sum_d6
            joint = p12 * p6
            if d12_val == 12:
                p_crit_success += joint
                p_success += joint
            elif d12_val == 1:
                p_crit_fail += joint
                p_fail += joint
            elif total >= sr:
                p_success += joint
            else:
                p_fail += joint

    return {
        "sr": sr,
        "crit_success": p_crit_success,
        "success": p_success,
        "normal_success": p_success - p_crit_success,
        "fail": p_fail,
        "normal_fail": p_fail - p_crit_fail,
        "crit_fail": p_crit_fail,
    }


# ---------------------------------------------------------------------------
# Systèmes candidats
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class System:
    """Un système candidat entièrement paramétré."""

    name: str
    family: str                          # "S0" | "S1" | "S2"
    fate_threshold: int = 10             # T — seuil du d12 (S1)
    d6_success: int = 6                  # face minimale qui sauve le jet (6, ou 5 pour "5-6")
    base_dice: int = 0                   # dés ajoutés au pool en plus de l'attribut
    six_rescues_natural_one: bool = False  # un 6 annule-t-il l'échec critique ?
    advantage_mode: str = "d12"          # "d12" (2d12 garde le meilleur) ou "d6" (±1 dé)
    fate_die: bool = True                # S2 : lance-t-on encore le d12 pour les critiques ?
    crit_from_pool: bool = False         # S2 sans d12 : réussite critique sur 2+ succès

    def label(self) -> str:
        bits: List[str] = []
        if self.family == "S1":
            bits.append(f"T={self.fate_threshold}")
        if self.d6_success != 6:
            bits.append(f"succès sur {self.d6_success}-6")
        if self.base_dice:
            bits.append(f"+{self.base_dice} dé(s) de base")
        if self.six_rescues_natural_one:
            bits.append("le 6 sauve le 1")
        if self.advantage_mode == "d6":
            bits.append("avantage = ±1d6")
        if self.family == "S2" and not self.fate_die:
            bits.append("sans d12")
        if self.crit_from_pool:
            bits.append("crit sur 2+ succès")
        return f"{self.name} ({', '.join(bits)})" if bits else self.name


BASELINE = System(name="S0 — actuel", family="S0")


def pool_size(system: System, attribute: int, mode: str) -> int:
    """Nombre de d6 lancés, une fois les modificateurs appliqués."""
    n = attribute + system.base_dice
    if system.advantage_mode == "d6":
        if mode == "advantage":
            n += 1
        elif mode == "disadvantage":
            n -= 1
    return max(n, 0)


def p_no_rescue(system: System, n: int) -> Fraction:
    """Probabilité qu'aucun dé du pool ne sauve le jet."""
    return Fraction(system.d6_success - 1, 6) ** n


def p_at_least_two(system: System, n: int) -> Fraction:
    """Probabilité d'obtenir au moins deux succès (réussite critique au pool)."""
    p_s = Fraction(7 - system.d6_success, 6)
    p_f = 1 - p_s
    if n == 0:
        return Fraction(0)
    exactly_one = n * p_s * (p_f ** (n - 1))
    return 1 - (p_f ** n) - exactly_one


def profile(system: System, attribute: int, mode: str = "normal") -> dict:
    """Profil de résultats d'un jet : réussite, échec et critiques."""
    if system.family == "S0":
        return analyze(attribute, mode)

    n = pool_size(system, attribute, mode)
    none = p_no_rescue(system, n)
    any_rescue = 1 - none

    success = Fraction(0)
    fail = Fraction(0)
    crit_success = Fraction(0)
    crit_fail = Fraction(0)

    if system.family == "S2" and not system.fate_die:
        # Pool seul : plus de dé du destin, donc plus d'échec critique.
        success = any_rescue
        fail = none
        if system.crit_from_pool:
            crit_success = p_at_least_two(system, n)
        return _pack(success, fail, crit_success, crit_fail)

    d12_mode = "normal" if system.advantage_mode == "d6" else mode
    for v, p12 in d12_distribution(d12_mode).items():
        if v == 12:
            success += p12
            crit_success += p12
        elif v == 1:
            if system.six_rescues_natural_one:
                success += p12 * any_rescue
                fail += p12 * none
                crit_fail += p12 * none
            else:
                fail += p12
                crit_fail += p12
        elif system.family == "S1" and v >= system.fate_threshold:
            # Le destin tranche seul : les d6 ne sont plus consultés.
            success += p12
        else:
            success += p12 * any_rescue
            fail += p12 * none

    if system.crit_from_pool:
        # Les critiques du pool s'ajoutent à celles du d12 sur les faces neutres.
        crit_success += (1 - Fraction(1, 12)) * p_at_least_two(system, n)

    return _pack(success, fail, crit_success, crit_fail)


def _pack(success: Fraction, fail: Fraction, crit_success: Fraction, crit_fail: Fraction) -> dict:
    return {
        "sr": None,
        "success": success,
        "fail": fail,
        "crit_success": crit_success,
        "crit_fail": crit_fail,
        "normal_success": success - crit_success,
        "normal_fail": fail - crit_fail,
    }


# ---------------------------------------------------------------------------
# Sorties
# ---------------------------------------------------------------------------


def pct(f: Fraction) -> str:
    return f"{float(f) * 100:6.2f}%"


def print_system_table(system: System, attributes=range(0, 7)) -> None:
    """Sortie 1, 4 et 5 : courbe complète, tenue en haut, viabilité de l'attribut 0."""
    print(f"\n### {system.label()}")
    for mode in MODES:
        print(f"\n  Mode : {mode}")
        header = (
            f"  {'ATTR':<6}{'SR':<5}{'Crit ✗':>9}{'Échec':>9}"
            f"{'Réussite':>11}{'Crit ✓':>9}{'Total ✓':>10}"
        )
        print(header)
        print("  " + "-" * (len(header) - 2))
        for attr in attributes:
            r = profile(system, attr, mode)
            sr = str(r["sr"]) if r["sr"] is not None else "—"
            print(
                f"  {attr:<6}{sr:<5}"
                f"{pct(r['crit_fail']):>9}"
                f"{pct(r['normal_fail']):>9}"
                f"{pct(r['normal_success']):>11}"
                f"{pct(r['crit_success']):>9}"
                f"{pct(r['success']):>10}"
            )


def rms_deviation(system: System, attributes=(0, 1, 2, 3)) -> float:
    """Sortie 2 : écart quadratique moyen à S0, en points de pourcentage."""
    total = 0.0
    for attr in attributes:
        ref = float(profile(BASELINE, attr)["success"])
        cur = float(profile(system, attr)["success"])
        total += ((cur - ref) * 100) ** 2
    return (total / len(attributes)) ** 0.5


def advantage_is_effective(system: System) -> bool:
    """L'avantage change-t-il encore quelque chose ?

    Piège : en abandonnant le d12 tout en gardant « avantage = 2d12 garde le
    meilleur », l'avantage et le désavantage cessent silencieusement d'exister.
    """
    normal = profile(system, 2, "normal")["success"]
    adv = profile(system, 2, "advantage")["success"]
    return adv != normal


def crit_fail_drift(system: System) -> tuple:
    """Taux d'échec critique aux attributs 0 et 6.

    L'échec critique n'est pas décoratif : il ignore l'armure, brise les
    boucliers, déclenche les jets de blessure et détruit les catalyseurs. Un
    système qui l'érode à mesure que les héros montent en niveau désamorce la
    létalité du jeu sans le dire.
    """
    return (
        float(profile(system, 0)["crit_fail"]) * 100,
        float(profile(system, 6)["crit_fail"]) * 100,
    )


def sort_key(system: System) -> tuple:
    """Fidélité d'abord, puis pénalise un avantage devenu inopérant."""
    return (rms_deviation(system), 0 if advantage_is_effective(system) else 1)


def candidate_systems() -> List[System]:
    """Balayage complet des paramètres ouverts du plan."""
    out: List[System] = []
    for t, d6s, six_saves, adv in product(
        (9, 10, 11), (6, 5), (False, True), ("d12", "d6")
    ):
        out.append(
            System(
                name="S1 — destin + rattrapage",
                family="S1",
                fate_threshold=t,
                d6_success=d6s,
                six_rescues_natural_one=six_saves,
                advantage_mode=adv,
            )
        )
    for base, d6s, fate, adv in product((0, 1, 2), (6, 5), (True, False), ("d12", "d6")):
        out.append(
            System(
                name="S2 — pool pur",
                family="S2",
                base_dice=base,
                d6_success=d6s,
                fate_die=fate,
                crit_from_pool=not fate,
                advantage_mode=adv,
            )
        )
    return out


def print_ranking(top: int = 12) -> List[System]:
    """Sortie 2 : classement des combinaisons par fidélité à la courbe actuelle."""
    print("\n" + "=" * 78)
    print(" Classement par fidélité à la courbe actuelle (attributs 0→3)")
    print("=" * 78)
    ref = [float(profile(BASELINE, a)["success"]) * 100 for a in range(4)]
    ref_crit = crit_fail_drift(BASELINE)
    print(f"  Référence S0 : " + "  ".join(f"{v:5.1f}%" for v in ref)
          + f"   | crit ✗ {ref_crit[0]:.1f}→{ref_crit[1]:.1f}%")
    print()
    header = (
        f"  {'écart':>7}  {'0':>6}{'1':>6}{'2':>6}{'3':>6}"
        f"{'crit ✗ 0→6':>13}{'av.':>5}   système"
    )
    print(header)
    print("  " + "-" * (len(header) - 2))

    ranked = sorted(candidate_systems(), key=sort_key)
    for system in ranked[:top]:
        curve = [float(profile(system, a)["success"]) * 100 for a in range(4)]
        lo, hi = crit_fail_drift(system)
        print(
            f"  {rms_deviation(system):6.2f}   "
            + "".join(f"{v:5.1f} " for v in curve)
            + f"{f'{lo:.1f}→{hi:.1f}%':>13}"
            + f"{'✓' if advantage_is_effective(system) else '✗':>5}"
            + f"   {system.label()}"
        )
    print("\n  écart  = moyenne quadratique des écarts à S0, en points de %")
    print("  crit ✗ = taux d'échec critique, de l'attribut 0 à l'attribut 6")
    print("  av.    = l'avantage produit-il encore un effet ?")
    return ranked


def print_marginal_die(systems: List[System]) -> None:
    """Sortie 3 : ce que rapporte un dé de plus — lisibilité du bonus côté MJ."""
    print("\n" + "=" * 78)
    print(" Valeur marginale d'un d6 supplémentaire (points de % de réussite)")
    print("=" * 78)
    print("  Un modificateur lisible doit valoir à peu près la même chose partout.")
    print()
    header = f"  {'pool':>5}" + "".join(f"{f'{n}→{n+1}':>9}" for n in range(0, 6))
    print(header)
    print("  " + "-" * (len(header) - 2))
    for system in systems:
        gains = []
        for n in range(0, 6):
            a = float(profile(system, n)["success"])
            b = float(profile(system, n + 1)["success"])
            gains.append((b - a) * 100)
        print(f"  {'':>5}" + "".join(f"{g:8.1f} " for g in gains) + f"  {system.label()}")


def print_bravoure_generation(turns: int = 5) -> None:
    """
    Sortie 6 : Bravoure générée par combat.

    Un 6 donne 1 PB, donc l'espérance ne dépend que de la TAILLE DU POOL : elle est
    identique en S0 et en S1, et n'augmente qu'avec les dés d'objet ou d'aide.

    Le multiplicateur qu'on oublie, ce sont les jets de DÉFENSE : le MJ ne lance
    jamais de dés (08-combat.md:26), donc chaque attaque ennemie fait lancer le
    héros. Les atouts coûtent 1 à 2 PB (14-atouts.md).
    """
    print("\n" + "=" * 78)
    print(" Génération de Bravoure par combat")
    print("=" * 78)
    print("  Attribut principal supposé = 2 à la création, +1 par niveau.")
    print("  Jets par tour = PA (attaques) + attaques ennemies subies (défenses).")
    print("  « fin. » = effets renforcés finançables (2 PB pièce).")
    print()

    header = (
        f"  {'Niv':<5}{'Attr':<6}{'PA':<4}{'déf/t':>6}{'jets':>6}"
        f"{'PB (attribut seul)':>20}{'fin.':>7}"
        f"{'PB (+2 objet/aide)':>20}{'fin.':>7}"
    )
    print(header)
    print("  " + "-" * (len(header) - 2))
    for level in range(1, 7):
        attribute = 1 + level          # 2 au niveau 1, 7 au niveau 6
        pa = PA_BY_LEVEL[level]
        for defenses in (1, 2):
            rolls = turns * (pa + defenses)
            solo = Fraction(rolls * attribute, 6)
            boosted = Fraction(rolls * (attribute + 2), 6)
            head = (
                f"  {level:<5}{attribute:<6}{pa:<4}"
                if defenses == 1
                else f"  {'':<5}{'':<6}{'':<4}"
            )
            print(
                head
                + f"{defenses:>6}{rolls:>6}"
                + f"{float(solo):>20.1f}{float(solo) / 2:>6.1f}×"
                + f"{float(boosted):>20.1f}{float(boosted) / 2:>6.1f}×"
            )
    print(f"\n  (combat de {turns} tours)")


def print_bravoure_budget(turns: int = 4, fights: int = 2, party: int = 4) -> None:
    """
    Combien de PB un joueur gagne par séance, et ce que ça permet d'acheter.

    Sert à fixer le prix des dépenses : une dépense qui coûte moins que le revenu
    d'un tour devient le choix par défaut à chaque tour, donc plus un choix.
    """
    print("\n" + "=" * 78)
    print(f" Revenu de Bravoure — séance de {fights} combats de {turns} tours")
    print("=" * 78)
    print("  Hypothèse haute : le héros a investi toutes ses montées de niveau dans")
    print("  son attribut de combat (c'est lui qui sert aux attaques ET aux défenses).")
    print("  1 défense subie par tour.")
    print()

    header = (
        f"  {'Niv':<5}{'Attr':<6}{'jets/combat':>12}{'PB/tour':>9}"
        f"{'PB/combat':>11}{'PB/séance':>11}{'groupe de ' + str(party):>15}"
    )
    print(header)
    print("  " + "-" * (len(header) - 2))
    rows = []
    for level in range(1, 7):
        attribute = 1 + level
        rolls_per_turn = PA_BY_LEVEL[level] + 1
        pb_turn = Fraction(rolls_per_turn * attribute, 6)
        pb_fight = pb_turn * turns
        pb_session = pb_fight * fights
        rows.append((level, attribute, pb_turn, pb_fight, pb_session))
        print(
            f"  {level:<5}{attribute:<6}{rolls_per_turn * turns:>12}"
            f"{float(pb_turn):>9.1f}{float(pb_fight):>11.1f}"
            f"{float(pb_session):>11.1f}{float(pb_session * party):>15.1f}"
        )

    print("\n" + "-" * 78)
    print(" Quel prix pour « +1 PA » ? Combien de fois par combat un héros peut-il se le payer")
    print(" — à comparer au nombre de tours du combat (au-delà, c'est gratuit de fait).")
    print()
    prices = (2, 3, 4, 5)
    header = f"  {'Niv':<5}{'PB/combat':>11}" + "".join(f"{f'à {p} PB':>10}" for p in prices)
    print(header)
    print("  " + "-" * (len(header) - 2))
    for level, _attr, _pb_turn, pb_fight, _pb_session in rows:
        line = f"  {level:<5}{float(pb_fight):>11.1f}"
        for price in prices:
            times = float(pb_fight) / price
            flag = "  ⚠" if times >= turns else ""
            line += f"{times:>8.1f}×{flag:<1}" if flag else f"{times:>9.1f}×"
        print(line)
    print(f"\n  ⚠ = le héros peut se l'offrir à CHAQUE tour du combat ({turns} tours),")
    print("  donc ce n'est plus un arbitrage mais un bonus permanent.")


def print_defense_rule_comparison(system: System = BASELINE) -> None:
    """
    Létalité : échec critique en défense → jet de blessure.
      A. Règle actuelle  : crit fail → jet de blessure (CON) → si raté, état Blessé.
      B. Règle proposée  : crit fail → état Blessé direct.
    Dépend directement de P(échec), donc du système retenu.
    """
    print("\n" + "=" * 78)
    print(f" Échec critique en défense — règle actuelle vs proposée ({system.name})")
    print("=" * 78)
    print("  A. Actuelle  : crit fail (1/12) → jet de blessure (CON) → si raté, Blessé.")
    print("  B. Proposée  : crit fail (1/12) → Blessé direct.")
    print()
    crit = Fraction(1, 12)
    header = f"  {'CON':<5}{'P(rater blessure)':>20}{'P(Blessé) A':>15}{'P(Blessé) B':>15}{'×':>6}"
    print(header)
    print("  " + "-" * (len(header) - 2))
    for con in range(0, 4):
        p_fail = profile(system, con)["fail"]
        a = crit * p_fail
        b = crit
        ratio = float(b / a) if a else float("inf")
        print(f"  {con:<5}{pct(p_fail):>20}{pct(a):>15}{pct(b):>15}{ratio:>6.1f}")
    print()
    print("  Lecture : « × » indique combien de fois la règle B rend l'état Blessé")
    print("  plus fréquent que la règle A, par défense ratée critiquement.")


# ---------------------------------------------------------------------------


def main() -> None:
    print("=" * 78)
    print(" PALANTÍR RPG — calibrage du système de résolution")
    print("=" * 78)

    print_system_table(BASELINE, attributes=range(0, 5))

    ranked = print_ranking()

    best_s1 = next(s for s in ranked if s.family == "S1")
    best_s2 = next(s for s in ranked if s.family == "S2")

    print("\n" + "=" * 78)
    print(" Meilleur candidat de chaque famille, courbe complète")
    print("=" * 78)
    for system in (best_s1, best_s2):
        print_system_table(system)

    print_marginal_die([BASELINE, best_s1, best_s2])
    print_bravoure_generation()

    print_defense_rule_comparison(BASELINE)
    print_defense_rule_comparison(best_s1)


if __name__ == "__main__":
    main()
