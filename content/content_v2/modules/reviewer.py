"""
Reviewer module.
AI-powered quality scoring of generated post bundles (caption + image prompt).
Scores brand alignment, inspiration match, engagement potential, and overall quality.
"""

import os
import json
from abc import ABC, abstractmethod
from typing import Dict

from .logger import setup_logger
from .utils import load_prompt, extract_json_from_text

logger = setup_logger('reviewer')


class BaseReviewer(ABC):

    @abstractmethod
    def review(self, caption: str, image_prompt: str, analysis: dict,
               brand_context: dict) -> dict:
        pass


class ClaudeReviewer(BaseReviewer):

    def __init__(self):
        from anthropic import Anthropic
        from dotenv import load_dotenv
        load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in .env")
        self.client = Anthropic(api_key=self.api_key)

    def review(self, caption: str, image_prompt: str, analysis: dict,
               brand_context: dict) -> dict:
        system_prompt = load_prompt("review_post")

        user_prompt = f"""
Review this generated Instagram post for the Benefills brand:

**Generated Caption:**
{caption}

**Image Generation Prompt:**
{image_prompt}

**Original Inspiration Analysis:**
{json.dumps(analysis, indent=2)}

**Brand Context:**
{json.dumps(brand_context, indent=2)}

Score this post and provide suggestions.
"""

        message = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1000,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )

        response_text = message.content[0].text
        review = extract_json_from_text(response_text)

        if review is None:
            logger.warning("Could not parse review JSON, using defaults")
            review = {
                "brand_alignment": {"score": 5, "reason": "Could not parse review"},
                "inspiration_match": {"score": 5, "reason": "Could not parse review"},
                "engagement_potential": {"score": 5, "reason": "Could not parse review"},
                "overall_quality": {"score": 5, "reason": "Could not parse review"},
                "suggestions": [],
                "raw_review": response_text
            }

        return review


class MockReviewer(BaseReviewer):

    def review(self, caption: str, image_prompt: str, analysis: dict,
               brand_context: dict) -> dict:
        logger.info("[MOCK] Reviewing post quality")
        return {
            "brand_alignment": {"score": 8, "reason": "Good use of thyroid health angle and Benefills products"},
            "inspiration_match": {"score": 7, "reason": "Captures the educational + visual appeal from inspiration"},
            "engagement_potential": {"score": 8, "reason": "Strong hook, clear CTA, save-worthy content"},
            "overall_quality": {"score": 8, "reason": "Ready to post with minor tweaks"},
            "suggestions": [
                "Consider adding a more specific pain point in the hook",
                "Could include a question to drive comments"
            ]
        }


class ReviewerFactory:
    @staticmethod
    def get_reviewer(provider: str = "claude", mock: bool = False) -> BaseReviewer:
        if mock:
            return MockReviewer()
        # Only Claude for reviews (doesn't need image gen capabilities)
        return ClaudeReviewer()
