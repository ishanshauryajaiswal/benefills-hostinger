---
description: Content Workflow V2 - Instagram image post generation from competitor inspiration
---

# Content Workflow V2 — Instagram Image Post Generator

Generate brand-specific Instagram image posts for Benefills, inspired by competitor content. Images only (no video), but the architecture supports adding video later.

## Prerequisites

1. Python 3.10+ installed
2. API keys configured in `content/content_v2/.env`
3. Dependencies installed (Step 1 below)

---

## Steps

### 1. Install Dependencies

```bash
pip install -r content/content_v2/requirements.txt
```

### 2. Configure Environment

Copy the example env and fill in your API keys:
```bash
cp content/content_v2/.env.example content/content_v2/.env
```

Required keys:
- `ANTHROPIC_API_KEY` — for caption generation and content analysis
- `GOOGLE_API_KEY` — for image generation via Imagen 3

### 3. Run the Pipeline

**From Instagram links (recommended):**
```bash
python content/content_v2/main.py --links "https://instagram.com/p/ABC123" "https://instagram.com/p/DEF456"
```

**From a text file of links:**
```bash
python content/content_v2/main.py --links-file content/content_v2/input/links.txt
```

**From local inspiration images:**
```bash
python content/content_v2/main.py --images content/content_v2/input/inspo_1.jpg content/content_v2/input/inspo_2.png
```

**Options:**
- `--style` : Image style (`poster`, `flatlay`, `lifestyle`, `editorial`, `amazon`) — default: `lifestyle`
- `--variants` : Number of caption/image variants to generate — default: `2`
- `--image-provider` : `google` or `dalle` — default: `google`
- `--text-provider` : `claude` or `gemini` — default: `claude`
- `--mock` : Run without API calls for testing
- `--skip-scrape` : Skip scraping, use images from `input/` directly
- `--skip-images` : Only generate captions, skip image generation

### 4. Review Output

Generated content bundles are saved to:
```
content/content_v2/output/<run_timestamp>/
├── analysis.json          # Inspiration breakdown
├── post_1/
│   ├── caption.txt        # Ready-to-post caption with hashtags
│   ├── image.png          # Generated image
│   └── metadata.json      # Score, prompt used, style info
├── post_2/
│   └── ...
└── run_log.json           # Full pipeline log
```

### 5. Review Scores

Each post gets an AI quality score (1-10) in `metadata.json`:
- `brand_alignment` — Does it match Benefills' voice and aesthetic?
- `inspiration_match` — Does it capture the competitor's successful elements?
- `engagement_potential` — Is it scroll-stopping for Instagram?

---

## Project Structure

```
content/content_v2/
├── main.py                 # CLI entrypoint
├── requirements.txt
├── .env.example
├── config/
│   └── brand_context.json  # Benefills brand profile
├── input/                  # Drop inspiration images or links.txt here
├── output/                 # Generated content bundles
├── modules/
│   ├── __init__.py
│   ├── scraper.py          # Instagram scraping (instaloader)
│   ├── analyzer.py         # AI analysis of inspiration content
│   ├── caption_gen.py      # Caption + hashtag generation
│   ├── image_gen.py        # Image generation (Imagen/DALL-E)
│   ├── reviewer.py         # AI quality scoring
│   ├── logger.py           # Logging utility
│   └── utils.py            # Shared helpers
└── prompts/
    ├── analyze_inspo.md    # System prompt for analyzing inspiration
    ├── generate_caption.md # System prompt for caption generation
    └── review_post.md      # System prompt for quality review
```

## Notes

- The `--mock` flag is your friend — use it to test the full pipeline without spending API credits.
- All runs are logged to `output/<timestamp>/run_log.json` for auditing.
- The architecture uses abstract base classes for all providers, making it easy to add video generation later.
- Brand context is loaded from `config/brand_context.json` — update this as Benefills evolves.
