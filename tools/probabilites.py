#!/usr/bin/env python3
"""
Palantír RPG — probabilités exactes du système d'attribut.

Système :
  Jet = 1d12 (dé du destin) + Nd6 (dés de bravoure, N = valeur d'attribut, 0..2).
  Réussite          : total >= SR (SR = 10 + 2*N).
  Réussite critique : d12 = 12 (toujours, même si total < SR).
  Échec critique    : d12 = 1  (toujours, même si total >= SR).
  Avantage          : 2d12, on garde le meilleur.
  Désavantage       : 2d12, on garde le pire.

Usage :
    python3 tools/probabilites.py
"""

from fractions import Fraction
from itertools import product
from typing import Dict, Optional


def d12_distribution(mode: str) -> Dict[int, Fraction]:
    """Probabilité de chaque face du d12 selon le mode."""
    if mode == "normal":
        return {v: Fraction(1, 12) for v in range(1, 13)}
    dist = {}
    op = max if mode == "advantage" else min
    for a, b in product(range(1, 13), repeat=2):
        v = op(a, b)
        dist[v] = dist.get(v, Fraction(0)) + Fraction(1, 144)
    return dist


def nd6_distribution(n: int) -> Dict[int, Fraction]:
    """Distribution de la somme de Nd6 (n = 0 → {0: 1})."""
    if n == 0:
        return {0: Fraction(1)}
    dist = {}
    for outcome in product(range(1, 7), repeat=n):
        s = sum(outcome)
        dist[s] = dist.get(s, Fraction(0)) + Fraction(1, 6**n)
    return dist


def analyze(attribute: int, mode: str = "normal", sr_override: Optional[int] = None) -> dict:
    """Calcule les probabilités d'un jet pour une valeur d'attribut donnée."""
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


def pct(f: Fraction) -> str:
    return f"{float(f) * 100:6.2f}%"


def print_table(mode: str) -> None:
    print(f"\nMode : {mode.upper()}")
    header = f"{'ATTR':<6}{'SR':<5}{'Crit ✗':>9}{'Échec':>9}{'Réussite':>11}{'Crit ✓':>9}{'Total ✓':>10}"
    print(header)
    print("-" * len(header))
    for attr in [0, 1, 2, 3]:
        r = analyze(attr, mode)
        print(
            f"{attr:<6}{r['sr']:<5}"
            f"{pct(r['crit_fail']):>9}"
            f"{pct(r['normal_fail']):>9}"
            f"{pct(r['normal_success']):>11}"
            f"{pct(r['crit_success']):>9}"
            f"{pct(r['success']):>10}"
        )


def print_defense_rule_comparison() -> None:
    """
    Compare deux interprétations de l'échec critique sur un jet de défense :
      A. Règle actuelle  : crit fail → jet de blessure (CON) → si raté, état Blessé.
      B. Règle proposée  : crit fail → état Blessé direct.
    """
    print("\n" + "=" * 72)
    print(" Échec critique en défense — règle actuelle vs proposée")
    print("=" * 72)
    print("  A. Actuelle  : crit fail (1/12) → jet de blessure (CON) → si raté, Blessé.")
    print("  B. Proposée  : crit fail (1/12) → Blessé direct.")
    print()
    crit = Fraction(1, 12)
    header = f"{'CON':<5}{'SR':<5}{'P(rater blessure)':>20}{'P(Blessé) A':>15}{'P(Blessé) B':>15}{'×':>5}"
    print(header)
    print("-" * len(header))
    for con in [0, 1, 2, 3]:
        r = analyze(con)
        p_fail = r["fail"]  # rater le jet de blessure
        a = crit * p_fail
        b = crit
        ratio = float(b / a) if a else float("inf")
        print(
            f"{con:<5}{r['sr']:<5}"
            f"{pct(p_fail):>20}"
            f"{pct(a):>15}"
            f"{pct(b):>15}"
            f"{ratio:>5.1f}"
        )
    print()
    print("Lecture : 'P(Blessé) B' est combien de fois plus élevé que 'A' (colonne ×).")
    print("Pour CON 2, la règle proposée rend l'état Blessé ≈ 3× plus fréquent")
    print("par défense ratée critique, donc beaucoup plus punitive.")


def main() -> None:
    print("=" * 72)
    print(" PALANTÍR RPG — Probabilités du jet d'attribut")
    print("=" * 72)
    for mode in ("normal", "advantage", "disadvantage"):
        print_table(mode)
    print_defense_rule_comparison()


if __name__ == "__main__":
    main()
