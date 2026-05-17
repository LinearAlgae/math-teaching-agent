from importlib import reload

import src.config as config


def test_default_lm_studio_url():
    reload(config)
    assert config.LM_STUDIO_URL == "http://127.0.0.1:1234"


def test_default_session_timeout():
    reload(config)
    assert config.SESSION_TIMEOUT_MINUTES == 30


def test_default_port():
    reload(config)
    assert config.PORT == 8000


def test_default_host():
    reload(config)
    assert config.HOST == "0.0.0.0"


def test_cors_origins_default():
    reload(config)
    assert "http://localhost:5173" in config.CORS_ORIGINS
    assert "http://127.0.0.1:5173" in config.CORS_ORIGINS


def test_max_image_size():
    from src.config import MAX_IMAGE_SIZE_BYTES
    assert MAX_IMAGE_SIZE_BYTES == 10 * 1024 * 1024


def test_allowed_image_types():
    from src.config import ALLOWED_IMAGE_TYPES
    assert "image/png" in ALLOWED_IMAGE_TYPES
    assert "image/jpeg" in ALLOWED_IMAGE_TYPES
    assert "image/webp" in ALLOWED_IMAGE_TYPES


def test_markdown_output_dir_exists():
    from src.config import MARKDOWN_OUTPUT_DIR
    assert MARKDOWN_OUTPUT_DIR.is_dir() or MARKDOWN_OUTPUT_DIR.parent.is_dir()


def test_lm_studio_endpoints():
    reload(config)
    assert config.LM_STUDIO_CHAT_ENDPOINT == "/api/v1/chat"
    assert config.LM_STUDIO_MODELS_ENDPOINT == "/api/v1/models"
