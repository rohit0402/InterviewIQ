from google import genai

from app.ai.providers.base_provider import BaseProvider
from app.core.config import settings


class GeminiProvider(BaseProvider):

    def __init__(self):
        self.client = genai.Client(api_key=settings.AI_API_KEY)

    def generate(self, prompt: str) -> str:

        response = self.client.models.generate_content(
            model=settings.AI_MODEL,
            contents=prompt,
        )
        
        return response.text.strip()