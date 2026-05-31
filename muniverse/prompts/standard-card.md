# Standard Card Template — Image Generation Prompt

Use this prompt template to generate artwork for **Standard** rarity Muniverse cards. Replace the `{{placeholders}}` with values from the card's entry in `data/cards.json`.

**Card size:** 2.5" × 3.5" (63mm × 88mm) — standard poker card dimensions.
**Art orientation:** The artwork sits inside a framed window on the card. Generate art in **6:5 landscape** orientation at **1800×1500px** minimum (print quality, 300 DPI).

---

## Prompt

```
Generate a single illustration for a trading card art window.

**Image specifications:**
- Orientation: landscape (6:5 ratio)
- Resolution: 1800×1500px minimum (300 DPI print quality)
- The image will be printed inside a bordered frame on a physical 2.5" × 3.5" card
- Ensure fine details are crisp and will hold up at print resolution

**Scene:**
{{art_description}}

**Style guidelines:**
- Vibrant, saturated colors with clean linework.
- The scene should feel dynamic and alive — capture motion, emotion, or tension.
- Art style: semi-realistic anime / illustration hybrid (not photorealistic, not chibi).
- Lighting should emphasize the mood of the scene (warm for emotional moments, cool/dramatic for action).

**Card chrome:**
- Border color: a muted silver or light grey.
- Card title: "{{title}}" — displayed in bold serif font below the artwork frame.
- Universe badge: a small "{{universe}}" label in the top-right corner of the card.
- Flavor text: "{{flavor_text}}" — in italic, below the title.
- Stat block at the bottom with five horizontal bars labeled:
  Magic & Mystery: {{magic_and_mystery}}
  Power & Action: {{power_and_action}}
  Mind & Mischief: {{mind_and_mischief}}
  Heart & Soul: {{heart_and_soul}}
  Luck & Destiny: {{luck_and_destiny}}

**Do not** include any watermarks, signatures, or logos.
```
