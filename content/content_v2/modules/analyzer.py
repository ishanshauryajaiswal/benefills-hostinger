"""
Analyzer module.
Takes scraped inspiration content and produces a structured analysis
of what makes it effective, using Claude or Gemini.
"""

import os
import json
import base64
from abc import ABC, abstractmethod
from typing import List, Dict, Optional

from .logger import setup_logger
from .utils import load_prompt, load_brand_context, extract_json_from_text

logger = setup_logger('analyzer')


class BaseAnalyzer(ABC):
    """Abstract analyzer — swap between LLM providers."""

    @abstractmethod
    def analyze(self, image_path: str, caption: str, brand_context: dict) -> dict:
        pass

    @abstractmethod
    def generate_concept(self, topic: str, brand_context: dict) -> dict:
        """Generate a concept analysis from scratch based on a topic."""
        pass


class ClaudeAnalyzer(BaseAnalyzer):
    """Uses Claude to analyze inspiration content (supports vision)."""

    def __init__(self):
        from anthropic import Anthropic
        from dotenv import load_dotenv
        load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in .env")
        self.client = Anthropic(api_key=self.api_key)

    def analyze(self, image_path: str, caption: str, brand_context: dict) -> dict:
        system_prompt = load_prompt("analyze_inspo")

        # Build message content
        content = []

        # Add image if it's a real image file (not a mock text file)
        if image_path and os.path.isfile(image_path) and not image_path.endswith('.txt'):
            try:
                with open(image_path, 'rb') as f:
                    image_data = base64.standard_b64encode(f.read()).decode('utf-8')

                # Determine media type
                ext = os.path.splitext(image_path)[1].lower()
                media_types = {'.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
                               '.png': 'image/png', '.webp': 'image/webp'}
                media_type = media_types.get(ext, 'image/jpeg')

                content.append({
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": media_type,
                        "data": image_data
                    }
                })
            except Exception as e:
                logger.warning(f"Could not load image for analysis: {e}")

        # Add text context
        user_text = f"""
Analyze this Instagram post inspiration:

**Caption from the post:**
{caption}

**Our brand context (Benefills):**
- Brand: {brand_context.get('brand_name', 'Benefills')}
- Products: {', '.join(brand_context.get('products', []))}
- Topics: {', '.join(brand_context.get('topics', []))}
- Target audience: {json.dumps(brand_context.get('target_audience', {}), indent=2)}

Provide a structured analysis as JSON following the framework in your system prompt.
"""
        content.append({"type": "text", "text": user_text})

        message = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=2000,
            system=system_prompt,
            messages=[{"role": "user", "content": content}]
        )

        response_text = message.content[0].text
        analysis = extract_json_from_text(response_text)

        if analysis is None:
            logger.warning("Could not parse JSON from analysis response, returning raw text")
            analysis = {"raw_analysis": response_text}

        return analysis

    def generate_concept(self, topic: str, brand_context: dict) -> dict:
        system_prompt = load_prompt("ideate_concept")
        
        user_prompt = f"""
Topic: {topic}

Brand Context:
- Brand: {brand_context.get('brand_name', 'Benefills')}
- Products: {', '.join(brand_context.get('products', []))}
- Topics: {', '.join(brand_context.get('topics', []))}
- Target Audience: {json.dumps(brand_context.get('target_audience', {}), indent=2)}

Generate a detailed concept for an Instagram post about this topic.
"""
        
        message = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=2000,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        
        response_text = message.content[0].text
        analysis = extract_json_from_text(response_text)
        
        if analysis is None:
            logger.warning("Could not parse JSON from concept generation, returning raw text")
            analysis = {"raw_analysis": response_text}
            
        # Add metadata so downstream tools know source
        analysis["_source"] = {"type": "scratch", "topic": topic}
        
        return analysis


