from src.services.pedagogy import build_system_prompt


def test_build_system_prompt_student():
    messages = build_system_prompt(role="student")
    assert isinstance(messages, list)
    assert messages[0]["role"] == "system"
    assert "数学教学助手" in messages[0]["content"]


def test_build_system_prompt_teacher():
    messages = build_system_prompt(role="teacher")
    assert "教师模式" in messages[0]["content"]


def test_build_system_prompt_with_subject():
    messages = build_system_prompt(role="student", subject="logarithms")
    assert "logarithms" in messages[0]["content"]


def test_build_system_prompt_with_history():
    history = [
        {"role": "user", "content": "What is x?"},
        {"role": "assistant", "content": "x is a variable."},
    ]
    messages = build_system_prompt(role="student", conversation_history=history)
    assert len(messages) > 2
    assert messages[1]["content"] == "What is x?"
