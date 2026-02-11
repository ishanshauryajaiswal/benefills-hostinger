# Benefills Brand Presence Engine - Guidelines

## Project Overview
This project is an automated pipeline for generating Instagram Reels for Benefills. It uses Claude for scripting, ElevenLabs for audio, HeyGen for video, and FFmpeg for assembly.

## Development Standards
- **Modular Design**: All external API integrations must be abstracted into classes in `content/modules/`.
- **Media Manipulation**: Use FFmpeg via Python `subprocess` or a wrapper. Never use hardcoded paths; use the established directory structure.
- **Environment Variables**: All sensitive keys must be in a `.env` file. Do not commit `.env`.
- **Aspect Ratio**: Always output 9:16 (1080x1920) for Instagram Reels.

## Directory Structure
- `content/`: Main application logic.
- `content/modules/`: Individual functional components (Audio, Video, Script, Assembly).
- `content/assets/`: Brand-specific B-roll, logos, and fonts.
- `.claude/agents/`: Subagent prompts for specialized tasks.

## Commands
- Run the pipeline: `./generate-content --topic "Your Topic"`
- Install dependencies: `pip install -r content/requirements.txt`

## Coding Standards
- Type hints are required for all module functions.
- Every module should have a `Mock` class for local testing without spending API credits.
- Log every step of the pipeline to `content/logs/`.
