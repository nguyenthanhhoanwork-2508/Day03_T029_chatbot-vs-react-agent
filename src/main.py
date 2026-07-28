"""
Cầu nối giữa Streamlit UI và ReAct Agent backend.

``app.py`` chỉ phụ thuộc vào ``ChatService.chat``. File này chịu trách nhiệm:
- gọi provider với ``REACT_SYSTEM_PROMPT``;
- parse ``Action: tool_name[JSON]``;
- thực thi đúng tool trong ``AVAILABLE_TOOLS``;
- đưa Observation thật về model;
- dừng bằng Final Answer hoặc guardrail an toàn.
"""

from __future__ import annotations

import json
import re
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
from dataclasses import asdict, dataclass
from typing import Any

from prompts import MAX_ITERATIONS, REACT_SYSTEM_PROMPT, TIMEOUT_SECONDS
from providers import BaseLLMProvider, get_llm_provider
from tools import AVAILABLE_TOOLS


PROVIDER_ERROR_PREFIXES = (
    "[Gemini Error]",
    "[Gemini Exception]",
    "[OpenRouter Error]",
    "[OpenRouter Exception]",
    "[Anthropic Error]",
    "[Anthropic Exception]",
    "[OpenAI Error]",
    "[OpenAI Exception]",
)

FINAL_ANSWER_PATTERN = re.compile(r"Final\s+Answer\s*:\s*(.+)", re.IGNORECASE | re.DOTALL)
ACTION_START_PATTERN = re.compile(
    r"Action\s*:\s*([A-Za-z_][A-Za-z0-9_]*)\s*\[",
    re.IGNORECASE,
)
INTERNAL_SOURCE_PATTERN = re.compile(
    r"\(?\s*(?:Nguồn|Source)\s*:\s*Observation\s+"
    r"(?:từ|của|from)\s+[`'\"]?([A-Za-z_][A-Za-z0-9_]*)[`'\"]?\s*\)?",
    re.IGNORECASE,
)
INTERNAL_TRACE_LINE_PATTERN = re.compile(
    r"^\s*(?:[-*]\s*)?(?:\*\*)?"
    r"(?:Thought|Action|Observation)(?:\*\*)?\s*:",
    re.IGNORECASE,
)

PUBLIC_TOOL_SOURCE_LABELS = {
    "get_job_market_trend": "Dữ liệu thị trường lao động đã được kiểm chứng",
    "compare_regions_by_industry": "Dữ liệu thị trường lao động đã được kiểm chứng",
    "get_top_industries_by_region": "Dữ liệu thị trường lao động đã được kiểm chứng",
    "list_job_market_options": "Danh mục thị trường lao động trong hệ thống",
    "get_admission_by_university": "Dữ liệu tuyển sinh đã được kiểm chứng",
    "get_admission_by_region": "Dữ liệu tuyển sinh đã được kiểm chứng",
    "get_admission_by_major_group": "Dữ liệu tuyển sinh đã được kiểm chứng",
    "list_admission_options": "Danh mục tuyển sinh trong hệ thống",
}


