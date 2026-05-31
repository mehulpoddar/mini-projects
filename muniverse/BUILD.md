# Build Guide

End-to-end instructions for setting up the environment, generating card art, and rendering print-ready PDFs.

## Prerequisites

- Python 3.9+
- macOS (for Real-ESRGAN GPU acceleration on Apple Silicon)

## Setup (one-time)

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Install headless browser for PDF rendering
playwright install chromium
```

> **All commands below assume the venv is active.** Always run `source .venv/bin/activate` first.

### Real-ESRGAN (image upscaler)

The Gemini app generates images at ~1264×848px, which is below print-quality minimums. Real-ESRGAN upscales them with AI.

1. Download the macOS binary from [Real-ESRGAN-ncnn-vulkan releases](https://github.com/xinntao/Real-ESRGAN/releases) (get the `-macos.zip` under the latest release that includes models)
2. Extract and place somewhere permanent:
   ```bash
   mkdir -p ~/bin/realesrgan
   unzip realesrgan-ncnn-vulkan-*-macos.zip -d /tmp/realesrgan
   cp /tmp/realesrgan/realesrgan-ncnn-vulkan ~/bin/realesrgan/
   cp -r /tmp/realesrgan/models ~/bin/realesrgan/
   chmod +x ~/bin/realesrgan/realesrgan-ncnn-vulkan
   ```
3. Add to PATH (add to `~/.zshrc`):
   ```bash
   export PATH="$HOME/bin/realesrgan:$PATH"
   ```
4. Verify:
   ```bash
   realesrgan-ncnn-vulkan -h
   ```

---

## Workflow

> Activate the virtual environment before running any script:
> ```bash
> source .venv/bin/activate
> ```

### 1. Generate Cards

Use the **`/generate-cards`** Windsurf workflow (`.windsurf/workflows/generate-cards.md`) to create new cards. It reads current deck totals from `data/cards.json`, generates cards with the LLM, and appends them back.

### 2. Generate Art Prompts

Builds ready-to-paste prompts from `cards.json` + style templates:

```bash
# (inside .venv)
python scripts/generate_prompts.py              # all cards
python scripts/generate_prompts.py --ids hp-001  # specific card
```

Output: `output/prompts.md` (numbered, ready-to-paste prompts).

The prompts intentionally exclude card chrome (title, stats, flavor text, borders) because those are rendered by the HTML/CSS templates. The AI generates **scene art only**.

### 3. Generate Images

Open [Gemini app](https://gemini.google.com) and paste each prompt from `output/prompts.md`.

- Save each image to `assets/art/raw/` named by card ID (e.g. `hp-001.png`)
- The free tier uses Nano Banana 2 (~20 images/day)

### 4. Upscale Art

Upscale raw images with Real-ESRGAN (4x) before rendering:

```bash
# (inside .venv)
python scripts/upscale_art.py              # upscale all images in raw/
python scripts/upscale_art.py --ids hp-001  # upscale specific card(s)
```

The script:
- Reads images from `assets/art/raw/`
- Upscales each 4x and writes the result to `assets/art/`
- Raw originals are kept in `raw/` (git-ignored)

### 5. Render PDFs

The render script validates that **all cards have art at print-quality resolution** before generating any PDFs. If any card is missing art or below the minimum dimensions, it fails immediately with a detailed error list.

```bash
# (inside .venv)
python scripts/render_cards.py                    # all cards
python scripts/render_cards.py hp-001 sc-003       # specific cards
python scripts/render_cards.py --merge              # merge into single PDF (card back auto-included)
```

Output goes to `output/` (git-ignored). Use `--merge` to produce a combined `muniverse-deck.pdf`. If `assets/art/card-back.png` exists, it is automatically interleaved after every front page — ready for double-sided printing.

---

## Printing

**Recommended stock:** 300gsm+ cardstock for best feel. Standard 80lb cover stock works well for home printing. For professional results, use a print service with 350gsm coated cardstock.

### Card Dimensions

All cards are sized to **2.5" × 3.5"** (63mm × 88mm) — standard poker card dimensions, designed for **physical printing at 300 DPI**.

| Rarity | Art Orientation | Art Ratio | Min Resolution (print) |
|---|---|---|---|
| Standard | Landscape (framed window) | 6:5 | 1800×1500px |
| Full Art Rare | Portrait (full bleed) | 5:7 | 1500×2100px |
