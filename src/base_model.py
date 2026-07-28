"""
Chạy mô hình thuần trên bộ test cases để quan sát hallucination.

Không system prompt, không tool, không dữ liệu trường/điểm chuẩn/thị trường,
không grounding. Output được giữ nguyên để người đánh giá xác định model:
- thừa nhận không biết dữ liệu thực tế;
- hay tự bịa thông tin nhưng trình bày như sự thật.
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from providers import get_llm_provider


def load_test_cases() -> list[dict[str, Any]]:
    """Đọc nguyên bộ câu hỏi, không thêm ngữ cảnh hay đáp án kỳ vọng vào prompt."""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    test_path = os.path.join(project_root, "config", "test_cases.json")
    with open(test_path, "r", encoding="utf-8") as file:
        test_cases = json.load(file)
    if not isinstance(test_cases, list) or not test_cases:
        raise ValueError("config/test_cases.json phải là danh sách không rỗng.")
    return test_cases


def run_base_model(question: str, provider) -> str:
    """Gọi model đúng một lần với câu hỏi thuần và không có system prompt."""
    return provider.generate(question)


def main() -> int:
    """Chạy toàn bộ test cases và in raw output phục vụ đánh giá thủ công."""
    provider = get_llm_provider()
    model_name = getattr(provider, "model_name", "offline-mock")

    print("=== BASE MODEL: KHÔNG PROMPT, KHÔNG TOOL, KHÔNG GROUNDING ===")
    print(f"Provider: {provider.__class__.__name__}")
    print(f"Model: {model_name}")

    responses: list[str] = []
    for test_case in load_test_cases():
        question = str(test_case["question"])
        response = run_base_model(question, provider)
        responses.append(response)

        print(f"\n--- TEST CASE #{test_case['id']}: {test_case['category']} ---")
        print(f"Question: {question}")
        print("System prompt: NONE")
        print("Tool calls: 0")
        print("Extra context: NONE")
        print(f"Raw response:\n{response}")

    provider_errors = (
        "[Gemini Error]",
        "[Gemini Exception]",
        "[OpenRouter Error]",
        "[OpenRouter Exception]",
        "[Anthropic Error]",
        "[Anthropic Exception]",
        "[OpenAI Error]",
        "[OpenAI Exception]",
    )
    if any(response.startswith(provider_errors) for response in responses):
        print("\nProvider lỗi. Kiểm tra API key trong .env rồi chạy lại.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