@dataclass(frozen=True)
class ChatResponse:
    """Stable response contract consumed by the UI."""

    content: str
    backend: str
    provider: str
    model: str
    tool_calls: int
    is_error: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Return a Streamlit-session-safe representation."""
        return asdict(self)


@dataclass(frozen=True)
class ParsedAction:
    """One parsed ReAct action and the end of its trusted output segment."""

    tool_name: str
    arguments: dict[str, Any]
    output_end: int


class ChatService:
    """Single integration boundary for the ReAct orchestration."""

    backend_name = "ReAct Agent"
    max_message_length = 4_000

    def __init__(self, provider: BaseLLMProvider | None = None) -> None:
        self._provider = provider or get_llm_provider()
        self.provider_name = self._provider.__class__.__name__
        self.model_name = getattr(self._provider, "model_name", "offline-mock")

    def chat(self, message: str) -> ChatResponse:
        """Resolve one user question through the guarded ReAct loop."""
        clean_message = str(message).strip()
        if not clean_message:
            return self._error("Vui lòng nhập câu hỏi trước khi gửi.")
        if len(clean_message) > self.max_message_length:
            return self._error(
                f"Câu hỏi vượt quá {self.max_message_length:,} ký tự. "
                "Vui lòng rút gọn rồi thử lại."
            )

        try:
            return self._run_react(clean_message)
        except Exception as error:
            return self._error(f"Không thể hoàn tất phiên tư vấn: {error}")

    def _run_react(self, question: str) -> ChatResponse:
        scratchpad: list[str] = []
        seen_actions: set[str] = set()
        tool_calls = 0

        for step in range(1, MAX_ITERATIONS + 1):
            model_prompt = self._build_model_prompt(question, scratchpad, step)
            model_output = str(
                self._provider.generate(
                    model_prompt,
                    system_prompt=REACT_SYSTEM_PROMPT,
                )
            ).strip()

            if model_output.startswith(PROVIDER_ERROR_PREFIXES):
                return self._response(
                    model_output,
                    tool_calls=tool_calls,
                    is_error=True,
                )

            final_answer = self._extract_final_answer(model_output)
            if final_answer is not None:
                return self._response(
                    self._sanitize_public_answer(final_answer),
                    tool_calls=tool_calls,
                    is_error=False,
                )

            try:
                action = self._parse_action(model_output)
            except ValueError as error:
                scratchpad.extend(
                    [
                        self._safe_model_step(model_output),
                        f"Observation: LỖI: {error}",
                    ]
                )
                continue

            trusted_step = model_output[: action.output_end].strip()
            action_key = (
                f"{action.tool_name}:"
                f"{json.dumps(action.arguments, ensure_ascii=False, sort_keys=True)}"
            )

            if action.tool_name not in AVAILABLE_TOOLS:
                observation = (
                    f"LỖI: Tool '{action.tool_name}' không tồn tại. "
                    f"Tools hợp lệ: {', '.join(AVAILABLE_TOOLS)}."
                )
            elif action_key in seen_actions:
                observation = (
                    "LỖI: Action này đã được gọi với cùng tham số. "
                    "Hãy dùng Observation hiện có, đổi tham số hoặc trả Final Answer."
                )
            else:
                seen_actions.add(action_key)
                observation = self._execute_tool(action.tool_name, action.arguments)
                tool_calls += 1

            scratchpad.extend(
                [
                    trusted_step,
                    f"Observation: {observation}",
                ]
            )

        return self._response(
            (
                "VeS chưa thể hoàn tất câu trả lời có kiểm chứng trong giới hạn "
                f"{MAX_ITERATIONS} bước. Vui lòng thu hẹp câu hỏi hoặc cung cấp rõ "
                "nhóm ngành, vùng miền hay trường bạn quan tâm."
            ),
            tool_calls=tool_calls,
            is_error=True,
        )

    def _build_model_prompt(
        self,
        question: str,
        scratchpad: list[str],
        step: int,
    ) -> str:
        history = "\n\n".join(scratchpad) if scratchpad else "(Chưa có Action/Observation.)"
        return (
            f"Question: {question}\n\n"
            f"ReAct Trace do ứng dụng kiểm soát:\n{history}\n\n"
            f"Vòng hiện tại: {step}/{MAX_ITERATIONS}.\n"
            "Hãy trả đúng một bước tiếp theo theo REACT_SYSTEM_PROMPT. "
            "Không tự tạo Observation."
        )

    @staticmethod
    def _extract_final_answer(model_output: str) -> str | None:
        match = FINAL_ANSWER_PATTERN.search(model_output)
        if match is None:
            return None
        answer = match.group(1).strip()
        if answer.endswith("```"):
            answer = answer[:-3].rstrip()
        return answer or None

    @staticmethod
    def _parse_action(model_output: str) -> ParsedAction:
        match = ACTION_START_PATTERN.search(model_output)
        if match is None:
            raise ValueError(
                "Phản hồi model thiếu Action hợp lệ hoặc Final Answer."
            )

        payload_start = match.end()
        depth = 1
        in_string = False
        escaped = False
        payload_end = None

        for index in range(payload_start, len(model_output)):
            character = model_output[index]
            if in_string:
                if escaped:
                    escaped = False
                elif character == "\\":
                    escaped = True
                elif character == '"':
                    in_string = False
                continue

            if character == '"':
                in_string = True
            elif character == "[":
                depth += 1
            elif character == "]":
                depth -= 1
                if depth == 0:
                    payload_end = index
                    break

        if payload_end is None:
            raise ValueError("Action thiếu dấu ']' kết thúc.")

        raw_arguments = model_output[payload_start:payload_end].strip() or "{}"
        try:
            arguments = json.loads(raw_arguments)
        except json.JSONDecodeError as error:
            raise ValueError(
                f"Tham số Action không phải JSON hợp lệ: {error.msg}."
            ) from error

        if not isinstance(arguments, dict):
            raise ValueError("Tham số Action phải là một JSON object.")

        return ParsedAction(
            tool_name=match.group(1),
            arguments=arguments,
            output_end=payload_end + 1,
        )

    @staticmethod
    def _safe_model_step(model_output: str) -> str:
        clean_output = model_output.strip()
        if not clean_output:
            return "Thought: Model trả về nội dung rỗng."
        observation_position = clean_output.lower().find("observation:")
        if observation_position >= 0:
            clean_output = clean_output[:observation_position].rstrip()
        return clean_output

    @staticmethod
    def _sanitize_public_answer(answer: str) -> str:
        """Remove internal ReAct/tool identifiers before content reaches the UI."""

        def replace_internal_source(match: re.Match[str]) -> str:
            tool_name = match.group(1)
            public_label = PUBLIC_TOOL_SOURCE_LABELS.get(
                tool_name,
                "Dữ liệu hệ thống đã được kiểm chứng",
            )
            return f"(Nguồn: {public_label})"

        public_answer = INTERNAL_SOURCE_PATTERN.sub(replace_internal_source, answer)
        public_lines = [
            line
            for line in public_answer.splitlines()
            if not INTERNAL_TRACE_LINE_PATTERN.match(line)
        ]
        public_answer = "\n".join(public_lines)

        for tool_name, public_label in PUBLIC_TOOL_SOURCE_LABELS.items():
            public_answer = re.sub(
                rf"\b{re.escape(tool_name)}\b",
                public_label,
                public_answer,
                flags=re.IGNORECASE,
            )

        public_answer = public_answer.strip()
        return public_answer or (
            "VeS đã xử lý yêu cầu nhưng không thể hiển thị câu trả lời an toàn. "
            "Vui lòng thử diễn đạt câu hỏi theo cách khác."
        )

    @staticmethod
    def _execute_tool(tool_name: str, arguments: dict[str, Any]) -> str:
        tool = AVAILABLE_TOOLS[tool_name]
        executor = ThreadPoolExecutor(max_workers=1)
        future = executor.submit(tool, **arguments)
        try:
            result = future.result(timeout=TIMEOUT_SECONDS)
            return str(result)
        except FutureTimeoutError:
            future.cancel()
            return (
                f"LỖI: Tool '{tool_name}' vượt quá timeout "
                f"{TIMEOUT_SECONDS} giây."
            )
        except TypeError as error:
            return f"LỖI: Tham số của tool '{tool_name}' không hợp lệ: {error}."
        except Exception as error:
            return f"LỖI: Tool '{tool_name}' thất bại: {error}."
        finally:
            executor.shutdown(wait=False, cancel_futures=True)

    def status(self) -> dict[str, str | int]:
        """Expose non-sensitive runtime metadata for the UI."""
        return {
            "backend": self.backend_name,
            "provider": self.provider_name,
            "model": self.model_name,
            "tool_calls": len(AVAILABLE_TOOLS),
        }

    def _response(
        self,
        content: str,
        *,
        tool_calls: int,
        is_error: bool,
    ) -> ChatResponse:
        return ChatResponse(
            content=content,
            backend=self.backend_name,
            provider=self.provider_name,
            model=self.model_name,
            tool_calls=tool_calls,
            is_error=is_error,
        )

    def _error(self, message: str) -> ChatResponse:
        return self._response(message, tool_calls=0, is_error=True)


def create_chat_service() -> ChatService:
    """Factory kept separate so UI can cache one provider instance."""
    return ChatService()
