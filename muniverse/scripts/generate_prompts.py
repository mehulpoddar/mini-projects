#!/usr/bin/env python3
from __future__ import annotations

"""Generate ready-to-paste image prompts for all Muniverse cards.

Reads cards.json and builds a complete prompt for each card using the
style/composition guidelines from the prompt templates. Outputs a single
markdown file with numbered, ready-to-paste prompts.

The prompts intentionally exclude card chrome (title text, stats, flavor
text, borders) because those are rendered by the HTML/CSS templates in
render_cards.py. The AI should generate scene art only.

Usage:
    python scripts/generate_prompts.py                # all cards
    python scripts/generate_prompts.py --ids hp-001 sc-003  # specific cards
    python scripts/generate_prompts.py --rarity standard    # filter by rarity
"""

import json
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "cards.json"
OUTPUT_DIR = BASE_DIR / "output"

# ---------------------------------------------------------------------------
# Prompt templates — scene + style only, no card chrome.
# Based on prompts/standard-card.md and prompts/full-art-rare.md but with
# text/chrome sections stripped (handled by HTML templates at render time).
# ---------------------------------------------------------------------------

STANDARD_PROMPT = """\
Generate a single illustration for a trading card.

**Image specifications:**
- Orientation: landscape (6:5 ratio)
- Resolution: 1800×1500px minimum
- The image will be printed inside a bordered frame on a physical 2.5" × 3.5" card
- Ensure fine details are crisp and will hold up at print resolution

**Scene:**
{art_description}

**Style guidelines:**
- Vibrant, saturated colors with clean linework.
- The scene should feel dynamic and alive — capture motion, emotion, or tension.
- Art style: semi-realistic anime / illustration hybrid (not photorealistic, not chibi).
- Lighting should emphasize the mood of the scene (warm for emotional moments, cool/dramatic for action).

**Do not** include any text, titles, labels, borders, frames, watermarks, signatures, or logos in the image. The image should contain scene artwork only — all text and borders are added separately.\
"""

FULL_ART_RARE_PROMPT = """\
Generate a single full-bleed illustration for a premium trading card.

**Image specifications:**
- Orientation: portrait (5:7 ratio)
- Resolution: 1500×2100px minimum
- The image will cover the entire physical 2.5" × 3.5" printed card edge-to-edge
- Ensure fine details and textures are crisp and will hold up at print resolution
- Leave the bottom ~30% slightly darker or less busy to allow overlaid elements to remain readable

**Scene:**
{art_description}

**Style guidelines:**
- Painterly, cinematic quality — rich textures, atmospheric depth, dramatic lighting.
- Art style: high-detail illustration with subtle painterly brush strokes (not flat digital, not photorealistic).
- The scene should feel like a defining, unforgettable moment — elevated and epic.
- Use a strong focal point with the rest of the composition flowing around it.
- Color palette should be bold and intentional — use complementary or split-complementary schemes for visual impact.

**Do not** include any text, titles, labels, borders, frames, watermarks, signatures, or logos in the image. The image should contain scene artwork only — all text and borders are added separately.\
"""


def load_cards():
    with open(DATA_FILE) as f:
        return json.load(f)


def build_prompt(card: dict) -> str:
    """Build a complete prompt for a single card."""
    template = (
        FULL_ART_RARE_PROMPT
        if card["rarity"] == "full_art_rare"
        else STANDARD_PROMPT
    )
    return template.format(art_description=card["art_description"])


def generate_prompts(
    card_ids: list[str] | None = None,
    rarity: str | None = None,
):
    data = load_cards()
    cards = data["cards"]

    if card_ids:
        cards = [c for c in cards if c["id"] in card_ids]
        missing = set(card_ids) - {c["id"] for c in cards}
        if missing:
            print(f"Warning: card IDs not found: {', '.join(sorted(missing))}")

    if rarity:
        cards = [c for c in cards if c["rarity"] == rarity]

    if not cards:
        print("No matching cards found.")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Build markdown file with all prompts
    lines = [
        "# Muniverse Card Art Prompts\n",
        f"**Total prompts:** {len(cards)}\n",
        "Generated from `data/cards.json`. Paste each prompt into "
        "[Gemini app](https://gemini.google.com) chat to generate card art.\n",
        "Save each image to `assets/art/` named by card ID.\n",
        "---\n",
    ]

    for i, card in enumerate(cards, 1):
        rarity_label = (
            "Full Art Rare" if card["rarity"] == "full_art_rare" else "Standard"
        )
        aspect = "5:7 portrait" if card["rarity"] == "full_art_rare" else "6:5 landscape"
        prompt = build_prompt(card)

        lines.append(f"## {i}. `{card['id']}` — {card['title']} ({rarity_label})\n")
        lines.append(f"**Universe:** {card['universe']} · **Aspect ratio:** {aspect}\n")
        lines.append(f"**Save as:** `{card['id']}.png`\n")
        lines.append("```")
        lines.append(prompt)
        lines.append("```\n")
        lines.append("---\n")

    prompts_path = OUTPUT_DIR / "prompts.md"
    with open(prompts_path, "w") as f:
        f.write("\n".join(lines))

    print(f"Generated {len(cards)} prompt(s) → {prompts_path}")
    print(
        f"\nWorkflow:\n"
        f"  1. Open {prompts_path.name} and paste each prompt into Gemini app chat\n"
        f"  2. Save each image to assets/art/ named by card ID (e.g. hp-001.png)\n"
        f"  3. Run: python scripts/render_cards.py"
    )


def main():
    parser = argparse.ArgumentParser(
        description="Generate image prompts for Muniverse card art",
        epilog="Examples:\n"
               "  python scripts/generate_prompts.py                    # all cards\n"
               "  python scripts/generate_prompts.py --ids hp-001 sc-003  # specific cards\n"
               "  python scripts/generate_prompts.py --rarity full_art_rare  # rare cards only",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--ids",
        nargs="*",
        help="Card IDs to generate prompts for (default: all cards)",
    )
    parser.add_argument(
        "--rarity",
        choices=["standard", "full_art_rare"],
        help="Filter cards by rarity",
    )
    args = parser.parse_args()
    generate_prompts(card_ids=args.ids, rarity=args.rarity)


if __name__ == "__main__":
    main()
