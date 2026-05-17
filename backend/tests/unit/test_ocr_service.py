import pytest

from src.services.ocr_service import OCRService


@pytest.mark.asyncio
async def test_ocr_empty_image():
    ocr = OCRService()
    text = await ocr.extract_text_from_image("", "image/png")
    assert text == ""
