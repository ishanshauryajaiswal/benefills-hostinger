import os
import json
import re
from typing import Optional
from urllib.parse import urlparse


def get_project_root() -> str:
    """Get the root of the content_v2 project."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def load_brand_context() -> dict:
    """Load brand context from config/brand_context.json."""
    config_path = os.path.join(get_project_root(), "config", "brand_context.json")
    with open(config_path, 'r') as f:
        return json.load(f)


def load_prompt(prompt_name: str) -> str:
    """Load a system prompt from the prompts/ directory."""
    prompt_path = os.path.join(get_project_root(), "prompts", f"{prompt_name}.md")
    if not os.path.exists(prompt_path):
        raise FileNotFoundError(f"Prompt not found: {prompt_path}")
    with open(prompt_path, 'r') as f:
        return f.read()


def validate_instagram_url(url: str) -> bool:
    """Check if a URL looks like a valid Instagram post link."""
    parsed = urlparse(url)
    return parsed.hostname in ('www.instagram.com', 'instagram.com') and '/p/' in parsed.path


def validate_image_file(path: str) -> bool:
    """Check if a file path points to a valid image."""
    valid_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.bmp'}
    return os.path.isfile(path) and os.path.splitext(path)[1].lower() in valid_extensions


def sanitize_filename(name: str) -> str:
    """Create a filesystem-safe name from a string."""
    sanitized = re.sub(r'[^\w\s-]', '', name.lower())
    sanitized = re.sub(r'[\s]+', '_', sanitized)
    return sanitized[:50]


def extract_json_from_text(text: str) -> Optional[dict]:
    """Extract a JSON object from AI response text that may contain markdown."""
    # Try direct parse first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try to find JSON in code blocks
    json_match = re.search(r'```(?:json)?\s*\n?(.*?)\n?```', text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1).strip())
        except json.JSONDecodeError:
            pass

    # Try to find raw JSON object
    json_match = re.search(r'\{.*\}', text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(0))
        except json.JSONDecodeError:
            pass

    return None


def truncate_text(text: str, max_chars: int = 2000) -> str:
    """Truncate text to a maximum number of characters."""
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "..."
