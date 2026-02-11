# Image Generation Strategy for Benefills

## Core Best Practices for Healthy Snacks (E-Commerce)

This strategy integrates proven techniques for generating high-quality, on-brand product images using AI. We focus on clean, premium aesthetics that build consumer trust and drive appetite appeal.

### 1. The Reference Photo (Crucial)
*   **Always start with a reference photo.** Uploading an actual product photo ensures the AI maintains the correct shape, label text, colors, and branding.
*   **Consistency is Key:** Models like NanoBanana Pro (or similar image-to-image workflows) keep the brand identity intact while changing the scene.

### 2. Premium Studio Aesthetics
*   **Backgrounds:** Pure white seamless, warm beige, or deep black for drama.
*   **Lighting:** High-key lighting, soft shadows, heavy backlighting for "glowing" food, no harsh direct flash unless stylized.
*   **Composition:** Clean, no distractions. Avoid hands/people unless specifically styled.
*   **Focus:** Sharp focus on the product, soft depth of field for background elements.

### 3. Food Styling & Props
*   **Analyze Product Type:** Auto-add complementary ingredients (e.g., scattered nuts, seeds, fresh herbs for savory; berries, honey drizzle for sweet).
*   **Textures:** Use words like "mouthwatering," "steam," "dynamic burst," "crisp," "gooey."
*   **Color Palette:** Use minimal beige tones for "healthy & natural" vibes, or vibrant colors for energy.

### 4. Efficient Experimentation
*   **Grid Variations:** Generate 6x6 grids of variations to test moods/angles cheaply before final high-res renders.
*   **Storyboarding:** Create 3x3 grids showing multiple angles/usage for reels.

### 5. Detailed Prompt Structure
Structure prompts with clear sections:
*   **Subject:** The product (uploaded reference).
*   **Action/Scene:** Dynamic explosion, static flat lay, etc.
*   **Lighting/Camera:** "Studio lighting," "100mm lens," "f/8," "8k," "macro."
*   **Negative Prompts:** "No text," "no hands," "no logos," "no low resolution."

---

## Ready-to-Use Prompt Templates

### 1. Premium Dynamic Poster (Social/Reels)
**Best for:** Hero images, ads, high-impact visuals.
> "Create a high-resolution square (1:1) food poster of (YOUR HEALTHY SNACK e.g. mixed nut trail mix in clear pouch). Capture the dish in a dynamic, explosion-like composition bursting toward the viewer. Present it with realistic, mouthwatering textures and vibrant colors. Place it against a deep black backdrop with dramatic professional studio lighting, rich depth of field, and high contrast. Emphasize the premium, luxurious, and visually impactful feel. Exclude any hands, people, text, logos, or distracting tableware."

### 2. Top-Down Flat Lay (E-Commerce/Instagram)
**Best for:** Detail shots, showing ingredients, clean aesthetic.
> "Create top-down flat lay product photo. Use the uploaded product as the main object, centered. Analyze the product type from the photo and automatically choose matching props/ingredients for an aesthetic flat lay around it (minimal, premium, on-brand) — e.g. scattered seeds, dried berries, honey drizzle for a healthy bar. Preserve exact geometry, size, colors, label design, and all text on the product (no changes). Warm beige seamless background, soft directional sunlight, crisp realistic shadow. Ultra-realistic macro product photography, 100mm lens look, f/8, sharp focus, clean composition, no extra text, 8k, format 2:3."

### 3. Cookbook-Style Render
**Best for:** Recipe cards, blog posts, storytelling.
> "Input: (YOUR SNACK e.g. energy bite with nuts & seeds)
> <instructions>
> Analysis: Extract key ingredients, cooking techniques, and cultural food elements
> Goal: A cookbook where ingredients and dishes emerge in delicious detail
> Rules:
> Base: A vintage cookbook with stained pages and fabric cover, historical timeline of food
> Scene: 3D Miniature kitchen or market scene with chef & ingredients
> Details: Detailed food textures, steam effects, cooking implements
> Lighting: Warm kitchen lighting with golden hour quality
> Output: Single 4:5 image with appetizing details
> </instructions>"

