from __future__ import annotations

from pathlib import Path

from src.config import PROMPTS_DIR


def _load_prompt(role: str) -> str:
    filename = f"teaching_{role}.txt"
    path = PROMPTS_DIR / filename
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


TEACHER_KEYWORDS = [
    "教案", "教学大纲", "课程", "教学法",
    "年级", "评估", "上课", "教学", "课堂",
    " pedagogy", "练习单", "习题", "作业",
    "学习目标", "进度", "单元计划",
]

STUDENT_KEYWORDS = [
    "帮助", "解答", "解释", "作业", "问题",
    "不懂", "不明白", "困惑", "卡住", "怎么做",
    "什么是", "步骤", "答案", "提问",
]


def detect_role_from_input(text: str) -> str:
    teacher_score = sum(1 for kw in TEACHER_KEYWORDS if kw in text)
    student_score = sum(1 for kw in STUDENT_KEYWORDS if kw in text)
    if teacher_score > student_score:
        return "teacher"
    return "student"


def build_system_prompt(
    role: str = "student",
    subject: str | None = None,
    examples: list[str] | None = None,
    blueprint: str | None = None,
    conversation_history: list[dict] | None = None,
) -> list[dict]:
    prompt = _load_prompt(role)

    if subject:
        prompt += f"\n\n当前科目：{subject}"

    if blueprint:
        prompt += f"\n\n参考教学蓝图（NHM教学法详细说明）：\n{blueprint}\n"

    if examples:
        prompt += "\n\n相关教学资源参考：\n"
        for ex in examples:
            prompt += f"\n{ex}\n"

    messages = [{"role": "system", "content": prompt}]

    if conversation_history:
        messages.extend(conversation_history[-6:])

    return messages
