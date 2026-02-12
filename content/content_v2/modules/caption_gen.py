"""
Caption generator module.
Produces Instagram captions + hashtags inspired by the analysis,
tailored to the Benefills brand.
"""

import os
import json
from abc import ABC, abstractmethod
from typing import List, Dict

from .logger import setup_logger
from .utils import load_prompt, extract_json_from_text

logger = setup_logger('caption_gen')


class BaseCaptionGenerator(ABC):
    """Abstract caption generator — supports multiple LLM providers."""

    @abstractmethod
    def generate(self, analysis: dict, brand_context: dict, num_variants: int = 2) -> List[dict]:
        """Generate caption variants. Returns list of {caption, hashtags} dicts."""
        pass


class ClaudeCaptionGenerator(BaseCaptionGenerator):

    def __init__(self):
        from anthropic import Anthropic
        from dotenv import load_dotenv
        load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in .env")
        self.client = Anthropic(api_key=self.api_key)

    def generate(self, analysis: dict, brand_context: dict, num_variants: int = 2) -> List[dict]:
        system_prompt = load_prompt("generate_caption")

        user_prompt = f"""
Based on this competitor inspiration analysis:
{json.dumps(analysis, indent=2)}

Brand context:
- Brand: {brand_context.get('brand_name', 'Benefills')}
- Products: {', '.join(brand_context.get('products', []))}
- Key ingredients: {', '.join(brand_context.get('key_ingredients', []))}
- Topics: {', '.join(brand_context.get('topics', []))}
- Target audience: {json.dumps(brand_context.get('target_audience', {}), indent=2)}
- CTA options: {', '.join(brand_context.get('social_media', {}).get('cta_options', []))}
- Seed hashtags: {', '.join(brand_context.get('social_media', {}).get('hashtags_seed', []))}

Generate {num_variants} distinct caption variants. Each should take a DIFFERENT angle
(e.g., one educational, one emotional/relatable).

Return as a JSON array:
[
  {{
    "variant": 1,
    "angle": "educational",
    "caption": "full caption text here",
    "hashtags": "#hashtag1 #hashtag2 ..."
  }},
  ...
]
"""

        message = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=3000,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )

        response_text = message.content[0].text
        result = extract_json_from_text(response_text)

        if result is None:
            # Fallback: treat the whole response as a single caption
            logger.warning("Could not parse JSON from caption response, using raw text")
            return [{"variant": 1, "angle": "mixed", "caption": response_text, "hashtags": ""}]

        # If result is a dict with a list inside, extract the list
        if isinstance(result, dict):
            for key in result:
                if isinstance(result[key], list):
                    return result[key]
            return [result]

        return result if isinstance(result, list) else [result]


class GeminiCaptionGenerator(BaseCaptionGenerator):

    def __init__(self):
        from dotenv import load_dotenv
        load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in .env")

        import google.generativeai as genai
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def generate(self, analysis: dict, brand_context: dict, num_variants: int = 2) -> List[dict]:
        system_prompt = load_prompt("generate_caption")

        user_prompt = f"""
{system_prompt}

Inspiration analysis: {json.dumps(analysis, indent=2)}
Brand: {brand_context.get('brand_name', 'Benefills')}
Products: {', '.join(brand_context.get('products', []))}

Generate {num_variants} caption variants as JSON array.
Each variant: {{"variant": N, "angle": "...", "caption": "...", "hashtags": "..."}}
"""

        response = self.model.generate_content(user_prompt)
        result = extract_json_from_text(response.text)

        if result is None:
            return [{"variant": 1, "angle": "mixed", "caption": response.text, "hashtags": ""}]

        if isinstance(result, dict):
            for key in result:
                if isinstance(result[key], list):
                    return result[key]
            return [result]

        return result if isinstance(result, list) else [result]


class MockCaptionGenerator(BaseCaptionGenerator):

    def generate(self, analysis: dict, brand_context: dict, num_variants: int = 2) -> List[dict]:
        logger.info(f"[MOCK] Generating {num_variants} caption variants")
        variants = []
        for i in range(num_variants):
            angle = "educational" if i % 2 == 0 else "relatable"
            variants.append({
                "variant": i + 1,
                "angle": angle,
                "caption": (
                    f"Your thyroid needs these 3 minerals daily. ✨\n\n"
                    f"Most people supplement blindly. But science says your thyroid specifically craves:\n\n"
                    f"→ Selenium (found in our Seeds Boost Bar)\n"
                    f"→ Zinc (packed into Nut-ella Nut Butter)\n"
                    f"→ Ashwagandha (in every Thyrovibe Care Pack)\n\n"
                    f"We didn't just make snacks. We made functional nutrition that your body actually recognizes.\n\n"
                    f"🔗 Link in bio | Use code FIRSTLOVE20 for 20% off\n\n"
                    f"What's your biggest thyroid health question? Drop it below 👇"
                ),
                "hashtags": (
                    "#Benefills #ThyroidHealth #FunctionalFoods #CleanEating "
                    "#HealthySnacks #NutButter #ThyroidNourishment #WellnessJourney "
                    "#ThyroidWarrior #Selenium #Zinc #Ashwagandha #HealthyLiving "
                    "#IndianHealthFood #NutritionFacts #ThyroidDiet"
                )
            })
        return variants


class CaptionGeneratorFactory:
    @staticmethod
    def get_generator(provider: str = "claude", mock: bool = False) -> BaseCaptionGenerator:
        if mock:
            return MockCaptionGenerator()
        if provider == "gemini":
            return GeminiCaptionGenerator()
        return ClaudeCaptionGenerator()
