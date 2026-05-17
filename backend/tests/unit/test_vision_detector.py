from unittest.mock import AsyncMock

import pytest

from src.services.llm_client import LLMClient
from src.services.vision_detector import VisionDetector


@pytest.fixture
def mock_client():
    client = AsyncMock(spec=LLMClient)
    client._get_loaded_model = AsyncMock()
    client.get_models = AsyncMock()
    return client


@pytest.mark.asyncio
async def test_vision_detector_no_models(mock_client):
    mock_client._get_loaded_model = AsyncMock(return_value=None)
    detector = VisionDetector(mock_client)
    supported, method, model = await detector.detect_vision_support()
    assert supported is False
    assert method == "no_models"
    assert model == "none"


@pytest.mark.asyncio
async def test_vision_detector_capabilities_vision(mock_client):
    mock_client._get_loaded_model = AsyncMock(return_value="qwen3.5-4b")
    mock_client.get_models = AsyncMock(return_value=[
        {"id": "qwen3.5-4b", "capabilities": {"vision": True}},
    ])
    detector = VisionDetector(mock_client)
    supported, method, model = await detector.detect_vision_support()
    assert supported is True
    assert method == "capabilities"
    assert model == "qwen3.5-4b"


@pytest.mark.asyncio
async def test_vision_detector_no_vision_capability(mock_client):
    mock_client._get_loaded_model = AsyncMock(return_value="llama-3-8b")
    mock_client.get_models = AsyncMock(return_value=[
        {"id": "llama-3-8b", "capabilities": {"vision": False}},
    ])
    detector = VisionDetector(mock_client)
    supported, method, model = await detector.detect_vision_support()
    assert supported is False
    assert method == "capabilities"
    assert model == "llama-3-8b"


@pytest.mark.asyncio
async def test_vision_detector_caching(mock_client):
    mock_client._get_loaded_model = AsyncMock(return_value="qwen3.5-4b")
    mock_client.get_models = AsyncMock(return_value=[
        {"id": "qwen3.5-4b", "capabilities": {"vision": True}},
    ])
    detector = VisionDetector(mock_client)
    supported1, method1, model1 = await detector.detect_vision_support()
    mock_client.get_models.reset_mock()
    mock_client._get_loaded_model.reset_mock()
    supported2, method2, model2 = await detector.detect_vision_support()
    assert supported1 is True
    assert supported2 is True
    assert method2 == "capabilities"
    mock_client.get_models.assert_not_called()
    mock_client._get_loaded_model.assert_not_called()


@pytest.mark.asyncio
async def test_vision_detector_default_fallback(mock_client):
    mock_client._get_loaded_model = AsyncMock(return_value="some-model")
    mock_client.get_models = AsyncMock(return_value=[])
    detector = VisionDetector(mock_client)
    supported, method, model = await detector.detect_vision_support()
    assert supported is True
    assert method == "default"
    assert model == "some-model"
