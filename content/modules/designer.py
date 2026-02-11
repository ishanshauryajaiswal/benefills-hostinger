from abc import ABC, abstractmethod
import os
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class ImageProvider(ABC):
    @abstractmethod
    def generate_image(self, prompt: str, output_path: str) -> str:
        pass

class DallEProvider(ImageProvider):
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in .env")
        self.client = OpenAI(api_key=self.api_key)

    def generate_image(self, prompt: str, output_path: str) -> str:
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024", # Or 1024x1792 for 9:16
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        
        # Download the image
        img_data = requests.get(image_url).content
        with open(output_path, 'wb') as handler:
            handler.write(img_data)
            
        return output_path

class MockImageProvider(ImageProvider):
    def generate_image(self, prompt: str, output_path: str) -> str:
        with open(output_path, 'w') as f:
            f.write(f"MOCK IMAGE for prompt: {prompt}")
        return output_path

class GoogleImageProvider(ImageProvider):
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in .env")
        
        import google.generativeai as genai
        genai.configure(api_key=self.api_key)
        # Using the advanced Imagen model (NanoBanana Pro)
        # Fallback logic for model naming variations
        self.model_name = os.getenv("GOOGLE_IMAGE_MODEL", "imagen-3.0-generate-001")

    def generate_image(self, prompt: str, output_path: str) -> str:
        import google.generativeai as genai
        model = genai.ImageModel(self.model_name)
        
        # NanoBanana Pro supports high quality and 1:1 or other aspects via prompt
        # but the SDK usually has specific parameters
        response = model.generate_images(
            prompt=prompt,
            number_of_images=1,
            # safety_setting="BLOCK_ONLY_HIGH"
        )
        
        if response.images:
            response.images[0].save(output_path)
            return output_path
        else:
            raise Exception("Google AI failed to generate image.")

class ImageFactory:
    @staticmethod
    def get_provider(provider_type: str = "dalle") -> ImageProvider:
        if provider_type == "google" and os.getenv("GOOGLE_API_KEY"):
            return GoogleImageProvider()
        if provider_type == "dalle" and os.getenv("OPENAI_API_KEY"):
            return DallEProvider()
        return MockImageProvider()
