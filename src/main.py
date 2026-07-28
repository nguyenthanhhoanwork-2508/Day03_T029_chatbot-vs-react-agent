"""
Application bridge giữa UI và AI backend.

UI chỉ phụ thuộc vào ``ChatService.chat``. Trong giai đoạn hiện tại, service gọi
base model thuần: không system prompt, không tools và không grounding. Khi ReAct
Agent hoàn thành, chỉ thay implementation trong file này; ``app.py`` không cần
biết cấu trúc của ``prompts.py`` hoặc ``tools.py``.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from base_model import run_base_model
from providers import BaseLLMProvider, get_llm_provider


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


class ChatService:
    """Single integration boundary for current and future chat backends."""

    backend_name = "Base model"
    max_message_length = 4_000

    def __init__(self, provider: BaseLLMProvider | None = None) -> None:
        self._provider = provider or get_llm_provider()
        self.provider_name = self._provider.__class__.__name__
        self.model_name = getattr(self._provider, "model_name", "offline-mock")

    def chat(self, message: str) -> ChatResponse:
        """Send one isolated user message to the pure base model.

        Current guarantees:
        - no import from ``prompts.py`` or ``tools.py``;
        - no system prompt;
        - no conversation history;
        - no tool schema or tool execution;
        - exactly one provider call.
        """
        clean_message = str(message).strip()
        if not clean_message:
            return self._error("Vui lòng nhập câu hỏi trước khi gửi.")
        if len(clean_message) > self.max_message_length:
            return self._error(
                f"Câu hỏi vượt quá {self.max_message_length:,} ký tự. "
                "Vui lòng rút gọn rồi thử lại."
            )

        try:
            content = run_base_model(clean_message, self._provider)
        except Exception as error:
            return self._error(f"Không thể kết nối mô hình: {error}")

        content = str(content).strip()
        return ChatResponse(
            content=content or "Mô hình không trả về nội dung.",
            backend=self.backend_name,
            provider=self.provider_name,
            model=self.model_name,
            tool_calls=0,
            is_error=not content or content.startswith(PROVIDER_ERROR_PREFIXES),
        )

    def status(self) -> dict[str, str | int]:
        """Expose non-sensitive runtime metadata for the UI."""
        return {
            "backend": self.backend_name,
            "provider": self.provider_name,
            "model": self.model_name,
            "tool_calls": 0,
        }

    def _error(self, message: str) -> ChatResponse:
        return ChatResponse(
            content=message,
            backend=self.backend_name,
            provider=self.provider_name,
            model=self.model_name,
            tool_calls=0,
            is_error=True,
        )


def create_chat_service() -> ChatService:
    """Factory kept separate so UI can cache one provider instance."""
    return ChatService()
