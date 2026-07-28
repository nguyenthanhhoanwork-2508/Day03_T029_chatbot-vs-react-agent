"""
Streamlit UI cho VeS.

File này chỉ chịu trách nhiệm hiển thị và gọi contract ``ChatService.chat``.
Không import hoặc thay đổi provider, prompt, tool hay backend.
"""

from __future__ import annotations

import os
import sys
from html import escape

import streamlit as st

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import ChatService, create_chat_service


st.set_page_config(
    page_title="VeS · Tư vấn chọn ngành",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed",
)


st.markdown(
    """
    <style>
        :root {
            --ves-primary: #2563EB;
            --ves-primary-hover: #1D4ED8;
            --ves-title: #0F172A;
            --ves-body: #334155;
            --ves-muted: #64748B;
            --ves-border: #D9E8FF;
            --ves-border-soft: #E8F1FF;
            --ves-user: #E7F0FF;
            --ves-surface: rgba(255, 255, 255, 0.96);
            --ves-shadow: 0 14px 42px rgba(37, 99, 235, 0.08);
        }

        html,
        body,
        [data-testid="stAppViewContainer"],
        .stApp {
            min-height: 100%;
            background:
                linear-gradient(135deg, #ffffff 0%, #f4f8ff 50%, #eaf4ff 100%);
            color: var(--ves-body);
        }

        [data-testid="stHeader"],
        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        [data-testid="stSidebar"],
        #MainMenu,
        footer {
            display: none !important;
        }

        [data-testid="stAppViewBlockContainer"],
        [data-testid="stMainBlockContainer"] {
            width: min(100%, 960px);
            max-width: 960px;
            padding: 1.15rem 1.25rem 2rem;
        }

        [data-testid="stBottom"],
        [data-testid="stBottomBlockContainer"] {
            position: static !important;
            width: 100% !important;
            padding: 0 !important;
            background: transparent !important;
            box-shadow: none !important;
        }

        .st-key-topbar {
            position: sticky;
            z-index: 100;
            top: 0;
            margin-bottom: 0.4rem;
            padding: 0.65rem 0;
            background: rgba(248, 251, 255, 0.86);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
        }

        .ves-brand {
            display: inline-flex;
            align-items: center;
            gap: 0.75rem;
            min-height: 3rem;
            color: var(--ves-title);
            text-decoration: none;
        }

        .ves-brand-mark {
            display: grid;
            width: 46px;
            height: 46px;
            place-items: center;
            flex: 0 0 46px;
            border: 1px solid #C8DCFF;
            border-radius: 14px;
            background: #FFFFFF;
            box-shadow: 0 8px 24px rgba(37, 99, 235, 0.10);
            font-size: 1.35rem;
        }

        .ves-brand-copy {
            display: flex;
            flex-direction: column;
            justify-content: center;
            gap: 0.05rem;
        }

        .ves-wordmark {
            color: var(--ves-title);
            font-size: 1.8rem;
            font-weight: 800;
            letter-spacing: -0.055em;
            line-height: 1;
        }

        .ves-wordmark .ves-s {
            color: var(--ves-primary);
        }

        .ves-brand-subtitle {
            color: var(--ves-muted);
            font-size: 0.76rem;
            font-weight: 500;
            line-height: 1.3;
        }

        .st-key-new_chat {
            display: flex;
            justify-content: flex-end;
        }

        .st-key-new_chat button {
            min-height: 2.35rem;
            padding: 0.45rem 0.8rem;
            border: 1px solid var(--ves-border);
            border-radius: 12px;
            background: rgba(255, 255, 255, 0.82);
            color: var(--ves-primary);
            box-shadow: none;
            font-size: 0.82rem;
            font-weight: 650;
            white-space: nowrap;
        }

        .st-key-new_chat button:hover {
            border-color: #AFCBFF;
            background: #FFFFFF;
            color: var(--ves-primary-hover);
            box-shadow: 0 8px 22px rgba(37, 99, 235, 0.08);
        }

        .st-key-empty_stage {
            padding-top: clamp(3.5rem, 10vh, 7.5rem);
            text-align: left;
        }

        .ves-hero {
            width: 100%;
            max-width: 800px;
            margin: 0 auto;
        }

        .ves-hero h1 {
            margin: 0;
            color: var(--ves-title);
            font-size: clamp(2.2rem, 6vw, 3.7rem);
            font-weight: 820;
            letter-spacing: -0.058em;
            line-height: 1.06;
        }

        .ves-hero p {
            width: 100%;
            max-width: 800px;
            margin: 30px 0 0;
            color: var(--ves-muted);
            font-size: clamp(0.98rem, 2vw, 1.08rem);
            line-height: 1.65;
        }

        .st-key-empty_composer {
            width: 100%;
            max-width: 800px;
            margin: 30px auto 0;
            padding: 0;
            border: 0;
            background: transparent;
            box-shadow: none;
        }

        .st-key-empty_composer [data-testid="stChatInput"],
        .st-key-chat_composer [data-testid="stChatInput"] {
            overflow: hidden;
            border: 1px solid #D8E6FF !important;
            border-radius: 18px;
            background: #FFFFFF !important;
            box-shadow: 0 10px 30px rgba(37, 99, 235, 0.10) !important;
            transition:
                border-color 150ms ease,
                box-shadow 150ms ease;
        }

        .st-key-empty_composer [data-testid="stChatInput"]:focus-within,
        .st-key-chat_composer [data-testid="stChatInput"]:focus-within {
            border-color: #2563EB !important;
            box-shadow: 0 10px 30px rgba(37, 99, 235, 0.14) !important;
        }

        .st-key-empty_composer [data-testid="stChatInput"] > div,
        .st-key-chat_composer [data-testid="stChatInput"] > div,
        .st-key-empty_composer [data-baseweb="textarea"],
        .st-key-chat_composer [data-baseweb="textarea"],
        .st-key-empty_composer [data-baseweb="base-input"],
        .st-key-chat_composer [data-baseweb="base-input"],
        .st-key-empty_composer textarea,
        .st-key-chat_composer textarea {
            border: 0 !important;
            background: #FFFFFF !important;
            box-shadow: none !important;
        }

        .st-key-empty_composer textarea,
        .st-key-chat_composer textarea {
            color: var(--ves-title);
            font-size: 0.96rem;
        }

        .st-key-empty_composer textarea::placeholder,
        .st-key-chat_composer textarea::placeholder {
            color: #94A3B8;
        }

        .st-key-empty_composer [data-testid="stChatInputSubmitButton"],
        .st-key-chat_composer [data-testid="stChatInputSubmitButton"] {
            width: 40px;
            height: 40px;
            margin-right: 0.35rem;
            border: 0 !important;
            border-radius: 12px !important;
            background: #2563EB !important;
            color: #FFFFFF !important;
        }

        .st-key-empty_composer [data-testid="stChatInputSubmitButton"]:hover,
        .st-key-chat_composer [data-testid="stChatInputSubmitButton"]:hover {
            background: #1D4ED8 !important;
        }

        .st-key-empty_composer [data-testid="stChatInputSubmitButton"] svg,
        .st-key-chat_composer [data-testid="stChatInputSubmitButton"] svg {
            fill: #FFFFFF !important;
            color: #FFFFFF !important;
            stroke: #FFFFFF !important;
        }

        .st-key-empty_composer [data-testid="stChatInputSubmitButton"]:disabled,
        .st-key-chat_composer [data-testid="stChatInputSubmitButton"]:disabled {
            background: #93B4F8 !important;
            opacity: 0.72;
        }

        .st-key-chat_page {
            display: flex;
            min-height: calc(100vh - 110px);
            flex-direction: column;
        }

        .st-key-chat_thread {
            width: min(100%, 920px);
            min-height: 52vh;
            flex: 1;
            margin: 0 auto;
            padding: 2rem 0 150px;
        }

        .ves-user-message {
            display: flex;
            width: 100%;
            justify-content: flex-end;
            margin: 0 0 16px;
        }

        .ves-user-bubble {
            width: max-content;
            max-width: min(78%, 680px);
            padding: 0.85rem 1rem;
            border-radius: 20px 20px 7px 20px;
            background: #2563EB;
            color: #FFFFFF;
            box-shadow: 0 8px 24px rgba(37, 99, 235, 0.14);
            font-size: 0.95rem;
            line-height: 1.6;
            overflow-wrap: anywhere;
            white-space: pre-wrap;
        }

        .ves-assistant-message {
            display: flex;
            width: 100%;
            align-items: flex-start;
            justify-content: flex-start;
            gap: 0.7rem;
            margin: 0 0 16px;
        }

        .ves-assistant-avatar {
            display: grid;
            width: 42px;
            height: 42px;
            flex: 0 0 42px;
            place-items: center;
            border: 1px solid #C8DCFF;
            border-radius: 13px;
            background: #EEF5FF;
            color: #2563EB;
            font-size: 0.76rem;
            font-weight: 800;
            letter-spacing: -0.03em;
        }

        .ves-assistant-bubble {
            width: max-content;
            max-width: min(82%, 700px);
            padding: 0.85rem 1rem;
            border: 1px solid #D8E6FF;
            border-radius: 20px 20px 20px 7px;
            background: #FFFFFF;
            color: var(--ves-body);
            box-shadow: 0 8px 28px rgba(37, 99, 235, 0.055);
            font-size: 0.95rem;
            line-height: 1.65;
            overflow-wrap: anywhere;
            white-space: pre-wrap;
        }

        .st-key-chat_composer {
            position: fixed !important;
            z-index: 1000;
            right: unset;
            bottom: 16px;
            left: 50%;
            width: min(920px, calc(100vw - 32px));
            max-width: 920px;
            margin: 0;
            padding: 0.625rem;
            border: 0;
            border-radius: 22px;
            background: rgba(245, 249, 255, 0.94);
            box-shadow: 0 14px 38px rgba(37, 99, 235, 0.12);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            transform: translateX(-50%);
        }

        .st-key-chat_composer [data-testid="stHorizontalBlock"] {
            display: grid !important;
            width: 100% !important;
            grid-template-columns: minmax(0, 1fr) 40px !important;
            align-items: center !important;
            gap: 8px !important;
        }

        .st-key-chat_composer [data-testid="stColumn"] {
            width: 100% !important;
            min-width: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        .st-key-clear_chat_icon,
        .st-key-clear_chat_icon [data-testid="stButton"] {
            width: 40px !important;
            height: 40px !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        .st-key-clear_chat_icon button {
            display: grid !important;
            width: 40px !important;
            min-width: 40px !important;
            max-width: 40px !important;
            height: 40px !important;
            min-height: 40px !important;
            max-height: 40px !important;
            place-items: center !important;
            margin: 0 !important;
            padding: 0 !important;
            border: 1px solid #D8E6FF !important;
            border-radius: 12px !important;
            background: #FFFFFF !important;
            color: #2563EB !important;
            box-shadow: none !important;
            font-size: 1rem !important;
        }

        .st-key-clear_chat_icon button:hover {
            border-color: #BFD4FF !important;
            background: #EEF5FF !important;
            color: #1D4ED8 !important;
        }

        [data-testid="stAlert"] {
            border-radius: 14px;
        }

        @media (max-width: 720px) {
            [data-testid="stAppViewBlockContainer"],
            [data-testid="stMainBlockContainer"] {
                padding: 0.75rem 0.75rem 1.2rem;
            }

            .ves-brand-mark {
                width: 44px;
                height: 44px;
                flex-basis: 44px;
            }

            .ves-wordmark {
                font-size: 1.65rem;
            }

            .ves-brand-subtitle {
                max-width: 13rem;
                overflow: hidden;
                font-size: 0.7rem;
                text-overflow: ellipsis;
                white-space: nowrap;
            }

            .st-key-empty_stage {
                padding-top: 2.8rem;
            }

            .ves-hero h1 {
                font-size: clamp(2rem, 11vw, 2.75rem);
            }

            .ves-hero p {
                font-size: 0.94rem;
            }

            .ves-user-bubble {
                max-width: 88%;
            }

            .ves-assistant-bubble {
                max-width: calc(100% - 54px);
            }

            .st-key-chat_composer {
                bottom: 10px;
                width: calc(100vw - 20px);
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def get_chat_service() -> ChatService:
    """Create one backend connection for the current Streamlit process."""
    return create_chat_service()


def initialize_session() -> None:
    """Preserve the existing UI session-state contract."""
    if "messages" not in st.session_state:
        st.session_state.messages = []


def clear_conversation() -> None:
    """Clear only the existing message list."""
    st.session_state.messages = []
    st.rerun()


def render_brand(compact: bool) -> None:
    """Render enlarged VeS logo with its supporting line."""
    st.markdown(
        """
        <div class="ves-brand">
            <span class="ves-brand-mark">🎓</span>
            <span class="ves-brand-copy">
                <span class="ves-wordmark">Ve<span class="ves-s">S</span></span>
                <span class="ves-brand-subtitle">
                    Tư vấn chọn ngành và nguyện vọng
                </span>
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_topbar(is_empty_chat: bool) -> None:
    """Render logo left and compact new-conversation action right."""
    with st.container(key="topbar"):
        brand_column, action_column = st.columns([7.5, 2.5], vertical_alignment="center")
        with brand_column:
            render_brand(compact=not is_empty_chat)
        with action_column:
            if st.button(
                "Cuộc trò chuyện mới",
                key="new_chat",
                use_container_width=True,
            ):
                clear_conversation()


def render_empty_hero() -> None:
    """Render centered first-use content."""
    with st.container(key="empty_stage"):
        st.markdown(
            """
            <section class="ves-hero">
                <h1>Hiểu mình rõ hơn.<br>Chọn ngành phù hợp hơn.</h1>
                <p>
                    Chia sẻ điểm thi, sở thích và nơi bạn muốn học. VeS sẽ giúp
                    bạn khám phá nhóm ngành phù hợp, tham khảo trường và sắp xếp
                    nguyện vọng dễ hiểu hơn.
                </p>
            </section>
            """,
            unsafe_allow_html=True,
        )


def render_empty_composer(service: ChatService) -> str | None:
    """Render the centered first-message input."""
    with st.container(key="empty_composer"):
        return st.chat_input(
            "Nhập điểm thi, sở thích hoặc câu hỏi của bạn...",
            max_chars=service.max_message_length,
            key="hero_chat_input",
        )


def render_history() -> None:
    """Render existing messages without changing their stored structure."""
    with st.container(key="chat_thread"):
        for message in st.session_state.messages:
            safe_content = escape(str(message.get("content", "")), quote=True)
            if message["role"] == "user":
                st.markdown(
                    f"""
                    <div class="ves-user-message" aria-label="Tin nhắn người dùng">
                        <div class="ves-user-bubble">{safe_content}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                    <div class="ves-assistant-message" aria-label="Tin nhắn VeS">
                        <div class="ves-assistant-avatar" aria-hidden="true">VeS</div>
                        <div class="ves-assistant-bubble">{safe_content}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


def render_chat_composer(service: ChatService) -> str | None:
    """Render fixed input and a same-size clear action below the active thread."""
    with st.container(key="chat_composer"):
        input_column, clear_column = st.columns(
            [1, 0.06],
            gap="small",
            vertical_alignment="center",
        )
        with input_column:
            prompt = st.chat_input(
                "Nhập điểm thi, sở thích hoặc câu hỏi của bạn...",
                max_chars=service.max_message_length,
                key="fixed_chat_input",
            )
        with clear_column:
            if st.button(
                "🗑️",
                key="clear_chat_icon",
                help="Cuộc trò chuyện mới",
            ):
                clear_conversation()
        return prompt


def submit_message(service: ChatService, prompt: str) -> None:
    """Call the unchanged backend and append to the existing message list."""
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = service.chat(prompt)
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response.content,
            "model": response.model,
            "is_error": response.is_error,
        }
    )
    st.rerun()


def run_app() -> None:
    """Switch between empty and active-chat UI without changing backend logic."""
    initialize_session()
    service = get_chat_service()
    is_empty_chat = len(st.session_state.get("messages", [])) == 0

    render_topbar(is_empty_chat)

    if is_empty_chat:
        render_empty_hero()
        prompt = render_empty_composer(service)
    else:
        with st.container(key="chat_page"):
            render_history()
            prompt = render_chat_composer(service)

    if prompt:
        submit_message(service, prompt)


if __name__ == "__main__":
    run_app()
