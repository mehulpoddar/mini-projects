#!/usr/bin/env python3
"""Compute deck running totals and validate card stat totals from cards.json."""

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


def print_deck_stats():
    data = load_cards()
    cards = data["cards"]
    count = len(cards)

    if count == 0:
        print("Deck is empty — no cards yet.")
        return

    totals = running_totals(cards)
    grand_total = sum(totals.values())

    print(f"Total cards: {count}\n")
    print(f"{'Category':<22} {'Total':>7} {'Avg':>7}")
    print("-" * 38)
    for cat in CATEGORIES:
        label = cat.replace("_", " ").title()
        avg = totals[cat] / count
        print(f"{label:<22} {totals[cat]:>7} {avg:>7.1f}")
    print("-" * 38)
    print(f"{'Grand Total':<22} {grand_total:>7} {grand_total / count:>7.1f}")

    # Category balance check
    avg_total = grand_total / len(CATEGORIES)
    max_dev = max(abs(t - avg_total) for t in totals.values())
    print(f"\nCategory balance — ideal per-category total: {avg_total:.0f}, max deviation: {max_dev:.0f}")


def validate_stat_total(stats: dict) -> int:
    """Compute and return the correct stat_total for a stats dict."""
    return sum(stats[cat] for cat in CATEGORIES)


if __name__ == "__main__":
    print_deck_stats()
