#!/usr/bin/env python3
"""Compute deck running totals, validate card stat totals, and enforce
the category hierarchy from cards.json."""

import json
import sys
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "cards.json"
CATEGORIES = [
    "magic_and_mystery",
    "power_and_action",
    "mind_and_mischief",
    "heart_and_soul",
    "luck_and_destiny",
]

# Enforced category hierarchy (highest → lowest by deck-wide average).
# See README § "Category Hierarchy (Enforced Imbalance)".
HIERARCHY = [
    "luck_and_destiny",
    "heart_and_soul",
    "magic_and_mystery",
    "power_and_action",
    "mind_and_mischief",
]

# MiM threshold — flag cards with MiM >= this value for manual review
MIM_HIGH_THRESHOLD = 70


def load_cards():
    with open(DATA_FILE) as f:
        return json.load(f)


def running_totals(cards):
    totals = {cat: 0 for cat in CATEGORIES}
    for card in cards:
        for cat in CATEGORIES:
            totals[cat] += card["stats"][cat]
    return totals


def validate_hierarchy(totals, count):
    """Check that deck averages follow the enforced hierarchy.
    Returns (ok, violations) where violations is a list of strings."""
    avgs = {cat: totals[cat] / count for cat in CATEGORIES}
    violations = []
    for i in range(len(HIERARCHY) - 1):
        higher = HIERARCHY[i]
        lower = HIERARCHY[i + 1]
        if avgs[higher] <= avgs[lower]:
            h_label = higher.replace("_", " ").title()
            l_label = lower.replace("_", " ").title()
            violations.append(
                f"{h_label} ({avgs[higher]:.1f}) must be > "
                f"{l_label} ({avgs[lower]:.1f})"
            )
    return len(violations) == 0, violations


def find_high_mim_cards(cards):
    """Return cards with MiM >= threshold for review."""
    return [
        card for card in cards
        if card["stats"]["mind_and_mischief"] >= MIM_HIGH_THRESHOLD
    ]


def validate_stat_caps(data):
    """Check each card's stat_total is within its rarity cap.
    Returns (ok, errors)."""
    caps = data["stat_caps"]
    errors = []
    for card in data["cards"]:
        total = sum(card["stats"][cat] for cat in CATEGORIES)
        rarity = card["rarity"]
        lo, hi = caps[rarity]["min"], caps[rarity]["max"]
        stored = card["stat_total"]
        if total != stored:
            errors.append(f"{card['id']}: computed={total} != stored={stored}")
        elif total < lo or total > hi:
            errors.append(f"{card['id']}: total={total} out of range {lo}-{hi}")
    return len(errors) == 0, errors


def print_deck_stats():
    data = load_cards()
    cards = data["cards"]
    count = len(cards)

    if count == 0:
        print("Deck is empty — no cards yet.")
        return

    totals = running_totals(cards)
    grand_total = sum(totals.values())
    avgs = {cat: totals[cat] / count for cat in CATEGORIES}

    # --- Category totals ---
    print(f"Total cards: {count}\n")
    rank = sorted(CATEGORIES, key=lambda c: avgs[c], reverse=True)
    print(f"{'#':<3} {'Category':<22} {'Total':>7} {'Avg':>7}")
    print("-" * 42)
    for i, cat in enumerate(rank, 1):
        label = cat.replace("_", " ").title()
        print(f"{i:<3} {label:<22} {totals[cat]:>7} {avgs[cat]:>7.1f}")
    print("-" * 42)
    print(f"    {'Grand Total':<22} {grand_total:>7} {grand_total / count:>7.1f}")

    # --- Hierarchy check ---
    ok, violations = validate_hierarchy(totals, count)
    print()
    if ok:
        print("✓ Category hierarchy holds")
    else:
        print("✗ Category hierarchy VIOLATED:")
        for v in violations:
            print(f"  - {v}")

    # --- Stat cap check ---
    caps_ok, cap_errors = validate_stat_caps(data)
    if caps_ok:
        print("✓ All stat totals within caps")
    else:
        print("✗ Stat cap errors:")
        for e in cap_errors:
            print(f"  - {e}")

    # --- High MiM review ---
    high_mim = find_high_mim_cards(cards)
    print(f"\nHigh MiM cards (≥{MIM_HIGH_THRESHOLD}): {len(high_mim)}")
    for card in high_mim:
        mim = card["stats"]["mind_and_mischief"]
        print(f"  {card['id']:>8}  MiM={mim:>3}  {card['title']}")

    # Exit with error if any validation failed
    if not ok or not caps_ok:
        sys.exit(1)


def validate_stat_total(stats: dict) -> int:
    """Compute and return the correct stat_total for a stats dict."""
    return sum(stats[cat] for cat in CATEGORIES)


if __name__ == "__main__":
    print_deck_stats()