class GeminiAnalyzer(BaseAnalyzer):
    """Uses Gemini to analyze inspiration content."""

    def __init__(self):
        from dotenv import load_dotenv
        load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in .env")

        import google.generativeai as genai
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def analyze(self, image_path: str, caption: str, brand_context: dict) -> dict:
        system_prompt = load_prompt("analyze_inspo")

        parts = []

        # Add image if valid
        if image_path and os.path.isfile(image_path) and not image_path.endswith('.txt'):
            try:
                import PIL.Image
                img = PIL.Image.open(image_path)
                parts.append(img)
            except Exception as e:
                logger.warning(f"Could not load image for Gemini analysis: {e}")

        user_text = f"""
{system_prompt}

Analyze this Instagram post inspiration:

**Caption:** {caption}

**Our brand (Benefills):**
- Products: {', '.join(brand_context.get('products', []))}
- Topics: {', '.join(brand_context.get('topics', []))}

Return structured JSON analysis.
"""
        parts.append(user_text)

        response = self.model.generate_content(parts)
        analysis = extract_json_from_text(response.text)

        if analysis is None:
            analysis = {"raw_analysis": response.text}

        return analysis

    def generate_concept(self, topic: str, brand_context: dict) -> dict:
        system_prompt = load_prompt("ideate_concept")
        
        user_prompt = f"""
{system_prompt}

Topic: {topic}

Brand Context:
- Brand: {brand_context.get('brand_name', 'Benefills')}
- Products: {', '.join(brand_context.get('products', []))}
- Topics: {', '.join(brand_context.get('topics', []))}

Generate structured JSON concept.
"""
        
        response = self.model.generate_content(user_prompt)
        analysis = extract_json_from_text(response.text)
        
        if analysis is None:
            analysis = {"raw_analysis": response.text}
            
        analysis["_source"] = {"type": "scratch", "topic": topic}
        
        return analysis


class MockAnalyzer(BaseAnalyzer):
    """Mock analyzer for testing."""

    def analyze(self, image_path: str, caption: str, brand_context: dict) -> dict:
        logger.info("[MOCK] Analyzing inspiration content")
        return {
            "visual_aesthetics": {
                "color_palette": "Warm earth tones with green accents",
                "composition": "Centered product with flat-lay styling",
                "lighting": "Natural soft light, slight golden hour warmth",
                "typography": "Bold sans-serif headline, minimal text",
                "props": "Scattered seeds, wooden surface, linen backdrop"
            },
            "content_strategy": {
                "hook_type": "Bold health claim with specific benefit",
                "value_proposition": "Functional nutrition made delicious",
                "content_format": "Product showcase with educational angle",
                "cta_approach": "Direct link in bio + discount code"
            },
            "engagement_elements": {
                "caption_structure": "Hook + 3-line body + CTA + hashtags",
                "emotional_trigger": "Aspiration + pain point",
                "shareability": "High — relatable health tip with save-worthy info"
            },
            "adaptation_notes": {
                "what_to_borrow": "Flat-lay composition, warm tones, ingredient-focused styling",
                "what_to_skip": "Generic wellness messaging without specific claims",
                "benefills_angle": "Tie to thyroid health with Selenium/Zinc callout"
            }
        }

    def generate_concept(self, topic: str, brand_context: dict) -> dict:
        logger.info(f"[MOCK] Generating concept for topic: {topic}")
        return {
            "visual_aesthetics": {
                "color_palette": "Fresh greens and whites",
                "composition": "Minimalist product shot",
                "lighting": "Bright studio lighting",
                "typography": "Clean sans-serif",
                "props": "Fresh ingredients related to topic"
            },
            "content_strategy": {
                "hook_type": "Did you know?",
                "value_proposition": "Simple health hack",
                "content_format": "Infographic style",
                "cta_approach": "Save for later"
            },
            "engagement_elements": {
                "caption_structure": "Question -> Answer -> CTA",
                "emotional_trigger": "Curiosity",
                "shareability": "High utility"
            },
            "adaptation_notes": {
                "what_to_borrow": "Clean layout",
                "what_to_skip": "Clutter",
                "benefills_angle": "Thyroid-friendly twist"
            },
            "_source": {"type": "scratch", "topic": topic}
        }


class AnalyzerFactory:
    @staticmethod
    def get_analyzer(provider: str = "claude", mock: bool = False) -> BaseAnalyzer:
        if mock:
            return MockAnalyzer()
        if provider == "gemini":
            return GeminiAnalyzer()
        return ClaudeAnalyzer()
