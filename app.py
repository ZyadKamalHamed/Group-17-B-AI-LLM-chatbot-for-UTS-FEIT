import streamlit as st
import requests

st.set_page_config(
    page_title="UTS FEIT Chatbot",
    layout="centered",
    initial_sidebar_state="collapsed",
    page_icon="UTS_Assets/images.png"
)

st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);
    }
    .uts-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 2rem;
        justify-content: space-between;
    }
    .uts-header img {
        height: 70px;
        width: auto;
    }
    .uts-title {
        color: #0052CC;
        font-weight: 700;
        font-size: 2.2rem;
        margin: 0;
        padding: 0;
    }
    .stButton>button {
        background-color: #0052CC;
        color: white;
        border-radius: 0.5rem;
        font-weight: 600;
        padding: 0.5rem 1.5rem;
    }
    .stButton>button:hover {
        background-color: #003d99;
    }
    /* Style chat message avatars */
    [data-testid="chatAvatarIcon-user"] {
        background-color: #0052CC !important;
    }
    [data-testid="chatAvatarIcon-assistant"] {
        background-color: #0052CC !important;
    }
    .stChatMessage [data-testid="chatAvatarIcon"] svg {
        filter: invert(1);
    }
    /* Source card styling */
    .source-card {
        background: linear-gradient(135deg, #E8F0FF 0%, #F0F5FF 100%);
        border-left: 4px solid #0052CC;
        padding: 0.75rem 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        word-break: break-word;
    }
    .source-icon {
        font-size: 1.2rem;
        flex-shrink: 0;
    }
    .source-link {
        color: #0052CC;
        text-decoration: none;
        font-weight: 500;
        word-break: break-all;
    }
    .source-link:hover {
        text-decoration: underline;
    }
    .example-questions {
        display: grid;
        gap: 0.75rem;
        margin-top: 2rem;
    }
    .example-btn {
        background: linear-gradient(135deg, #E8F0FF 0%, #F0F5FF 100%);
        border: 1px solid #0052CC;
        padding: 1rem;
        border-radius: 0.5rem;
        cursor: pointer;
        text-align: left;
        color: #0052CC;
        font-weight: 500;
        transition: all 0.2s;
    }
    .example-btn:hover {
        background: linear-gradient(135deg, #0052CC 0%, #003d99 100%);
        color: white;
        border-color: #003d99;
    }
    @keyframes swing {
        0%, 100% { transform: rotate(-20deg); transform-origin: top center; }
        50% { transform: rotate(20deg); transform-origin: top center; }
    }
</style>
""", unsafe_allow_html=True)

col_logo, col_title, col_restart = st.columns([0.12, 0.7, 0.18])
with col_logo:
    st.image("UTS_Assets/images (1).png", width=70)
with col_title:
    st.markdown('<div class="uts-title">UTS FEIT Chatbot</div>', unsafe_allow_html=True)
with col_restart:
    if st.button("↻ Restart", type="primary", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

st.divider()

# Initialise chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    avatar = "📚" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"], unsafe_allow_html=True)

# Show example questions if chat is empty
if not st.session_state.messages:
    st.markdown("### Example Questions")
    col1, col2 = st.columns(2)

    example_questions = [
        "How do I enrol in subjects?",
        "What's the census date?",
        "How do I get special consideration?",
        "Where can I get food on campus?"
    ]

    for i, q in enumerate(example_questions):
        col = col1 if i % 2 == 0 else col2
        with col:
            if st.button(q, key=f"example_{i}", use_container_width=True, help="Click to ask this question"):
                st.session_state.ask_example = q
                st.rerun()

    st.markdown("---")

# Handle example question or user input
if "ask_example" in st.session_state:
    prompt = st.session_state.ask_example
    del st.session_state.ask_example
else:
    prompt = st.chat_input("e.g., How do I get special consideration?")

if prompt:
    # Show user message
    st.chat_message("user", avatar="👤").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display loading state with animated anchor
    with st.chat_message("assistant", avatar="📚"):
        with st.spinner("⚓ Diving into our UTS sources..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/chat",
                    json={"question": prompt}
                ).json()

                answer = response.get("answer", "No answer returned.")
                sources = response.get("sources", [])

                # Build assistant message with styled sources
                formatted_answer = answer
                if sources:
                    formatted_answer += "\n\n**Sources:**"
                    for i, url in enumerate(sources, 1):
                        # Create a styled source card
                        formatted_answer += f'\n<div class="source-card"><span class="source-icon">📎</span><a href="{url}" target="_blank" class="source-link">{url}</a></div>'

            except Exception as e:
                formatted_answer = f"Error contacting backend: {e}"

        # Display assistant message
        st.markdown(formatted_answer, unsafe_allow_html=True)

    st.session_state.messages.append(
        {"role": "assistant", "content": formatted_answer}
    )
