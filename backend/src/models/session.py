from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta

from src.config import SESSION_TIMEOUT_MINUTES
from src.models.message import (
    ConversationSession,
    MessageRole,
    SessionMessage,
)


def serialize_session(session: ConversationSession) -> str:
    data = {
        "id": session.id,
        "createdAt": session.createdAt.isoformat(),
        "lastActivityAt": session.lastActivityAt.isoformat(),
        "messages": [m.model_dump() for m in session.messages],
        "role": (
            session.role.value
            if isinstance(session.role, MessageRole)
            else session.role
        ),
        "expired": session.expired,
        "subject": session.subject,
    }
    return json.dumps(data)


def deserialize_session(data: str) -> ConversationSession | None:
    try:
        obj = json.loads(data)
        messages = [SessionMessage(**m) for m in obj.get("messages", [])]
        return ConversationSession(
            id=obj["id"],
            createdAt=datetime.fromisoformat(obj["createdAt"]),
            lastActivityAt=datetime.fromisoformat(obj["lastActivityAt"]),
            messages=messages,
            role=MessageRole(obj.get("role", "auto")),
            expired=obj.get("expired", False),
            subject=obj.get("subject"),
        )
    except (json.JSONDecodeError, KeyError, ValueError):
        return None


def check_session_expired(
    session: ConversationSession,
    timeout_minutes: int = SESSION_TIMEOUT_MINUTES,
) -> bool:
    if session.expired:
        return True
    cutoff = datetime.now(UTC) - timedelta(minutes=timeout_minutes)
    return session.lastActivityAt < cutoff


def touch_session(session: ConversationSession) -> ConversationSession:
    session.lastActivityAt = datetime.now(UTC)
    session.expired = False
    return session
