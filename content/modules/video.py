from abc import ABC, abstractmethod
import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

class VideoProvider(ABC):
    @abstractmethod
    def generate_video(self, script_text: str, audio_url: str, output_path: str) -> str:
        pass

class HeyGenVideo(VideoProvider):
    def __init__(self):
        self.api_key = os.getenv("HEYGEN_API_KEY")
        self.avatar_id = os.getenv("HEYGEN_AVATAR_ID")

    def generate_video(self, script_text: str, audio_url: str, output_path: str) -> str:
        # Simplified HeyGen implementation
        # In a real scenario, you'd post to /v2/video/generate and poll for status
        url = "https://api.heygen.com/v2/video/generate"
        headers = {
            "X-Api-Key": self.api_key,
            "Content-Type": "application/json"
        }
        data = {
            "video_inputs": [
                {
                    "character": {
                        "type": "avatar",
                        "avatar_id": self.avatar_id
                    },
                    "input_text": script_text
                }
            ],
            "dimension": "portrait"
        }
        # Note: This is a placeholder for the actual complex polling logic
        # return "https://heygen-output-url.mp4"
        print(f"Submitting to HeyGen: {script_text[:50]}...")
        return "mock_heygen_output.mp4"

class MockVideo(VideoProvider):
    def generate_video(self, script_text: str, audio_url: str, output_path: str) -> str:
        with open(output_path, 'w') as f:
            f.write("MOCK VIDEO content")
        return output_path

class VideoFactory:
    @staticmethod
    def get_provider(provider_type: str = "heygen") -> VideoProvider:
        if provider_type == "heygen" and os.getenv("HEYGEN_API_KEY"):
            return HeyGenVideo()
        return MockVideo()
