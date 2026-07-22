from app.ai.providers.base_provider import BaseProvider


class OpenAIProvider(BaseProvider):

    def generate(self, prompt: str) -> str:
        raise NotImplementedError("OpenAI Provider not implemented.")