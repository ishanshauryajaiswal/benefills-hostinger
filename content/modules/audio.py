from abc import ABC, abstractmethod
import os
import requests
from dotenv import load_dotenv

load_dotenv()

class AudioProvider(ABC):
    @abstractmethod
    def synthesize(self, text: str, output_path: str) -> str:
        pass

class ElevenLabsAudio(AudioProvider):
    def __init__(self):
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        self.voice_id = os.getenv("ELEVENLABS_VOICE_ID", "pNInz6obpgnuMvscWqt5") # Default voice

    def synthesize(self, text: str, output_path: str) -> str:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            return output_path
        else:
            raise Exception(f"ElevenLabs API error: {response.text}")

class MockAudio(AudioProvider):
    def synthesize(self, text: str, output_path: str) -> str:
        # Create a silent audio file using ffmpeg for testing if possible, 
        # or just return a dummy path.
        with open(output_path, 'w') as f:
            f.write("MOCK AUDIO")
        return output_path

class AudioFactory:
    @staticmethod
    def get_provider(provider_type: str = "elevenlabs") -> AudioProvider:
        if provider_type == "elevenlabs" and os.getenv("ELEVENLABS_API_KEY"):
            return ElevenLabsAudio()
        return MockAudio()
