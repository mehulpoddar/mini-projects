#!/usr/bin/env python3
from __future__ import annotations

"""Render Muniverse cards to print-ready PDF files."""

import json
import argparse
import os
import sys
import tempfile
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from PIL import Image
from playwright.sync_api import sync_playwright

from deck_stats import print_deck_stats

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "cards.json"
TEMPLATES_DIR = BASE_DIR / "templates"
ART_DIR = BASE_DIR / "assets" / "art"
OUTPUT_DIR = BASE_DIR / "output"
CARD_BACK = ART_DIR / "card-back.png"

ART_EXTENSIONS = [".png", ".jpg", ".jpeg", ".webp"]

# Minimum dimensions for print quality (300 DPI at card size)
MIN_DIMENSIONS = {
    "standard": (1800, 1500),       # 6:5 landscape
    "full_art_rare": (1500, 2100),  # 5:7 portrait
}


def load_cards():
    with open(DATA_FILE) as f:
        return json.load(f)


def find_art(card_id: str) -> Path | None:
    """Find art file for a card, return its path."""
    for ext in ART_EXTENSIONS:
        path = ART_DIR / f"{card_id}{ext}"
        if path.exists():
            return path
    return None


def validate_art(cards: list[dict]) -> bool:
    """Validate all cards have art with sufficient dimensions. Returns True if valid."""
    errors = []

    for card in cards:
        art_path = find_art(card["id"])
        if art_path is None:
            errors.append(f"  {card['id']}: missing art (expected in {ART_DIR}/{card['id']}.<ext>)")
            continue

        try:
            with Image.open(art_path) as img:
                w, h = img.size
        except Exception as e:
            errors.append(f"  {card['id']}: could not read {art_path.name} ({e})")
            continue

        rarity = card["rarity"]
        min_w, min_h = MIN_DIMENSIONS.get(rarity, (0, 0))

        if rarity == "standard":
            actual_w, actual_h = max(w, h), min(w, h)
        else:
            actual_w, actual_h = min(w, h), max(w, h)

        if actual_w < min_w or actual_h < min_h:
            errors.append(
                f"  {card['id']}: {w}×{h}px — below minimum {min_w}×{min_h}px for {rarity}"
            )

    if errors:
        print(f"Validation failed ({len(errors)} error(s)):\n")
        for err in errors:
            print(err)
        print(f"\nFix all errors before rendering. No PDFs were generated.")
        return False

    print(f"Validated {len(cards)} card(s) — all art present and meets print resolution.")
    return True


def render_cards(card_ids: list[str] | None = None, merge: bool = False, back: bool = False, skip_validation: bool = False):
    data = load_cards()
    cards = data["cards"]

    if not cards:
        print("No cards in deck.")
        return

    if card_ids:
        found = [c for c in cards if c["id"] in card_ids]
        missing = set(card_ids) - {c["id"] for c in found}
        if missing:
            print(f"Warning: card IDs not found: {', '.join(missing)}")
        cards = found
        if not cards:
            return

    # Validate all art before rendering anything
    if skip_validation:
        print("Skipping art validation (--skip-validation)")
    elif not validate_art(cards):
        sys.exit(1)

    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    pdf_paths = []

    with sync_playwright() as p:
        browser = p.chromium.launch()

        for card in cards:
            template_name = (
                "full-art-rare.html"
                if card["rarity"] == "full_art_rare"
                else "standard.html"
            )
            template = env.get_template(template_name)
            art_path = find_art(card["id"])
            art_uri = f"file://{art_path.resolve()}"
            html = template.render(card=card, art_path=art_uri)

            tmp_fd, tmp_path = tempfile.mkstemp(suffix=".html", dir=str(OUTPUT_DIR))
            try:
                with os.fdopen(tmp_fd, "w") as tmp:
                    tmp.write(html)

                page = browser.new_page()
                page.goto(f"file://{tmp_path}")
                page.wait_for_load_state("networkidle")

                pdf_path = OUTPUT_DIR / f"{card['id']}.pdf"
                page.pdf(
                    path=str(pdf_path),
                    width="2.5in",
                    height="3.5in",
                    margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
                    print_background=True,
                )
                page.close()
                pdf_paths.append(pdf_path)

                print(f"  {card['id']} → {pdf_path.name}")
            finally:
                os.unlink(tmp_path)

        browser.close()

    if merge and len(pdf_paths) > 1:
        back_pdf = None
        if CARD_BACK.exists():
            with sync_playwright() as p2:
                b2 = p2.chromium.launch()
                back_pdf = _render_back_pdf(CARD_BACK, b2)
                b2.close()
            print(f"  card-back → {back_pdf.name}")
        else:
            print(f"  No card back found at {CARD_BACK.relative_to(BASE_DIR)} — merging without cover/backs")
        _merge_pdfs(pdf_paths, back_pdf, interleave_backs=back)
        for p in pdf_paths:
            p.unlink(missing_ok=True)
        if back_pdf:
            back_pdf.unlink(missing_ok=True)

    print(f"\nRendered {len(pdf_paths)} card(s) to {OUTPUT_DIR}/")


