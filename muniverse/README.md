# Muniverse

A cross-universe trading card game where iconic scenes from Mu's favourite fictional worlds collide.

## Mu Universes

- The Bad Boy's Girl
- Mu
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

### Scene-Specific Scoring (Non-Negotiable)
**Stats must be scored authentically based on what happens in the specific scene — this is the highest priority and absolutely non-negotiable.** Never score by universe stereotype or general character traits. Every stat must be justified by what is actually happening in that moment.

Example: *"Hermione punching Draco"* scores high in Power & Action but low in Magic & Mystery — despite being set at Hogwarts. A Shinchan moment might surprise with a massive Heart & Soul score if the scene is genuinely emotional.

### Total Stat Cap
- **Standard card**: total stat sum ~250–270
- **Full Art Rare**: total stat sum ~280–300

Cards should have **2–3 competitive stats** (55–80 range) alongside clear weaknesses. This creates real choice when calling a category — no card should have a single obvious "always pick this" stat.

### Natural Imbalance
The deck will naturally develop category imbalances from authentic scene-based scoring. This is desirable — it makes certain stats rarer and more strategic. Run `deck_stats.py` after any card changes to review deck-wide averages. If adjustments are needed, make them by adding or swapping scenes — not by tweaking individual card stats.

### Mix Specialists and Generalists
Include specialist cards (2–3 spike stats, weak everywhere else) alongside generalist "Jack-of-all-Trades" cards (~40–50 across the board). Generalists are safe defensive plays; specialists are high-risk, high-reward.

### Rarity Distribution
Target ratio of **~4:1** — roughly 4 Standard cards for every 1 Full Art Rare. Full Art Rares should feel genuinely special and be reserved for the most iconic moments in each universe.

---

## Project Structure

```
.windsurf/workflows/
└── generate-cards.md          # Windsurf workflow for card generation

muniverse/
├── README.md
├── BUILD.md                   # Setup, art generation, rendering & printing guide
├── requirements.txt           # Python dependencies (jinja2, playwright, pikepdf, Pillow)
├── assets/
│   └── art/                   # Upscaled card art images, named <card-id>.png
│       └── raw/               # Raw downloaded images (git-ignored, input to upscaler)
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
│   ├── upscale_art.py         # Upscales undersized art with Real-ESRGAN
│   └── render_cards.py        # Validates art + renders print-ready PDFs
└── templates/
    ├── standard.html          # HTML/CSS card template — bordered layout
    └── full-art-rare.html     # HTML/CSS card template — full bleed layout
```

All card data lives in `data/cards.json`. Use the **`/generate-cards`** Windsurf workflow to create new cards.

Card art images are stored in `assets/art/`, named by card ID (e.g. `hp-001.png`).

**See [BUILD.md](BUILD.md) for setup, art generation, upscaling, rendering, and printing instructions.**