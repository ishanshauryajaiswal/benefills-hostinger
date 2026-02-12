"""
Image generation module.
Generates Instagram post images using Google Imagen 3 or DALL-E,
with prompts crafted from the inspiration analysis + brand context.
"""

import os
import json
import requests
from abc import ABC, abstractmethod
from typing import Optional

from .logger import setup_logger
from .utils import load_brand_context

logger = setup_logger('image_gen')


# Instagram-optimized image style prompts (adapted from v1 image_prompts.py)
STYLE_TEMPLATES = {
    "lifestyle": (
        "Professional Instagram lifestyle product photography of {description}. "
        "Setting: Natural, authentic environment (modern kitchen counter, sunny breakfast table, or cozy living room). "
        "Lighting: Natural sunlight, golden hour, soft directional warmth. "
        "Styling: Casual organic feel with complementary props (fresh ingredients, scattered seeds, wooden surface). "
        "Product is the clear hero but context adds warmth. "
        "Aesthetic: Fresh, healthy, wholesome, premium Indian health food brand. "
        "Colors: Soft purple/lavender accents, warm beige, fresh greens. "
        "Aspect ratio 4:5, Instagram-optimized, high-res, commercial quality, no text on image."
    ),
    "poster": (
        "High-resolution Instagram post image (4:5 aspect ratio) of {description}. "
        "Dynamic premium composition, mouthwatering textures, vibrant colors. "
        "Deep rich backdrop with dramatic professional studio lighting, depth of field, high contrast. "
        "Premium luxurious feel. No hands, people, text, logos, or distracting elements. "
        "Commercial advertising quality, ultra-detailed."
    ),
    "flatlay": (
        "Top-down flat lay product photography for Instagram (4:5). {description}. "
        "Centered main product with aesthetic props scattered around "
        "(scattered seeds, dried berries, honey drizzle, fresh herbs). "
        "Warm beige seamless background, soft directional sunlight, crisp realistic shadow. "
        "Ultra-realistic, macro photography feel, sharp focus, clean composition, no text. 8k quality."
    ),
    "editorial": (
        "High-key editorial product shot for Instagram of {description}. "
        "Aspect ratio 4:5. Artistic composition with creative angles. "
        "Magazine-quality lighting with soft studio setup. "
        "Clean, sophisticated, premium feel. Minimal background. Sharp focus. "
        "Commercial advertising standard. No text overlay."
    ),
    "amazon": (
        "Product image for e-commerce listing: {description}. "
        "Pure white background (RGB 255, 255, 255). Front view, crystal clear product-centric shot. "
        "No props, no distractions, no text. Soft studio lighting, sharp focus throughout. "
        "Product fills 85% of frame. Square 1:1 format."
    )
}


class BaseImageGenerator(ABC):
    """Abstract image generator — makes it easy to add video generation later."""

    @abstractmethod
    def generate(self, prompt: str, output_path: str, style: str = "lifestyle") -> str:
        """Generate an image and save to output_path. Returns the path."""
        pass


class GoogleImageGenerator(BaseImageGenerator):
    """Uses Google Imagen 3 for image generation."""

    def __init__(self):
        from dotenv import load_dotenv
        load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in .env")

        import google.generativeai as genai
        genai.configure(api_key=self.api_key)
        self.model_name = os.getenv("GOOGLE_IMAGE_MODEL", "imagen-3.0-generate-001")

    def generate(self, prompt: str, output_path: str, style: str = "lifestyle") -> str:
        import google.generativeai as genai

        styled_prompt = self._apply_style(prompt, style)
        logger.info(f"Generating image with Imagen 3 ({style} style)")
        logger.info(f"Prompt: {styled_prompt[:200]}...")

        model = genai.ImageModel(self.model_name)
        response = model.generate_images(
            prompt=styled_prompt,
            number_of_images=1,
        )

        if response.images:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            response.images[0].save(output_path)
            logger.info(f"Image saved: {output_path}")
            return output_path
        else:
            raise Exception("Google Imagen failed to generate image.")

    def _apply_style(self, description: str, style: str) -> str:
        template = STYLE_TEMPLATES.get(style, STYLE_TEMPLATES["lifestyle"])
        return template.format(description=description)


class DallEImageGenerator(BaseImageGenerator):
    """Uses OpenAI DALL-E 3 for image generation."""

    def __init__(self):
        from openai import OpenAI
        from dotenv import load_dotenv
        load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in .env")
        self.client = OpenAI(api_key=self.api_key)

    def generate(self, prompt: str, output_path: str, style: str = "lifestyle") -> str:
        styled_prompt = self._apply_style(prompt, style)
        logger.info(f"Generating image with DALL-E 3 ({style} style)")

        response = self.client.images.generate(
            model="dall-e-3",
            prompt=styled_prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url

        # Download
        img_data = requests.get(image_url).content
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'wb') as f:
            f.write(img_data)

        logger.info(f"Image saved: {output_path}")
        return output_path

    def _apply_style(self, description: str, style: str) -> str:
        template = STYLE_TEMPLATES.get(style, STYLE_TEMPLATES["lifestyle"])
        return template.format(description=description)


class MockImageGenerator(BaseImageGenerator):

    def generate(self, prompt: str, output_path: str, style: str = "lifestyle") -> str:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(f"[MOCK IMAGE]\nStyle: {style}\nPrompt: {prompt}")
        logger.info(f"[MOCK] Image saved: {output_path}")
        return output_path


class ImageGeneratorFactory:
    @staticmethod
    def get_generator(provider: str = "google", mock: bool = False) -> BaseImageGenerator:
        if mock:
            return MockImageGenerator()
        if provider == "dalle" and os.getenv("OPENAI_API_KEY"):
            return DallEImageGenerator()
        if provider == "google" and os.getenv("GOOGLE_API_KEY"):
            return GoogleImageGenerator()
        
        logger.warning(f"Provider {provider} requested but API key missing. Falling back to MockImageGenerator.")
        return MockImageGenerator()


def build_image_prompt(analysis: dict, brand_context: dict) -> str:
    """
    Build an image generation prompt from the inspiration analysis and brand context.
    Extracts the most relevant visual elements from the analysis.
    """
    brand_name = brand_context.get("brand_name", "Benefills")
    products = brand_context.get("products", [])
    colors = brand_context.get("colors", {})

    # Extract visual insights from analysis
    visual = analysis.get("visual_aesthetics", {})
    adaptation = analysis.get("adaptation_notes", {})

    borrow_elements = adaptation.get("what_to_borrow", "")
    benefills_angle = adaptation.get("benefills_angle", "")
    color_palette = visual.get("color_palette", "")
    props = visual.get("props", "")

    # Pick a product to feature (first one as default)
    featured_product = products[0] if products else "functional health food product"

    prompt = (
        f"{brand_name} brand '{featured_product}' — "
        f"Instagram performance marketing image. "
        f"Inspired by: {borrow_elements}. "
        f"Brand angle: {benefills_angle}. "
        f"Color hints: {color_palette}, with brand colors {json.dumps(colors)}. "
        f"Props/styling: {props}. "
        f"Must look premium, appetizing, and scroll-stopping for Instagram."
    )

    return prompt
