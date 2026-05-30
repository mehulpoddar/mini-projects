# Full Art Rare Card Template — Image Generation Prompt

Use this prompt template to generate artwork for **Full Art Rare** Muniverse cards. Replace the `{{placeholders}}` with values from the card's entry in `data/cards.json`.

**Card size:** 2.5" × 3.5" (63mm × 88mm) — standard poker card dimensions.
**Art orientation:** The artwork extends edge-to-edge (full bleed). Generate art in **5:7 portrait** orientation at **1500×2100px** minimum (print quality, 300 DPI).

---

## Prompt

```
Generate a single full-bleed illustration for a premium trading card.

**Image specifications:**
- Orientation: portrait (5:7 ratio)
- Resolution: 1500×2100px minimum (300 DPI print quality)
- The image will cover the entire physical 2.5" × 3.5" printed card edge-to-edge with text overlaid on top
- Ensure fine details and textures are crisp and will hold up at print resolution
- Leave the bottom ~30% slightly darker or less busy to allow stat overlays to remain readable

**Scene:**
{{art_description}}

**Style guidelines:**
- Painterly, cinematic quality — rich textures, atmospheric depth, dramatic lighting.
- Art style: high-detail illustration with subtle painterly brush strokes (not flat digital, not photorealistic).
- The scene should feel like a defining, unforgettable moment — elevated and epic.
- Use a strong focal point with the rest of the composition flowing around it.
- Color palette should be bold and intentional — use complementary or split-complementary schemes for visual impact.

**Card chrome (overlaid on art):**
- Card title: "{{title}}" — in an elegant, embossed gold or silver serif font, positioned at the bottom-center.
- Universe badge: a small translucent "{{universe}}" label in the top-right corner.
- Flavor text: "{{flavor_text}}" — in italic, subtly overlaid near the bottom with a gentle text shadow.
- Stat block: five compact stat icons along the bottom edge with semi-transparent background:
  Magic & Mystery: {{magic_and_mystery}}
  Power & Action: {{power_and_action}}
  Mind & Mischief: {{mind_and_mischief}}
  Heart & Soul: {{heart_and_soul}}
  Luck & Destiny: {{luck_and_destiny}}
- A subtle holographic or foil shimmer texture across the entire card surface.

**Do not** include any watermarks, signatures, or logos.
```
