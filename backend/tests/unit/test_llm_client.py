import pytest

from src.services.llm_client import LLMClient


@pytest.fixture
def llm_client():
    return LLMClient("http://127.0.0.1:1234")


@pytest.mark.asyncio
async def test_llm_client_chat_complete(llm_client):
    messages = [{"role": "user", "content": "What is 2+2?"}]
    response = await llm_client.chat_complete(messages)
    assert isinstance(response, str)
    assert len(response) > 0


@pytest.mark.asyncio
async def test_llm_client_chat_stream(llm_client):
    messages = [{"role": "user", "content": "Hello"}]
    chunks = []
    async for chunk in llm_client.chat_stream(messages):
        chunks.append(chunk)
    assert isinstance(chunks, list)


@pytest.mark.asyncio
async def test_llm_client_get_models(llm_client):
    models = await llm_client.get_models()
    assert isinstance(models, list)
