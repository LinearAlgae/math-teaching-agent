from datetime import UTC, datetime, timedelta

from src.models.message import (
    ConversationSession,
    MessageRole,
    SessionMessage,
)
from src.models.session import (
    check_session_expired,
    deserialize_session,
    serialize_session,
    touch_session,
)


def test_serialize_deserialize_session():
    session = ConversationSession(id="test-123", role=MessageRole.STUDENT)
    session.messages = []

    serialized = serialize_session(session)
    restored = deserialize_session(serialized)

    assert restored is not None
    assert restored.id == session.id
    assert restored.role == MessageRole.STUDENT


def test_serialize_deserialize_with_messages():
    session = ConversationSession(id="test-456", role=MessageRole.TEACHER)
    session.messages = [
        SessionMessage(
            type="user",
            data={"text": "What is 2+2?", "role": "student"},
        ),
        SessionMessage(
            type="system",
            data={"content": "4", "status": "complete"},
        ),
    ]

    serialized = serialize_session(session)
    restored = deserialize_session(serialized)

    assert restored is not None
    assert len(restored.messages) == 2
    assert restored.role == MessageRole.TEACHER


def test_deserialize_invalid_json():
    result = deserialize_session("not valid json")
    assert result is None


def test_deserialize_missing_fields():
    result = deserialize_session('{"id": "test"}')
    assert result is None


def test_check_session_expired_false():
    session = ConversationSession(expired=False)
    assert not check_session_expired(session)


def test_check_session_expired_true():
    session = ConversationSession(
        lastActivityAt=datetime.now(UTC) - timedelta(hours=1)
    )
    assert check_session_expired(session)


def test_check_session_expired_already_marked():
    session = ConversationSession(expired=True)
    assert check_session_expired(session)


def test_check_session_expired_custom_timeout():
    session = ConversationSession(
        lastActivityAt=datetime.now(UTC) - timedelta(minutes=5)
    )
    assert check_session_expired(session, timeout_minutes=3)
    assert not check_session_expired(session, timeout_minutes=10)


def test_touch_session_updates_timestamp():
    session = ConversationSession(
        lastActivityAt=datetime.now(UTC) - timedelta(hours=1),
        expired=True,
    )
    touch_session(session)
    assert not session.expired
    cutoff = datetime.now(UTC) - timedelta(minutes=1)
    assert session.lastActivityAt > cutoff


def test_session_with_auto_role():
    session = ConversationSession(role=MessageRole.AUTO)
    serialized = serialize_session(session)
    restored = deserialize_session(serialized)
    assert restored.role == MessageRole.AUTO


def test_session_with_subject():
    session = ConversationSession(
        role=MessageRole.STUDENT,
        subject="logarithms",
    )
    serialized = serialize_session(session)
    restored = deserialize_session(serialized)
    assert restored.subject == "logarithms"
