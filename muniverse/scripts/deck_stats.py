#!/usr/bin/env python3
"""Compute deck running totals, validate card stat totals, and report
deck-wide category averages from cards.json."""

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


def load_cards():
    with open(DATA_FILE) as f:
        return json.load(f)


def running_totals(cards):
    totals = {cat: 0 for cat in CATEGORIES}
    for card in cards:
        for cat in CATEGORIES:
            totals[cat] += card["stats"][cat]
    return totals


def validate_stat_caps(data):
    """Check each card's computed stat total is within its rarity cap and
    no individual stat exceeds max_stat. Returns (ok, errors)."""
    caps = data["stat_caps"]
    max_stat = data.get("max_stat", 90)
    errors = []
    for card in data["cards"]:
        total = sum(card["stats"][cat] for cat in CATEGORIES)
        rarity = card["rarity"]
        lo, hi = caps[rarity]["min"], caps[rarity]["max"]
        if total < lo or total > hi:
            errors.append(f"{card['id']}: total={total} out of range {lo}-{hi}")
        for cat in CATEGORIES:
            if card["stats"][cat] > max_stat:
                label = cat.replace('_', ' ').title()
                errors.append(
                    f"{card['id']}: {label}={card['stats'][cat]} exceeds max {max_stat}"
                )
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

    print()

    # --- Stat cap check ---
    caps_ok, cap_errors = validate_stat_caps(data)
    if caps_ok:
        print("✓ All stat totals within caps")
    else:
        print("✗ Stat cap errors:")
        for e in cap_errors:
            print(f"  - {e}")

    # Exit with error if stat caps are violated
    if not caps_ok:
        sys.exit(1)


def validate_stat_total(stats: dict) -> int:
    """Compute and return the correct stat_total for a stats dict."""
    return sum(stats[cat] for cat in CATEGORIES)


if __name__ == "__main__":
    print_deck_stats()
