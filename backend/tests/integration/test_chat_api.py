import pytest
from httpx import ASGITransport, AsyncClient


@pytest.mark.asyncio
async def test_health_endpoint():
    from src.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_chat_text_only():
    from src.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.post(
            "/api/chat",
            data={"text": "What is 2+2?"},
        )
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_chat_empty_input():
    from src.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.post("/api/chat", data={"text": ""})
    assert resp.status_code in (200, 422)


@pytest.mark.asyncio
async def test_chat_teacher_role():
    from src.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.post(
            "/api/chat",
            data={"text": "Create a lesson plan", "role": "teacher"},
        )
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_chat_multipart_image():
    from src.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.post(
            "/api/chat",
            data={"text": "Solve this problem"},
            files={
                "files": ("test.png", b"fake-png-content", "image/png")
            },
        )
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_chat_auto_role():
    from src.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.post(
            "/api/chat",
            data={"text": "What is a derivative?", "role": "auto"},
        )
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_chat_multiple_images():
    from src.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.post(
            "/api/chat",
            data={"text": "Compare these two diagram"},
            files=[
                ("files", ("img1.png", b"fake-png-1", "image/png")),
                ("files", ("img2.jpg", b"fake-jpg-2", "image/jpeg")),
            ],
        )
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_chat_image_only_no_text():
    from src.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.post(
            "/api/chat",
            data={"text": ""},
            files={
                "files": ("problem.png", b"fake-png-content", "image/png")
            },
        )
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_chat_session_persistence():
    from src.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp1 = await client.post(
            "/api/chat",
            data={"text": "First message"},
        )
        assert resp1.status_code == 200
        resp2 = await client.post(
            "/api/chat",
            data={"text": "Follow-up question"},
        )
        assert resp2.status_code == 200
