"""
Mốc 2: chạy Chatbot Baseline trên toàn bộ test cases.

Baseline chỉ gọi LLM đúng một lần cho mỗi câu hỏi và không import/execute tool.
ReAct orchestration được triển khai ở Mốc 3.
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any

from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from prompts import CHATBOT_BASELINE_PROMPT
from providers import get_llm_provider

load_dotenv()


def load_test_cases() -> list[dict[str, Any]]:
    """Load and validate the Role 1 test-case list."""
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(project_dir, "config", "test_cases.json")
    with open(config_path, "r", encoding="utf-8") as file:
        cases = json.load(file)
    if not isinstance(cases, list) or not cases:
        raise ValueError("config/test_cases.json phải là danh sách không rỗng.")
    return cases


def run_baseline_chatbot(user_query: str, provider) -> str:
    """Run exactly one LLM call without exposing or executing any tool."""
    return provider.generate(user_query, system_prompt=CHATBOT_BASELINE_PROMPT)


def run_all_baseline_tests(provider) -> list[dict[str, Any]]:
    """Run all configured test cases and return serializable observations."""
    results: list[dict[str, Any]] = []
    for test_case in load_test_cases():
        response = run_baseline_chatbot(test_case["question"], provider)
        results.append(
            {
                "id": test_case["id"],
                "category": test_case["category"],
                "question": test_case["question"],
                "expected_behavior": test_case["expected_behavior"],
                "tool_calls": 0,
                "response": response,
            }
        )
    return results


def main() -> int:
    """CLI entry point for Mốc 2 baseline evaluation."""
    provider = get_llm_provider()
    model_name = getattr(provider, "model_name", "offline-mock")
    print("=== MỐC 2: BASELINE CHATBOT HƯỚNG NGHIỆP ===")
    print(f"Provider: {provider.__class__.__name__}")
    print(f"Model: {model_name}")

    results = run_all_baseline_tests(provider)
    for result in results:
        print(f"\n--- TEST CASE #{result['id']}: {result['category']} ---")
        print(f"Question: {result['question']}")
        print(f"Tool calls: {result['tool_calls']}")
        print(f"Response:\n{result['response']}")

    has_provider_error = any(
        str(result["response"]).startswith(("[Gemini Error]", "[Gemini Exception]"))
        for result in results
    )
    if has_provider_error:
        print("\nCần điền GEMINI_API_KEY trong .env rồi chạy lại.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
