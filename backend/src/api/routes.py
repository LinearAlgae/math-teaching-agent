from __future__ import annotations

import base64
import json
import logging
import re
import uuid
from collections.abc import AsyncGenerator

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from src.models.message import (
    ConversationSession,
    ImageAttachment,
    MessageRole,
    SessionMessage,
)
from src.models.session import (
    check_session_expired,
    touch_session,
)
from src.services.example_loader import MATH_TOPICS, ResourceRetriever
from src.services.llm_client import LLMClient
from src.services.ocr_service import OCRService
from src.services.pedagogy import build_system_prompt, detect_role_from_input
from src.services.vision_detector import VisionDetector

router = APIRouter()

llm_client = LLMClient()
vision_detector = VisionDetector(llm_client)
ocr_service = OCRService()
example_loader = ResourceRetriever()

logger = logging.getLogger(__name__)

_sessions: dict[str, ConversationSession] = {}


def _extract_keywords(text: str) -> str:
    terms = set(re.findall(r"[\w\u4e00-\u9fff]+", text.lower()))
    matched = [t for t in terms if t in MATH_TOPICS]
    return ", ".join(matched) if matched else text


@router.post("/chat")
async def chat(
    text: str = Form(""),
    role: str = Form("auto"),
    session_id: str | None = Form(None, alias="sessionId"),  # noqa: N803
    files: list[UploadFile] | None = File(None),
) -> StreamingResponse:
    session: ConversationSession
    if session_id and session_id in _sessions:
        session = _sessions[session_id]
        if check_session_expired(session):
            session = ConversationSession()
    else:
        session = ConversationSession()

    resolved_role = role
    if role == "auto":
        resolved_role = detect_role_from_input(text)
    session.role = MessageRole(resolved_role)
    images: list[ImageAttachment] = []

    if files:
        for f in files:
            if f.size and f.size > 10 * 1024 * 1024:
                raise HTTPException(400, "图片过大（最大10MB）")
            content = await f.read()
            b64 = base64.b64encode(content).decode()
            img = ImageAttachment(
                filename=f.filename or "image",
                mimeType=f.content_type or "image/png",
                sizeBytes=len(content),
                data=b64,
            )
            images.append(img)

            vision_supported, _, _ = (
                await vision_detector.detect_vision_support()
            )
            if not vision_supported and img.data:
                extracted = await ocr_service.extract_text_from_image(
                    img.data, img.mimeType
                )
                text += f"\n[图片内容]：{extracted}"

    user_msg = SessionMessage(
        type="user",
        data={
            "text": text,
            "role": session.role.value,
            "images": len(images),
        },
    )
    session.messages.append(user_msg)
    touch_session(session)

    context_lines = []
    for m in session.messages[:-1]:
        role_label = "User" if m.type == "user" else "Assistant"
        content = m.data.get("text", "")
        if content:
            context_lines.append(f"{role_label}: {content}")
    context_lines = context_lines[-10:]

    blueprint = example_loader.get_blueprint_content()

    context = text
    if context_lines:
        context = "\n".join(context_lines) + f"\n\nUser: {text}"

    async def event_generator() -> AsyncGenerator[str, None]:
        response_id = str(uuid.uuid4())
        start_data = json.dumps({
            "sessionId": session.id,
            "responseId": response_id,
        })
        yield f"event: start\ndata: {start_data}\n\n"

        try:
            search_terms = _extract_keywords(text) if text else text

            status = json.dumps({"content": "正在分析问题关键词..."})
            yield f"event: reasoning\ndata: {status}\n\n"

            if text:
                try:
                    keywords = await llm_client.analyze_query(text)
                    if keywords.strip():
                        search_terms = keywords
                        logger.info(f"LLM analysis keywords: {keywords}")
                except Exception:
                    pass

            examples = example_loader.get_examples_for_subject(search_terms, max_chars=12000) if search_terms else []

            status = json.dumps({"content": f"已找到 {len(examples)} 份相关教学资料，正在生成回答..."})
            yield f"event: reasoning\ndata: {status}\n\n"
            system_prompt = build_system_prompt(
                role=session.role.value,
                subject=session.subject,
                examples=examples,
                blueprint=blueprint,
            )
            system_prompt_text = system_prompt[0]["content"]

            previous_id = getattr(session, "previous_response_id", None)
            if images:
                img_dicts = []
                for img in images:
                    img_dicts.append({
                        "data": img.data,
                        "mime_type": img.mimeType,
                    })
                stream = llm_client.chat_stream_with_images(
                    system_prompt=system_prompt_text,
                    user_message=context,
                    images=img_dicts,
                    previous_response_id=previous_id,
                )
                async for content_token in stream:
                    token_data = json.dumps({"content": content_token})
                    yield f"event: token\ndata: {token_data}\n\n"
            else:
                stream = llm_client.chat_stream(
                    system_prompt=system_prompt_text,
                    user_message=context,
                    previous_response_id=previous_id,
                )
                reasoning_parts: list[str] = []
                content_parts: list[str] = []
                new_response_id: str | None = None

                async for token_type, token in stream:
                    if token_type == "reasoning":
                        reasoning_parts.append(token)
                        token_data = json.dumps({"content": token})
                        yield f"event: reasoning\ndata: {token_data}\n\n"
                    elif token_type == "content":
                        content_parts.append(token)
                        token_data = json.dumps({"content": token})
                        yield f"event: token\ndata: {token_data}\n\n"
                    elif token_type == "complete":
                        new_response_id = token

                reasoning = "".join(reasoning_parts)
                full_content = "".join(content_parts)

                if new_response_id:
                    session.previous_response_id = new_response_id

                complete_data = json.dumps({
                    "responseId": response_id,
                    "reasoning": reasoning,
                    "fullContent": full_content,
                })
                yield f"event: complete\ndata: {complete_data}\n\n"

        except Exception as e:
            logger.exception("LLM streaming error")
            error_data = json.dumps({
                "message": str(e),
                "code": "LLM_ERROR",
            })
            yield f"event: error\ndata: {error_data}\n\n"

    _sessions[session.id] = session

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.get("/session/{session_id}")
async def get_session(session_id: str) -> dict:
    if session_id not in _sessions:
        raise HTTPException(404, "会话未找到")
    session = _sessions[session_id]
    return {
        "id": session.id,
        "createdAt": session.createdAt.isoformat(),
        "lastActivityAt": session.lastActivityAt.isoformat(),
        "role": session.role.value,
        "expired": session.expired,
        "subject": session.subject,
        "messages": [m.model_dump() for m in session.messages],
    }


@router.post("/vision/detect")
async def detect_vision() -> dict:
    supported, method, model = (
        await vision_detector.detect_vision_support()
    )
    return {
        "visionSupported": supported,
        "detectionMethod": method,
        "modelName": model,
    }
