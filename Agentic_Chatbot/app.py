import streamlit as st
from langchain_core.messages import HumanMessage

from agentic_part1 import workflow


st.set_page_config(
    page_title="LangGraph AI",
    page_icon="🤖",
    layout="centered"
)


st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 20%, rgba(59, 130, 246, 0.15), transparent 30%),
        radial-gradient(circle at 90% 80%, rgba(139, 92, 246, 0.15), transparent 30%),
        linear-gradient(135deg, #020617 0%, #0f172a 50%, #111827 100%);

    color: #f8fafc;
    min-height: 100vh;
}

.stApp::before {
    content: "";
    position: fixed;
    width: 400px;
    height: 400px;
    border-radius: 50%;
    background: rgba(59, 130, 246, 0.08);
    filter: blur(100px);
    top: 10%;
    left: -100px;
    animation: floatOne 8s ease-in-out infinite;
    pointer-events: none;
}

.stApp::after {
    content: "";
    position: fixed;
    width: 350px;
    height: 350px;
    border-radius: 50%;
    background: rgba(168, 85, 247, 0.08);
    filter: blur(100px);
    bottom: 5%;
    right: -100px;
    animation: floatTwo 10s ease-in-out infinite;
    pointer-events: none;
}

@keyframes floatOne {
    0%, 100% {
        transform: translate(0, 0);
    }

    50% {
        transform: translate(80px, 50px);
    }
}

@keyframes floatTwo {
    0%, 100% {
        transform: translate(0, 0);
    }

    50% {
        transform: translate(-70px, -60px);
    }
}

.block-container {
    max-width: 850px;
    padding-top: 2rem;
    padding-bottom: 7rem;
}

h1 {
    text-align: center;
    font-size: 42px !important;
    font-weight: 800 !important;
    margin-bottom: 5px !important;

    background: linear-gradient(
        90deg,
        #60a5fa,
        #a78bfa,
        #c084fc,
        #60a5fa
    );

    background-size: 300% 300%;

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    animation: gradientMove 5s ease infinite;
}

@keyframes gradientMove {
    0% {
        background-position: 0% 50%;
    }

    50% {
        background-position: 100% 50%;
    }

    100% {
        background-position: 0% 50%;
    }
}

.subtitle {
    text-align: center;
    color: #94a3b8;
    font-size: 15px;
    margin-bottom: 35px;
}

.status {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 8px;
    margin-bottom: 25px;
    color: #94a3b8;
    font-size: 13px;
}

.status-dot {
    width: 8px;
    height: 8px;
    background: #22c55e;
    border-radius: 50%;
    box-shadow: 0 0 12px #22c55e;
    animation: pulse 1.8s infinite;
}

@keyframes pulse {
    0% {
        box-shadow: 0 0 5px #22c55e;
    }

    50% {
        box-shadow: 0 0 18px #22c55e;
    }

    100% {
        box-shadow: 0 0 5px #22c55e;
    }
}

[data-testid="stChatMessage"] {
    border-radius: 20px;
    padding: 14px 18px;
    margin: 12px 0;

    border: 1px solid rgba(255,255,255,0.08);

    backdrop-filter: blur(15px);

    animation: messageAppear 0.45s ease-out;

    transition:
        transform 0.25s ease,
        box-shadow 0.25s ease;
}

[data-testid="stChatMessage"]:hover {
    transform: translateY(-2px);

    box-shadow:
        0 10px 30px rgba(0,0,0,0.25),
        0 0 20px rgba(96,165,250,0.08);
}

@keyframes messageAppear {
    from {
        opacity: 0;
        transform: translateY(15px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-user"]
) {
    background: linear-gradient(
        135deg,
        rgba(37,99,235,0.30),
        rgba(59,130,246,0.12)
    );

    border-color: rgba(96,165,250,0.25);
}

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) {
    background: linear-gradient(
        135deg,
        rgba(51,65,85,0.55),
        rgba(30,41,59,0.45)
    );

    border-color: rgba(148,163,184,0.15);
}

[data-testid="stChatMessageAvatarUser"] {
    background: linear-gradient(
        135deg,
        #2563eb,
        #7c3aed
    );
}

[data-testid="stChatMessageAvatarAssistant"] {
    background: linear-gradient(
        135deg,
        #7c3aed,
        #db2777
    );
}

[data-testid="stChatInput"] {
    border-radius: 18px;

    border: 1px solid rgba(148,163,184,0.25);

    background: rgba(15,23,42,0.75);

    backdrop-filter: blur(20px);

    box-shadow:
        0 10px 40px rgba(0,0,0,0.35),
        0 0 25px rgba(59,130,246,0.05);

    transition:
        border 0.3s ease,
        box-shadow 0.3s ease,
        transform 0.3s ease;
}

[data-testid="stChatInput"]:focus-within {
    border-color: rgba(96,165,250,0.7);

    box-shadow:
        0 10px 40px rgba(0,0,0,0.4),
        0 0 30px rgba(59,130,246,0.18);

    transform: translateY(-2px);
}

[data-testid="stChatInput"] textarea {
    color: #f8fafc !important;
    font-size: 15px;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #64748b;
}

[data-testid="stChatInput"] button {
    border-radius: 12px;
    transition: all 0.25s ease;
}

[data-testid="stChatInput"] button:hover {
    transform: scale(1.08);
}

::-webkit-scrollbar {
    width: 7px;
}

::-webkit-scrollbar-track {
    background: transparent;
}

::-webkit-scrollbar-thumb {
    background: #334155;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #64748b;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


st.markdown("""
<h1>🤖 LangGraph AI</h1>

<div class="subtitle">
    Intelligent conversations powered by LangGraph
</div>

<div class="status">
    <span class="status-dot"></span>
    AI is online
</div>
""", unsafe_allow_html=True)


if "thread_id" not in st.session_state:
    st.session_state.thread_id = "chat_1"


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])


user_input = st.chat_input("Ask me anything...")


if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    config = {
        "configurable": {
            "thread_id": st.session_state.thread_id
        }
    }

    with st.chat_message("assistant"):

        def stream_response():
            for message_chunk, metadata in workflow.stream(
                {
                    "messages": [
                        HumanMessage(content=user_input)
                    ]
                },
                config=config,
                stream_mode="messages"
            ):
                if message_chunk.content:
                    yield message_chunk.content

        ai_message = st.write_stream(stream_response())

    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_message
    })