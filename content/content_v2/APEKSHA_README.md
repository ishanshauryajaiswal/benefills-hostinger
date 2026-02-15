# Benefills Content Generation Overview

This guide lists the key files and folders that power our content creation engine. It is designed to help you understand where the "brain" and "strategy" reside.

## 🧠 Brain & Strategy

These files define *how* the AI thinks and creates content.

- **Content Strategy**: `content/docs/IMAGE_GENERATION_STRATEGY.md`
  - *This file contains the core visual guidelines and strategy for generating on-brand images.*

- **Ideation Prompts**: `content/content_v2/prompts/ideate_concept.md`
  - *Instructions for brainstorming creative concepts based on input.*

- **Caption Logic**: `content/content_v2/prompts/generate_caption.md`
  - *Guidelines for writing engaging captions in our brand voice.*
  
- **Analysis Logic**: `content/content_v2/prompts/analyze_inspo.md`
  - *How the AI analyzes inspiration images/posts to glean style and content.*

## ⚙️ The Engine (Core Logic)

These are the main scripts that execute the strategy.

- **Image Generator**: `content/content_v2/modules/image_gen.py`
  - *The module responsible for physically creating images.*

- **Caption Generator**: `content/content_v2/modules/caption_gen.py`
  - *The module that writes the text accompanying the images.*

- **Main Operator**: `content/content_v2/main.py`
  - *The primary script that runs the entire process.*

## 📂 Workflow

Here is how the system works from start to finish:

1.  **Input Phase**:
    -   You provide inspiration (links or images) in the `content/content_v2/input/` folder (e.g., `links.txt`).
    -   *This is where you tell the AI what to look at.*

2.  **Generation Phase**:
    -   We run the `main.py` script.
    -   The AI analyzes your input, brainstorms ideas based on our strategy, generates images, and writes captions.

3.  **Output Phase**:
    -   The final results (images + captions) are saved in the `content/content_v2/output/` folder.
    -   *You can review and pick the best content from here.*
