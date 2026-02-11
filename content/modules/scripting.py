from abc import ABC, abstractmethod
import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

class ScriptingProvider(ABC):
    @abstractmethod
    def generate_script(self, topic: str, brand_context: dict, content_format: str = "reel") -> str:
        pass

class ClaudeScripting(ScriptingProvider):
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in .env")
        self.client = Anthropic(api_key=self.api_key)

    def generate_script(self, topic: str, brand_context: dict, content_format: str = "reel") -> str:
        # Load subagent prompt
        prompt_path = os.path.join(os.path.dirname(__file__), "../../.claude/agents/script_writer.md")
        with open(prompt_path, 'r') as f:
            system_prompt = f.read()

        user_prompt = f"""
        Topic: {topic}
        Format: {content_format}
        Brand Context: {brand_context['raw_data'][:2000]}
        
        Generate content for an Instagram {content_format}.
        """
        
        message = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1500,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        return message.content[0].text

class GeminiScripting(ScriptingProvider):
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in .env (needed for Gemini scripting)")
        import google.generativeai as genai
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def generate_script(self, topic: str, brand_context: dict, content_format: str = "reel") -> str:
        prompt_path = os.path.join(os.path.dirname(__file__), "../../.claude/agents/script_writer.md")
        system_prompt = ""
        if os.path.exists(prompt_path):
            with open(prompt_path, 'r') as f:
                system_prompt = f.read()

        user_prompt = f"""
        {system_prompt}
        
        Topic: {topic}
        Format: {content_format}
        Brand Context: {brand_context['raw_data'][:2000]}
        
        Generate content for an Instagram {content_format}.
        """
        
        response = self.model.generate_content(user_prompt)
        return response.text

class MockScripting(ScriptingProvider):
    def generate_script(self, topic: str, brand_context: dict, content_format: str = "reel") -> str:
        if content_format == "carousel":
            return "Slide 1: Title\nSlide 2: Fact\nSlide 3: CTA"
        return f"MOCK SCRIPT for {topic}: [HOOK] Hey Benefills fam! [BODY] Thyroid health is key. [CTA] Link in bio!"

class ScriptingFactory:
    @staticmethod
    def get_provider(provider_type: str = "claude") -> ScriptingProvider:
        if provider_type == "claude" and os.getenv("ANTHROPIC_API_KEY"):
            return ClaudeScripting()
        if provider_type == "gemini" or (provider_type == "claude" and not os.getenv("ANTHROPIC_API_KEY") and os.getenv("GOOGLE_API_KEY")):
            return GeminiScripting()
        return MockScripting()
