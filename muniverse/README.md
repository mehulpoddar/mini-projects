# Muniverse

A cross-universe trading card game where iconic scenes from Mu's favourite fictional worlds collide.

## Mu Universes

- The Bad Boy's Girl
- Me Before You
- Shinchan
- Harry Potter
- Disney Cars
- Pokémon
- Mario

---

## Art Style

- **Pokémon TCG Aesthetics** — Visual layout mirrors classic trading cards with clear stat blocks, structured text areas, and dynamic, vibrant illustrations.
- **Scenes, not Characters** — The deck captures the full narrative by featuring complete memorable scenes or moments, not just isolated characters or objects.
- **Standard vs Full Art Rare** — Standard cards use traditional bordered layouts for important scenes. Full Art Rares feature edge-to-edge artwork reserved for the absolute pinnacle moments of a universe.

## Stat Categories

Every card is scored **1–100** across five traits:

| Category | Description |
|---|---|
| **Magic & Mystery** | Supernatural presence, wizardry, unexplainable phenomena, deep lore |
| **Power & Action** | Physical effort, dynamic movement, combat, sheer physical presence |
| **Mind & Mischief** | Cunning, strategic thinking, sharp wit, clever pranks or schemes |
| **Heart & Soul** | Emotional vulnerability, deep empathy, romantic devotion, pure love |
| **Luck & Destiny** | Plot armor, cosmic coincidences, accidental successes, fate |

## Gameplay

1. Shuffle the deck and deal equally between both players.
2. Players hold their cards in a stack, looking only at the top card.
3. **Player A** selects one of the five categories from their top card and reads the score aloud.
4. **Player B** reads the score of the same category from their top card.
5. The higher score wins the round — the winner takes both cards and places them at the bottom of their stack.
6. The winner chooses the category for the next turn.
7. The game ends when one player holds all the cards.

## Balancing Rules

### Break Universe Stereotypes
Stats must not be predictable by universe. Base them strictly on the specific scene. Example: *"Hermione punching Draco"* scores high in Power & Action but low in Magic & Mystery. A Shinchan moment might surprise with a massive Heart & Soul score.

### Total Stat Cap
- **Standard card**: total stat sum ~200–220
- **Full Art Rare**: total stat sum ~240

This forces real trade-offs — an 88 in Mind & Mischief means terrible scores elsewhere.

### Mix Specialists and Generalists
Include specialist cards (one spike stat, weak everywhere else) alongside generalist "Jack-of-all-Trades" cards (~40–50 across the board). Generalists are safe defensive plays; specialists are high-risk, high-reward.

### Global Deck Equilibrium
The sum total of all cards across the entire deck should be roughly equal per category. When new cards are added, their stats should intentionally fill existing deficits. Running totals are computed from `data/cards.json` automatically via the card generation workflow.

### Rarity Distribution
Target ratio of **~4:1** — roughly 4 Standard cards for every 1 Full Art Rare. Full Art Rares should feel genuinely special and be reserved for the most iconic moments in each universe.

---

## Project Structure

```
.windsurf/workflows/
└── generate-cards.md          # Windsurf workflow for card generation

muniverse/
├── README.md
├── requirements.txt           # Python dependencies (jinja2, playwright, pikepdf, Pillow)
├── assets/
│   └── art/                   # Card art images, named <card-id>.png
├── data/
│   └── cards.json             # All card data — single source of truth
├── output/                    # Generated card PDFs (git-ignored)
├── prompts/
│   ├── card-back.md           # 6 design concepts for the card back
│   ├── standard-card.md       # Image gen prompt for standard card art
│   └── full-art-rare.md       # Image gen prompt for full art rare art
├── scripts/
│   ├── deck_stats.py          # Deck running totals and stat validation
│   ├── generate_prompts.py    # Generates ready-to-paste AI image prompts
│   └── render_cards.py        # Validates art + renders print-ready PDFs
└── templates/
    ├── standard.html          # HTML/CSS card template — bordered layout
    └── full-art-rare.html     # HTML/CSS card template — full bleed layout
```

### Data Management

All card data lives in `data/cards.json`. Stats, running totals, and deck equilibrium are all derived directly from the JSON at generation time.

Use the **`/generate-cards`** Windsurf workflow (defined at `.windsurf/workflows/generate-cards.md` in the repo root) to create new cards. It automatically reads current deck totals from the JSON, generates cards with the LLM, and appends the results back to the JSON.

### Card Dimensions

All cards are sized to **2.5" × 3.5"** (63mm × 88mm) — standard poker card dimensions, designed for **physical printing at 300 DPI**.

| Rarity | Art Orientation | Art Ratio | Min Resolution (print) |
|---|---|---|---|
| Standard | Landscape (framed window) | 3:2 | 1800×1200px |
| Full Art Rare | Portrait (full bleed) | 5:7 | 1500×2100px |

### Card Art

Card art images are stored in `assets/art/`, named by card ID (e.g. `hp-001.png`). Each card in `cards.json` has an `art_description` field describing the scene. The prompt templates in `prompts/` provide style and composition guidelines for each rarity.

#### Art Generation Workflow

1. **Generate prompts** — builds ready-to-paste prompts from `cards.json` + style templates:
   ```bash
   python scripts/generate_prompts.py              # all cards
   python scripts/generate_prompts.py --ids hp-001  # specific card
   ```
   Output: `output/prompts.md` (numbered, ready-to-paste prompts).

2. **Generate images** — open [Google AI Studio](https://aistudio.google.com) and paste each prompt:
   - Set aspect ratio: **3:2 landscape** for Standard, **5:7 portrait** for Full Art Rare
   - Generate at **2K resolution** or higher for print quality
   - Save each image directly to `assets/art/` named by card ID (e.g. `hp-001.png`)

The prompts intentionally exclude card chrome (title, stats, flavor text, borders) because those are rendered by the HTML/CSS templates. The AI generates **scene art only**.

### Rendering & Printing

The render script validates that **all cards have art at print-quality resolution** before generating any PDFs. If any card is missing art or below the minimum dimensions, it fails immediately with a detailed error list.

It then uses Playwright (headless Chromium) to convert the HTML/CSS card templates into **print-ready PDFs** at exact card dimensions (2.5"×3.5").

```bash
# Setup (one-time)
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium

# Render all cards to individual PDFs
python scripts/render_cards.py

# Render specific cards
python scripts/render_cards.py hp-001 sc-003

# Render all + merge into a single deck PDF
python scripts/render_cards.py --merge

# Merge with card back interleaved (front, back, front, back, ...)
python scripts/render_cards.py --merge --back assets/art/card-back.png
```

Output goes to `output/` (git-ignored). Use `--merge` to produce a combined `muniverse-deck.pdf`. Add `--back <image>` to interleave a card back page after every front — ready for double-sided printing.

**Recommended stock:** 300gsm+ cardstock for best feel. Standard 80lb cover stock works well for home printing. For professional results, use a print service with 350gsm coated cardstock.