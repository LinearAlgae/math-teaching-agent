import os
from pathlib import Path

# LM Studio configuration
LM_STUDIO_URL = os.getenv("LM_STUDIO_URL", "http://127.0.0.1:1234")
LM_STUDIO_CHAT_ENDPOINT = os.getenv("LM_STUDIO_CHAT_ENDPOINT", "/api/v1/chat")
LM_STUDIO_MODELS_ENDPOINT = os.getenv("LM_STUDIO_MODELS_ENDPOINT", "/api/v1/models")
LM_STUDIO_TIMEOUT = int(os.getenv("LM_STUDIO_TIMEOUT", "1800"))
LM_STUDIO_TEMPERATURE = float(os.getenv("LM_STUDIO_TEMPERATURE", "0.7"))
LM_STUDIO_MODEL = os.getenv("LM_STUDIO_MODEL", "qwen3.5-4b")

# Server configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")

# Pedagogical resources
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
RESOURCE_DIR = PROJECT_ROOT / "resource"
MARKDOWN_OUTPUT_DIR = RESOURCE_DIR / "markdown_output"
PEDAGOGY_BLUEPRINT_PATH = RESOURCE_DIR / "blueprints" / "YouTube Math Pedagogy Instructional Blueprint.md"
PROMPTS_DIR = RESOURCE_DIR / "prompts"

# Session configuration
SESSION_TIMEOUT_MINUTES = int(os.getenv("SESSION_TIMEOUT_MINUTES", "30"))

# Image configuration
MAX_IMAGE_SIZE_BYTES = 10 * 1024 * 1024  # 10MB
ALLOWED_IMAGE_TYPES = {"image/png", "image/jpeg", "image/webp"}
