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

class ImageFactory:
    @staticmethod
    def get_provider(provider_type: str = "dalle") -> ImageProvider:
        if provider_type == "dalle" and os.getenv("OPENAI_API_KEY"):
            return DallEProvider()
        return MockImageProvider()
