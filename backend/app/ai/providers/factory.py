from app.ai.providers.gemini_provider import GeminiProvider
from app.ai.providers.openai_provider import OpenAIProvider
from app.ai.providers.base_provider import BaseProvider


class ProviderFactory:
    @staticmethod
    def create(provider: str) -> BaseProvider:
        provider=provider.lower()
        providers = {
            "gemini": GeminiProvider,
            "openai": OpenAIProvider,
        }
        provider_class = providers.get(provider)
        if not provider_class:
            raise ValueError(f"Invalid provider: {provider}")
        return provider_class()