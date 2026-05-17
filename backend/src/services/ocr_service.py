from __future__ import annotations

import base64
import io
import logging

try:
    import pytesseract
    from PIL import Image
    HAS_TESSERACT = True
except ImportError:
    HAS_TESSERACT = False

logger = logging.getLogger(__name__)


class OCRService:
    def __init__(self):
        if not HAS_TESSERACT:
            logger.warning("pytesseract not installed. OCR fallback disabled.")

    async def extract_text_from_image(self, image_base64: str, mime_type: str) -> str:
        if not HAS_TESSERACT:
            return ""

        try:
            image_data = base64.b64decode(image_base64)
            image = Image.open(io.BytesIO(image_data))
            text = pytesseract.image_to_string(image)
            return text.strip()
        except Exception as e:
            logger.error(f"OCR extraction failed: {e}")
            return ""
