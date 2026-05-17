from __future__ import annotations

import logging

from src.services.llm_client import LLMClient

logger = logging.getLogger(__name__)


class VisionDetector:
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
        self._cached_result: tuple[bool, str, str] | None = None

    async def detect_vision_support(self) -> tuple[bool, str, str]:
        if self._cached_result:
            return self._cached_result

        model_id = await self.llm_client._get_loaded_model()
        if not model_id:
            self._cached_result = (False, "no_models", "none")
            return self._cached_result

        try:
            models = await self.llm_client.get_models()
            for m in models:
                if m.get("id") == model_id:
                    capabilities = m.get("capabilities", {})
                    vision_supported = capabilities.get("vision", False)
                    if vision_supported:
                        self._cached_result = (True, "capabilities", model_id)
                    else:
                        self._cached_result = (False, "capabilities", model_id)
                    return self._cached_result
        except Exception as e:
            logger.warning(f"Failed to check model capabilities: {e}")

        self._cached_result = (True, "default", model_id)
        return self._cached_result
