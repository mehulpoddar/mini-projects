---
description: Generate new Muniverse trading cards and add them to cards.json
---

# Generate Muniverse Cards

## Pre-requisite

Before generating cards, read `muniverse/README.md` and `muniverse/data/cards.json` to understand the full game design, balancing rules, universes, and current deck state.

## Steps

1. **Validate the user's request**
   Before generating anything, check the request against the README's balancing rules. **Push back** if:
   - The request would create too many cards from one universe, skewing deck variety
   - The requested rarity mix doesn't make sense (e.g. too many Full Art Rares in one batch)
   - The request conflicts with any constraint in the README

   Explain the concern and suggest an alternative. Only proceed after the user confirms.

2. **Generate cards**
   Generate new cards based on the user's approved request.

   Each card must follow this schema:
   ```json
   {
     "id": "<universe_slug>-<incremental_number>",
     "title": "Card Title",
     "universe": "Universe Name",
     "rarity": "standard" | "full_art_rare",
     "art_description": "Detailed scene description for AI image generation. Compose for 6:5 landscape (standard) or 5:7 portrait (full_art_rare).",
     "flavor_text": "A memorable quote or flavor line",
     "scene_context": "A paragraph explaining the scene's narrative significance and relevance to its universe.",
     "stats": {
       "magic_and_mystery": 0,
       "power_and_action": 0,
       "mind_and_mischief": 0,
       "heart_and_soul": 0,
       "luck_and_destiny": 0
     },
     "stat_total": 0
   }
   ```

   **Do NOT compute `stat_total` yourself.** Leave it as 0 — it will be validated and filled by the script in step 3.

   Follow the README's balancing constraints (stat caps, stereotype-breaking, specialist/generalist mix). **Score stats authentically based on the scene** — do not artificially adjust stats for deck-wide balance. Present the generated cards to the user for review before proceeding.

3. **Validate stat totals and append to cards.json**
   After user approval, for each new card, compute the correct `stat_total` by running:
   ```
   python3 -c "
   import json, sys
   sys.path.insert(0, 'muniverse/scripts')
   from deck_stats import validate_stat_total, CATEGORIES
   stats = <PASTE_STATS_DICT_HERE>
   total = validate_stat_total(stats)
   print(f'stat_total: {total}')
   "
   ```
   Verify each total falls within the allowed range for its rarity (check `stat_caps` in `cards.json`). If any card is out of range, fix the stats before appending.

   Then append the new card objects (with correct `stat_total`) to the `cards` array in `muniverse/data/cards.json`. Preserve all existing cards. Ensure the file is valid JSON after writing.

4. **Validate deck and print stats**
// turbo
   Run the validation script to check stat caps, category hierarchy, and flag high-MiM cards:
   ```
   python3 muniverse/scripts/deck_stats.py
   ```
   The script will **exit with error** if:
   - Any card's `stat_total` is outside its rarity cap
   - The category hierarchy is violated (LD > HS > MM > PA > MiM)

   If validation fails, fix the offending cards before proceeding. Review any high-MiM cards (≥70) to confirm they involve genuine cunning/scheming — see README § "Category Hierarchy" for the MiM scoring rule.