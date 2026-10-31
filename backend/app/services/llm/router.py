import os
import logging
from typing import Optional, Dict, Any
from app.core.config import settings

logger = logging.getLogger(__name__)

class LLMRouter:
    """Routes generation requests across Tier 1 (Flash) and Tier 2 (Pro) models."""

    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self._client = None
        if self.api_key:
            try:
                from google import genai
                self._client = genai.Client(api_key=self.api_key, http_options={"timeout": 180000})
                logger.info("Initialized Google GenAI client successfully.")
            except Exception as e:
                logger.warning(f"Could not initialize GenAI client: {e}")

    def is_available(self) -> bool:
        return self._client is not None

    def generate_content(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        model: str = "gemini-flash-latest",
        config: Optional[Dict[str, Any]] = None
    ) -> Optional[str]:
        if not self._client:
            return None
        try:
            response = self._client.models.generate_content(
                model=model,
                contents=prompt,
                config={**(config or {}), **({"system_instruction": system_instruction} if system_instruction else {})} or None
            )
            return response.text
        except Exception as e:
            logger.warning(f"LLM generation failed ({model}): {e}. Using deterministic primary fallback.")
            return None

llm_router = LLMRouter()

