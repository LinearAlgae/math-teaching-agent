from __future__ import annotations

import uuid
from datetime import UTC, datetime
from enum import Enum

from pydantic import BaseModel, Field, field_validator


class ImageAttachment(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    filename: str
    mimeType: str
    sizeBytes: int
    data: str  # base64 encoded
    extractedText: str | None = None


class MessageRole(str, Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    AUTO = "auto"


class UserMessage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    text: str = ""
    images: list[ImageAttachment] = Field(default_factory=list)
    role: MessageRole = MessageRole.AUTO

    @field_validator("text", "images")
    @classmethod
    def check_at_least_one(cls, v: str | list, info) -> str | list:
        return v


class ResponseStatus(str, Enum):
    STREAMING = "streaming"
    COMPLETE = "complete"
    ERROR = "error"


class PedagogyPhase(str, Enum):
    SLOW_FOUNDATION = "slow-foundation"
    FAST_DERIVATION = "fast-derivation"
    SLOW_REFLECTION = "slow-reflection"


class SystemResponse(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    completedAt: datetime | None = None
    content: str = ""
    status: ResponseStatus = ResponseStatus.STREAMING
    errorMessage: str | None = None
    pedagogyPhase: PedagogyPhase | None = None


class SessionMessage(BaseModel):
    type: str  # "user" or "system"
    data: dict


class ConversationSession(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    createdAt: datetime = Field(default_factory=lambda: datetime.now(UTC))
    lastActivityAt: datetime = Field(default_factory=lambda: datetime.now(UTC))
    messages: list[SessionMessage] = Field(default_factory=list)
    role: MessageRole = MessageRole.AUTO
    expired: bool = False
    subject: str | None = None
    previous_response_id: str | None = None
