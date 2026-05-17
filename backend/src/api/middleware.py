import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

# fmt: off
ERROR_MESSAGES = {
    "LLM_UNAVAILABLE": (
        "学习引擎似乎没有响应。"
        " 让我们来看看发生了什么。"
    ),
    "INVALID_INPUT": (
        "让我看看你分享的内容……"
        " 请提供文字或图片来帮助我理解。"
    ),
    "IMAGE_TOO_LARGE": (
        "图片太大了！"
        " 能上传一张小一点的版本吗（10MB以内）？"
    ),
    "PAYLOAD_TOO_LARGE": (
        "你分享的内容太多了。"
        " 我们试着分成小部分来讨论吧。"
    ),
    "OCR_FAILED": (
        "我没能清晰地读出图片中的文字。"
        " 文字可能需要更清晰一些——"
        " 你能试试拍一张更清楚的照片吗？"
    ),
    "INTERNAL_ERROR": (
        "发生了意外错误。"
        " 我们一起来解决吧。"
    ),
}
# fmt: on


def add_error_handling_middleware(app: FastAPI):
    @app.exception_handler(Exception)
    async def exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        logger.error(f"Unhandled exception: {exc}", exc_info=True)

        error_msg = str(exc)

        if "connect" in error_msg.lower() or "connection" in error_msg.lower():
            user_message = ERROR_MESSAGES.get("LLM_UNAVAILABLE")
        elif "timeout" in error_msg.lower() or "timed out" in error_msg.lower():
            user_message = (
                "响应时间比预期长。"
                " 试试问一个更简单的问题吧。"
            )
        else:
            user_message = ERROR_MESSAGES.get("INTERNAL_ERROR")

        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": user_message,
                }
            },
        )
