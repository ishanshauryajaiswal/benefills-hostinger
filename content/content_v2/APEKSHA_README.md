# specialized content generation brain

This document outlines the **Brain**, **Skills**, and **Workflow** of our AI content generation system. Use this as a map to understand where our content strategy lives and how the AI is instructed to create posts for Benefills.

## 🧠 The Brain (Strategy & Brand Voice)

These files represent the core intelligence and guidelines of the system. **Edit these files to change *how* the AI thinks about our brand.**

- **Visual Strategy**: `content/docs/IMAGE_GENERATION_STRATEGY.md`
  - *The master guide for our visual identity. It defines our color palettes, photography styles (e.g., "lifestyle", "flatlay"), and mood.*

- **Brand Context**: `content/content_v2/config/brand_context.json`
  - *The "persona" of Benefills. This file tells the AI who we are, our tone of voice, and our target audience.*

## ⚡ The Skills (Prompting & Instructions)

Think of these files as the specific instructions we give to the AI for each step of the creative process.

- **🕵️‍♀️ Analyzing Inspiration**: `content/content_v2/prompts/analyze_inspo.md`
  - *Instructions on how to look at competitor posts or inspiration images and extract key themes, lighting, and composition.*

- **💡 Ideating Concepts**: `content/content_v2/prompts/ideate_concept.md`
  - *The creative brief. It tells the AI how to brainstorm unique, on-brand post ideas based on the analyzed inspiration.*

- **✍️ Writing Captions**: `content/content_v2/prompts/generate_caption.md`
  - *The copywriter's guide. It ensures captions are engaging, use the right hashtags, and match our voice (confident, helpful, premium).*

- **⚖️ Review & Quality Control**: `content/content_v2/prompts/review_post.md`
  - *The editor's checklist. The AI uses this to double-check its own work against our brand standards before saving it.*

## 📚 Deep Knowledge Skills (Specialized Intelligence)

These folders contain specialized knowledge modules that give the AI deep expertise in our specific domain.

- **Brand Voice Module**: `.claude/skills/benefills-brand-voice`
  - *Deep training on exactly how Benefills sounds, including vocabulary and tone nuances.*

- **Visual Briefs**: `.claude/skills/benefills-image-briefs`
  - *Detailed instructions for generating our specific types of photography and graphics.*

- **Product Library**: `.claude/skills/benefills-product-library`
  - *Information about our specific products, ensuring the AI represents them accurately.*

- **Social Media System**: `.claude/skills/benefills-social-system`
  - *Best practices and formats for our social media channels.*

- **Thyroid Knowledge**: `.claude/skills/benefills-thyroid-hormone-knowledge`
  - *Medical and wellness context about thyroid health to ensure accuracy in our educational content.*

## 🔄 The Workflow

Here is the step-by-step process of how the system generates content:

1.  **Drop Inspiration**:
    -   You place inspiration images or a list of Instagram links into the `content/content_v2/input/` folder.
    -   *This tells the system: "Make something like this, but for Benefills."*

2.  **The AI "Thinks"**:
    -   The system reads your input and analyzes it using the **Analyzing Inspiration** skill.
    -   It then checks the **Brand Context** and **Visual Strategy** to ensure alignment.
    -   It brainstorms a fresh concept using the **Ideating Concepts** skill.

3.  **Creation**:
    -   **Visuals**: It generates a high-quality image based on the new concept.
    -   **Copy**: It writes a caption using the **Writing Captions** skill.

4.  **Review**:
    -   The system scores the final output using the **Review & Quality Control** skill.

5.  **Final Result**:
    -   You find the finished post (Image + Caption + Score) in the `content/content_v2/output/` folder.
    -   *Ready for you to post!*

---
*Note for Marketing: To improve the output, tweak the instruction files in "The Skills" or the strategy documents in "The Brain".*
