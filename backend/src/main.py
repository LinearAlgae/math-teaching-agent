from datetime import UTC, datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from src.api.middleware import add_error_handling_middleware
from src.api.routes import router
from src.config import CORS_ORIGINS
from src.services.llm_client import LLMClient
from src.services.vision_detector import VisionDetector

app = FastAPI(
    title="Math Teaching Agent API",
    description="NHM pedagogy-driven math teaching chat application",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=500)

add_error_handling_middleware(app)

app.include_router(router, prefix="/api")

llm_client = LLMClient()
vision_detector = VisionDetector(llm_client)


@app.get("/api/health")
async def health_check():
    llm_connected = False
    model_name = None
    vision_supported = False

    try:
        models = await llm_client.get_models()
        if models:
            llm_connected = True
            model_name = models[0].get("id", "unknown")
            vision_supported, _, _ = (
                await vision_detector.detect_vision_support()
            )
    except Exception:
        pass

    return {
        "status": "healthy",
        "llmConnected": llm_connected,
        "llmModel": model_name,
        "llmVisionSupported": vision_supported,
        "timestamp": datetime.now(UTC).isoformat(),
    }
