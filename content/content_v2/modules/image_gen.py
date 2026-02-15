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
        "Aesthetic: Fresh, healthy, wholesome, premium, empowering Indian health food brand. "
        "Colors: Benefills Palette — Teal (#2A9D8F), Warm Coral (#E76F51), Cream (#F4F1DE), Soft Sage Green. "
        "Aspect ratio 4:5, Instagram-optimized, high-res, commercial quality, no text on image."
    ),
    "poster": (
        "High-resolution Instagram post image (4:5 aspect ratio) of {description}. "
        "Dynamic premium composition, mouthwatering textures, vibrant colors. "
        "Place it against a deep, rich backdrop (Teal or Navy) with dramatic professional studio lighting, depth of field, high contrast. "
        "Premium luxurious feel. No hands, people, text, logos, or distracting elements. "
        "Use Benefills brand colors: Teal, Coral, Cream accents. "
        "Commercial advertising quality, ultra-detailed."
    ),
    "flatlay": (
        "Top-down flat lay product photography for Instagram (4:5). {description}. "
        "Centered main product with aesthetic props scattered around "
        "(scattered seeds, dried berries, honey drizzle, fresh herbs). "
        "Background: Clean Cream (#F4F1DE) or Soft Sage Green (#8AB17D) seamless paper. "
        "Lighting: Soft directional sunlight, crisp realistic shadow (Golden Hour). "
        "Ultra-realistic, macro photography feel, sharp focus, clean composition, no text. 8k quality."
    ),
    "editorial": (
        "High-key editorial product shot for Instagram of {description}. "
        "Aspect ratio 4:5. Artistic composition with creative angles. "
        "Magazine-quality lighting with soft studio setup. "
        "Background: Pure white or soft cream (#F4F1DE). "
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
    """Uses Google NanoBanana (Gemini 2.5/3.0) for image generation via curl."""

    def __init__(self):
        from dotenv import load_dotenv
        env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
        # Use override=True to ensure file values take precedence over any stale env vars
        load_dotenv(env_path, override=True)

        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in .env")

        # Default to the cheaper "Nano Banana" (Gemini 2.5 Flash Image)
        # We explicitly check if the env var is the old legacy value and replace it if so
        env_model = os.getenv("GOOGLE_IMAGE_MODEL")
        if env_model == "imagen-3.0-generate-001" or not env_model:
            self.model_name = "gemini-2.5-flash-image"
        else:
            self.model_name = env_model
            
        # Pro model "Nano Banana Pro" (Gemini 3 Pro Image)
        self.pro_model_name = os.getenv("GOOGLE_IMAGE_MODEL_PRO", "gemini-3.0-flash-image")
        
        logger.info(f"Initialized GoogleImageGenerator with model: {self.model_name}")

    def generate(self, prompt: str, output_path: str, style: str = "lifestyle") -> str:
        styled_prompt = self._apply_style(prompt, style)
        logger.info(f"Generating image with Google Model: {self.model_name} ({style} style)")
        logger.info(f"Prompt: {styled_prompt[:200]}...")

        # Construct the curl command
        # Note: Using the v1beta endpoint as per documentation
        # Target endpoint: https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent
        
        # Decide which model to use (could add a flag later, defaulting to standard/flash)
        model_to_use = self.model_name
        
        # Prepare the JSON payload
        import json
        payload = {
            "contents": [{
                "parts": [{"text": styled_prompt}]
            }]
        }
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_to_use}:generateContent?key={self.api_key}"
        
        # We will execute this via subprocess to mimic the curl command, but using requests is safer/easier in python.
        # However, the user asked to "take some sort of manual approval before calling its curl".
        # We will simulate this by asking for input if we were in an interactive shell, 
        # but since we are in a script, we might log it or use a confirm utility.
        # For now, we will print the plan and proceed if in mock/test mode, but the user explicitly asked for approval.
        
        print(f"\n[APPROVAL REQUIRED] About to call Google Image API ({model_to_use})")
        print(f"Endpoint: .../models/{model_to_use}:generateContent")
        print(f"Cost Warning: Ensure you are aware of the costs for {model_to_use}.")
        
        # In a real automated pipeline, manual approval stops the flow. 
        # We will check an environment variable or arg to skip, otherwise we pause.
        # For this specific user request, I will implement a strict input check.
        if os.getenv("SKIP_APPROVAL", "false").lower() != "true":
             response_input = input(">> Type 'yes' to proceed with generation, or anything else to skip: ")
             if response_input.lower() != "yes":
                 logger.warning("User skipped image generation.")
                 return None

        try:
            response = requests.post(
                url,
                headers={'Content-Type': 'application/json'},
                json=payload
            )
            
            if response.status_code != 200:
                logger.error(f"Google API Error ({response.status_code}): {response.text}")
                raise Exception(f"Google API failed: {response.text}")
                
            response_json = response.json()
            
            # The image data is in candidates[0].content.parts[0].inline_data.data (Base64)
            # OR sometimes directly if the API shape changes, but based on recent docs:
            # It usually returns inline_data for images.
            
            # Let's handle the response structure carefully
            try:
                # Check for direct image bytes if that's how it returns (rare for this endpoint, usually JSON)
                # Parse JSON path
                import base64
                
                # Common path for Gemini Image responses
                # Note: The user doc says "response has the generated image as Base64 encoded data in the inline_data"
                # This is typically under candidates -> content -> parts -> inline_data
                
                candidates = response_json.get("candidates", [])
                if not candidates:
                    # Check if it was blocked
                    prompt_feedback = response_json.get("promptFeedback", {})
                    if prompt_feedback:
                         raise Exception(f"Prompt blocked: {prompt_feedback}")
                    raise Exception("No candidates returned.")
                    
                parts = candidates[0].get("content", {}).get("parts", [])
                if not parts:
                     raise Exception("No parts in content.")
                     
                # Look for inline_data (camelCase in raw JSON)
                base64_data = None
                for part in parts:
                    if "inlineData" in part:
                         base64_data = part["inlineData"]["data"]
                         break
                
                if not base64_data:
                    # Fallback check for snake_case just in case
                    for part in parts:
                         if "inline_data" in part:
                             base64_data = part["inline_data"]["data"]
                             break
                
                if not base64_data:
                    raise Exception("No inline_data found in response.")
                    
                img_bytes = base64.b64decode(base64_data)
                
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                with open(output_path, "wb") as f:
                    f.write(img_bytes)
                    
                logger.info(f"Image saved: {output_path}")
                return output_path

            except Exception as parse_e:
                 logger.error(f"Failed to parse Google API response: {parse_e}")
                 logger.error(f"Full Response: {json.dumps(response_json, indent=2)}")
                 raise

        except Exception as e:
            logger.error(f"Generate Request Failed: {e}")
            raise

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