def _render_back_pdf(back_image: Path, browser) -> Path:
    """Render the card back image as a single-page PDF."""
    art_uri = f"file://{back_image.resolve()}"
    html = f"""<!DOCTYPE html>
<html><head><style>
  * {{ margin: 0; padding: 0; }}
  html, body {{ width: 2.5in; height: 3.5in; overflow: hidden; }}
  img {{ width: 100%; height: 100%; object-fit: cover; }}
  @page {{ size: 2.5in 3.5in; margin: 0; }}
</style></head>
<body><img src="{art_uri}"></body></html>"""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    tmp_fd, tmp_path = tempfile.mkstemp(suffix=".html", dir=str(OUTPUT_DIR))
    try:
        with os.fdopen(tmp_fd, "w") as tmp:
            tmp.write(html)

        page = browser.new_page()
        page.goto(f"file://{tmp_path}")
        page.wait_for_load_state("networkidle")

        pdf_path = OUTPUT_DIR / "card-back.pdf"
        page.pdf(
            path=str(pdf_path),
            width="2.5in",
            height="3.5in",
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            print_background=True,
        )
        page.close()
        return pdf_path
    finally:
        os.unlink(tmp_path)


def _merge_pdfs(pdf_paths: list[Path], back_pdf: Path | None = None, interleave_backs: bool = False):
    """Merge individual card PDFs into a single deck file.

    The card-back page (if available) is always added as the first page (cover).
    When interleave_backs is True, a card-back page is also inserted after every
    front page (useful for double-sided printing).
    """
    try:
        from pikepdf import Pdf
    except ImportError:
        print(
            "\nWarning: pikepdf not installed — skipping merge.\n"
            "Install it with: pip install pikepdf"
        )
        return

    back_src = None
    if back_pdf:
        back_src = Pdf.open(back_pdf)

    merged = Pdf.new()

    # Card-back as cover page
    if back_src:
        merged.pages.append(back_src.pages[0])

    for path in sorted(pdf_paths):
        with Pdf.open(path) as src:
            merged.pages.extend(src.pages)
        if interleave_backs and back_src:
            merged.pages.append(back_src.pages[0])

    merged_path = pdf_paths[0].parent / "muniverse-deck.pdf"
    merged.save(merged_path)
    if back_src:
        back_src.close()
    print(f"  Merged → {merged_path.name} ({len(merged.pages)} pages)")


def main():
    parser = argparse.ArgumentParser(
        description="Render Muniverse cards to print-ready PDFs",
        epilog="Examples:\n"
               "  python render_cards.py                  # all cards → individual PDFs\n"
               "  python render_cards.py hp-001 sc-003    # specific cards only\n"
               "  python render_cards.py --merge          # all cards + merged deck PDF (card-back as cover)\n"
               "  python render_cards.py --merge --back    # merged PDF with card-back interleaved for double-sided printing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "ids",
        nargs="*",
        help="Card IDs to render (default: all cards)",
    )
    parser.add_argument(
        "--merge",
        action="store_true",
        help="Merge all rendered cards into muniverse-deck.pdf (card-back as cover page)",
    )
    parser.add_argument(
        "--back",
        action="store_true",
        help="Interleave card-back after every front page in merged PDF (requires --merge)",
    )
    parser.add_argument(
        "--skip-validation",
        action="store_true",
        help="Skip art presence and dimension checks",
    )
    args = parser.parse_args()
    if args.back and not args.merge:
        parser.error("--back requires --merge")
    render_cards(args.ids if args.ids else None, merge=args.merge, back=args.back, skip_validation=args.skip_validation)
    print("\n" + "=" * 42)
    print("DECK BALANCE REPORT")
    print("=" * 42)
    print_deck_stats()


if __name__ == "__main__":
    main()