### 4. Variation Grid (Testing)
**Best for:** Rapidly testing different styles/moods.
> "Generate a 6x6 grid of professional product photography. Reference the original image’s mood, quality, and aesthetic. Each cell should showcase a completely different product (…food, snacks…) in a unique studio setting with a distinct color palette. Maintain the same high-end commercial photography style throughout. Vary the products, lighting, backgrounds, props, and styling dramatically across all 36 images."

### 5. High-Key Studio Editorial
**Best for:** Clean catalog look, website headers.
> "Frosted-glass hands (optional), pure white background, ultra-sharp product, soft lighting, ethereal calm mood." (JSON-structured prompt recommended).

---

## Integration with Automation

We have implemented these strategies directly into the Content Engine (`content/main.py`).

### Usage
Generate content using specific visual styles via the `--style` flag:

```bash
python content/main.py --topic "Healthy Snacks for Energy" --format carousel --style poster
```

### Supported Styles
*   `poster`: Premium Dynamic Poster (Social/Reels) - **Default**
*   `flatlay`: Top-Down Flat Lay (E-Commerce/Instagram)
*   `cookbook`: Cookbook-Style Render
*   `grid`: Variation Grid (Testing)
*   `editorial`: High-Key Studio Editorial

### Implementation Logic
The system automatically:
1.  Generates a content plan (via Claude).
2.  Extracts specific visual descriptions for each slide.
3.  Injects these descriptions into the selected "Master Prompt" template (e.g., specific lighting, camera settings, negative prompts).
4.  Sends the optimized prompt to DALL-E 3 for generation.

**Note on Reference Images:**
Current automation uses text-to-image (DALL-E 3). While we cannot upload a reference photo directly in this pipeline, the prompts are engineered to simulate high consistency by detailing product attributes. For exact product replication (e.g., using a specific SKU photo), manual generation with tools like Midjourney or Stable Diffusion (ControlNet) is recommended using the "Reference Photo" best practices above.

---

## Workflow Patterns

### 1. Hybrid Workflow (AI Background + Real Product Photo)
**Recommended for:** Amazon, Etsy, Marketplaces.
*   **Step 1:** Start with a real, well-lit photo of your packet.
*   **Step 2:** Use UI-based tools (like NanoBanana Pro, Photoroom, or Photoshop Gen Fill) to remove the background.
*   **Step 3:** Generate a new background using the "Background & Environment" prompts described above.
*   **Step 4:** Final touch-ups in Photoshop.

### 2. Full AI Renders (Automated)
**Recommended for:** Social Media, Storyboards, Concept Testing.
*   **Method:** Use the `content/main.py` script.
*   **Role:** Creates high-quality "aspirational" imagery where exact package details are less critical than the overall mood and ingredient appeal.

---

## Strategy by Platform

### Amazon / E-Commerce
*   **Role:** Conversion & Clarity.
*   **Style:** `amazon`
*   **Key Visuals:** Pure white background, high-key lighting, 85% frame fill.
*   **Goal:** Zero distractions, pure product focus.

### Shopify / Instagram / Pinterest
*   **Role:** Engagement & Brand Building.
*   **Style:** `lifestyle`, `poster`, `flatlay`
*   **Key Visuals:** Natural lighting, human context (implied), complementary props.
*   **Goal:** "Stop the scroll," appetizing appeal.

---

## Additional Supported Styles

### 6. Amazon Catalog Standard
*   **Command:** `--style amazon`
*   **Visuals:** Pure white background (RGB 255,255,255), soft studio lighting, crystal clear focus.

### 7. Lifestyle Context
*   **Command:** `--style lifestyle`
*   **Visuals:** Natural sunlight, authentic environments (kitchen counter, picnic), 
casually styled with ingredients.

---

## AI Product Photo Skill

We have installed the `@GroundMountCompany/ai-product-photo` skill to this project. 

### Location
`.agent/skills/@GroundMountCompany/ai-product-photo/`

### How to Use
This skill provides a systematic framework for:
*   **Style Exploration:** Generate 5 distinct styles (Clean, Lifestyle, Premium, Editorial, Natural) before finalizing assets.
*   **Photography Shot Types:** Standardized prompts for Hero, Detail, and Lifestyle shots.
*   **Food Deep Dives:** Specific optimization for appetite appeal and freshness cues (steam, condensation, herbs).
*   **Platform Optimization:** Pre-configured constraints for Amazon vs. Instagram.

Use this skill's logic when constructing new prompts for the `main.py` engine to ensure maximum commercial viability.



