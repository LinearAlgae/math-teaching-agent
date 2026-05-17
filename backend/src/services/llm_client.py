from __future__ import annotations

import json
import logging
import re
from collections.abc import AsyncGenerator

import httpx

from src.config import (
    LM_STUDIO_CHAT_ENDPOINT,
    LM_STUDIO_MODEL,
    LM_STUDIO_MODELS_ENDPOINT,
    LM_STUDIO_TEMPERATURE,
    LM_STUDIO_TIMEOUT,
    LM_STUDIO_URL,
    PROMPTS_DIR,
)
from src.services.example_loader import MATH_TOPICS

logger = logging.getLogger(__name__)

StreamToken = tuple[str, str]  # (type, content): "reasoning", "content", or "complete"


def _load_analysis_prompt() -> str:
    path = PROMPTS_DIR / "analysis_keywords.txt"
    if path.exists():
        return path.read_text(encoding="utf-8").strip()
    return ""


ANALYSIS_SYSTEM_PROMPT = _load_analysis_prompt()


def _clean_keywords(text: str) -> str:
    text = re.sub(r"[\[\]【】\"'「」『』*]", "", text)
    parts = [p.strip() for p in text.replace("\n", ",").split(",") if p.strip()]
    return ", ".join(parts[:10])


def _extract_keywords_from_text(text: str) -> str:
    terms = set(re.findall(r"[\w\u4e00-\u9fff]+", text.lower()))
    matched = [t for t in MATH_TOPICS if t in terms]
    return ", ".join(matched[:8]) if matched else ""


class LLMClient:
    def __init__(self, base_url: str = LM_STUDIO_URL):
        self.base_url = base_url.rstrip("/")
        self.chat_endpoint = LM_STUDIO_CHAT_ENDPOINT
        self.models_endpoint = LM_STUDIO_MODELS_ENDPOINT
        self.timeout = LM_STUDIO_TIMEOUT
        self._cached_model: str | None = None

    async def _get_loaded_model(self) -> str | None:
        if self._cached_model:
            return self._cached_model
        configured = LM_STUDIO_MODEL
        if configured:
            self._cached_model = configured
            return configured
        try:
            models = await self.get_models()
            if models:
                self._cached_model = models[0].get("id")
                return self._cached_model
        except Exception:
            pass
        return None

    async def analyze_query(
        self,
        user_message: str,
        reasoning_effort: str | None = None,
        max_tokens: int | None = None,
    ) -> str:
        model = await self._get_loaded_model()
        url = f"{self.base_url}{self.chat_endpoint}"
        payload: dict = {
            "model": model or "",
            "system_prompt": ANALYSIS_SYSTEM_PROMPT,
            "input": user_message,
            "stream": False,
            "temperature": 0.3,
            "store": False,
        }
        if reasoning_effort is not None:
            payload["reasoning"] = reasoning_effort
        if max_tokens is not None:
            payload["max_output_tokens"] = max_tokens
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                data = response.json()
                for item in data.get("output", []):
                    if item.get("type") == "message":
                        content = item.get("content", "")
                        return _clean_keywords(content)
                for item in data.get("output", []):
                    if item.get("type") == "reasoning":
                        content = item.get("content", "")
                        keywords = _extract_keywords_from_text(content)
                        if keywords:
                            return keywords
        except Exception as e:
            logger.warning(f"analyze_query failed: {e}")
        return ""

    async def chat_stream(
        self,
        system_prompt: str,
        user_message: str,
        previous_response_id: str | None = None,
        temperature: float = LM_STUDIO_TEMPERATURE,
    ) -> AsyncGenerator[StreamToken, None]:
        model = await self._get_loaded_model()
        url = f"{self.base_url}{self.chat_endpoint}"
        payload: dict = {
            "model": model or "",
            "system_prompt": system_prompt,
            "input": user_message,
            "stream": True,
            "temperature": temperature,
            "store": True,
        }
        if previous_response_id:
            payload["previous_response_id"] = previous_response_id

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            async with client.stream("POST", url, json=payload) as response:
                response.raise_for_status()
                current_event = ""
                async for line in response.aiter_lines():
                    if line.startswith("event: "):
                        current_event = line[7:].strip()
                    elif line.startswith("data: "):
                        data_str = line[6:].strip()
                        if not data_str:
                            continue
                        try:
                            event_data = json.loads(data_str)
                            if current_event == "reasoning.delta":
                                content = event_data.get("content", "")
                                if content:
                                    yield ("reasoning", content)
                            elif current_event == "message.delta":
                                content = event_data.get("content", "")
                                if content:
                                    yield ("content", content)
                            elif current_event == "chat.end":
                                result = event_data.get("result", {})
                                response_id = result.get("response_id", "")
                                if response_id:
                                    yield ("complete", response_id)
                                return
                        except json.JSONDecodeError:
                            continue

    async def chat_complete(
        self,
        system_prompt: str,
        user_message: str,
        previous_response_id: str | None = None,
        temperature: float = LM_STUDIO_TEMPERATURE,
    ) -> str:
        model = await self._get_loaded_model()
        url = f"{self.base_url}{self.chat_endpoint}"
        payload: dict = {
            "model": model or "",
            "system_prompt": system_prompt,
            "input": user_message,
            "stream": False,
            "temperature": temperature,
            "store": False,
        }
        if previous_response_id:
            payload["previous_response_id"] = previous_response_id

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            outputs = data.get("output", [])
            for item in outputs:
                if item.get("type") == "message":
                    return item.get("content", "")
            return ""

    async def get_models(self) -> list[dict]:
        url = f"{self.base_url}{self.models_endpoint}"
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json().get("models", [])

    async def chat_stream_with_images(
        self,
        system_prompt: str,
        user_message: str,
        images: list[dict],
        previous_response_id: str | None = None,
        temperature: float = LM_STUDIO_TEMPERATURE,
    ) -> AsyncGenerator[str, None]:
        model = await self._get_loaded_model()
        url = f"{self.base_url}{self.chat_endpoint}"
        input_parts: list[dict] = []
        for img in images:
            mime = img.get("mime_type", "image/png")
            input_parts.append({
                "type": "image",
                "data_url": f"data:{mime};base64,{img['data']}",
            })
        input_parts.append({"type": "message", "content": user_message or ""})

        payload: dict = {
            "model": model or "",
            "system_prompt": system_prompt,
            "input": input_parts,
            "stream": True,
            "temperature": temperature,
            "store": False,
        }
        if previous_response_id:
            payload["previous_response_id"] = previous_response_id

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            async with client.stream("POST", url, json=payload) as response:
                response.raise_for_status()
                current_event = ""
                async for line in response.aiter_lines():
                    if line.startswith("event: "):
                        current_event = line[7:].strip()
                    elif line.startswith("data: "):
                        data_str = line[6:].strip()
                        if not data_str:
                            continue
                        try:
                            event_data = json.loads(data_str)
                            if current_event == "message.delta":
                                content = event_data.get("content", "")
                                if content:
                                    yield content
                            elif current_event == "chat.end":
                                return
                        except json.JSONDecodeError:
                            continue
