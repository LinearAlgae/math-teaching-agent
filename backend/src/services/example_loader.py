from __future__ import annotations

import logging
import re
from collections import Counter
from pathlib import Path

from src.config import MARKDOWN_OUTPUT_DIR, PEDAGOGY_BLUEPRINT_PATH

logger = logging.getLogger(__name__)


MATH_TOPICS = [
    "对数", "logarithm", "指数",
    "几何", "geometry", "图形", "三角", "三角形",
    "代数", "algebra",
    "方程", "方程式", "equation", "不等式",
    "微积分", "calculus", "微分", "积分", "导数",
    "三角函数", "正弦", "余弦", "正切",
    "函数", "function",
    "概率", "probability", "统计", "statistics",
    "向量", "vector",
    "矩阵", "matrix",
    "数列", "sequence",
    "复数", "complex",
    "直线", "圆", "椭圆", "抛物线", "双曲线",
    "排列", "组合",
    "乘法", "除法", "加法", "减法",
    "分数", "小数", "百分比",
    "面积", "体积", "周长",
    "集合", "逻辑",
]


class ResourceRetriever:
    def __init__(self, resources_dir: Path = MARKDOWN_OUTPUT_DIR):
        self.resources_dir = resources_dir
        self._file_index: list[tuple[Path, float, str]] = []  # (path, quality_score, text)
        self._indexed = False

    def _compact(self, text: str) -> str:
        text = re.sub(r"\[Images?:.*?\]", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\[Image \d+.*?\]:?", "", text)
        text = re.sub(r"\n{4,}", "\n\n\n", text)
        text = re.sub(r"^[\d\s]{1,10}$", "", text, flags=re.MULTILINE)
        return text.strip()

    def _quality_score(self, text: str) -> float:
        lines = text.split("\n")
        if not lines:
            return 0.0
        meaningful = sum(1 for l in lines if len(l.strip()) > 10)
        total = len(lines)
        return meaningful / max(total, 1)

    def _build_index(self):
        if self._indexed:
            return
        self._indexed = True
        if not self.resources_dir.exists():
            logger.warning(f"Resources directory not found: {self.resources_dir}")
            return

        for md_file in sorted(self.resources_dir.rglob("*.md")):
            try:
                content = md_file.read_text(encoding="utf-8", errors="ignore")
                compacted = self._compact(content)
                score = self._quality_score(compacted)
                if score > 0.3 and len(compacted) > 200:
                    self._file_index.append((md_file, score, compacted))
            except Exception:
                continue

        self._file_index.sort(key=lambda x: -x[1])
        logger.info(f"Indexed {len(self._file_index)} resource files")

    def get_examples_for_subject(self, subject: str, max_chars: int = 6000) -> list[str]:
        self._build_index()

        subject_lower = subject.lower()
        query_terms = set(re.findall(r"[\w\u4e00-\u9fff]+", subject_lower))

        scored: list[tuple[float, str, str]] = []
        for fpath, quality, text in self._file_index:
            text_lower = text.lower()
            term_matches = sum(1 for t in query_terms if t in text_lower)
            topic_matches = sum(1 for t in MATH_TOPICS if t in text_lower and t in subject_lower)
            rel_score = term_matches * 0.5 + topic_matches * 5.0
            if rel_score > 0:
                scored.append((rel_score, str(fpath.name), text))

        scored.sort(key=lambda x: -x[0])

        results: list[str] = []
        total = 0
        seen_texts: set[str] = set()

        for score, name, text in scored:
            if total >= max_chars:
                break
            excerpt = text[:3000].strip()
            if len(excerpt) > 100:
                dedup_key = excerpt[:100]
                if dedup_key not in seen_texts:
                    seen_texts.add(dedup_key)
                    results.append(f"参考资源 {name}：\n{excerpt}")
                    total += len(excerpt)

        return results

    def get_blueprint_content(self) -> str | None:
        if PEDAGOGY_BLUEPRINT_PATH.exists():
            return PEDAGOGY_BLUEPRINT_PATH.read_text(encoding="utf-8")
        return None
