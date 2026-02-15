# PRD: Benefills Content Engine v2

## Overview
A web-based marketing interface for the Benefills Content Engine, allowing the marketing team to manage inspiration, trigger AI generation, and review results without touching the command line.

## Feature Roadmap

### 1. Inspiration Library
- [x] **View/Add Instagram Links**: Manage a list of competitor URLs for AI analysis.
- [x] **Visual Inspiration Gallery**: Grid view of reference images uploaded for style inspiration.
- [x] **Delete/Archive**: Clean up old or unused inspiration records.
- [x] **Upload Mechanism**: Direct upload of local reference images.

### 2. Dashboard & Navigation
- [x] **Central Hub**: Unified landing page for quick access to all modules.
- [x] **Modern UI**: Clean, premium aesthetic using Tailwind CSS and Lucide icons.

### 3. Generated Content Gallery (Gallery View)
- [x] **Run Batches**: List all historical generation runs (e.g., `run_20260215_...`).
- [x] **Post Grid**: View all generated images and captions from a specific run.
- [x] **Status Indicators**: Show metadata like provider (Claude/Gemini) and AI review score.

### 4. Post Inspector (Detail View)
- [x] **Image Viewer**: High-res view of the generated post.
- [x] **Caption Editor**: View and copy generated captions with emoji support.
- [x] **Prompt Visibility**: Show the exact prompt used to generate the image for transparency.
- [x] **AI Review Details**: Breakdown of brand alignment, engagement potential, and suggestions.

### 5. Content Strategic Insights
- [ ] **Strategic Analysis View**: Visualize the logic from `analysis.json` (Color palette, composition, hook, etc.).
- [ ] **Target Audience Context**: Show how the AI adapted the inspiration to the Benefills brand.

### 6. Interactive Generation (Self-Serve)
- [ ] **"Generate From Scratch"**: Form to provide a topic and trigger the backend script.
- [ ] **"Analyze & Generate"**: Select inspiration from the library and trigger a new run.
- [ ] **Live Progress UI**: Real-time feedback while the AI is thinking/generating.

## Technical Notes
- **Framework**: Next.js 15 (App Router), Tailwind CSS.
- **Backend Sync**: Interfaces directly with `content/content_v2` folder structure.
- **Image Serving**: Custom API routes to serve local file system images to the web.
