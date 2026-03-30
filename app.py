import streamlit as st
import requests

st.set_page_config(
    page_title="UTS FEIT Chatbot",
    layout="centered"
)

with st.container(border=False, horizontal=True, vertical_alignment="center"):
    st.title("UTS FEIT Chatbot")
    st.space("small")
    if st.button("↻ Restart", type="primary"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

st.caption("Ask any question about UTS FEIT. The chatbot will search the web and summarise the results.")

# Initialise chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle new user input
if prompt := st.chat_input("Type here..."):
    # Show user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Send to backend
    try:
        response = requests.post(
            "http://127.0.0.1:8000/chat",
            json={"question": prompt}
        ).json()

        answer = response.get("answer", "No answer returned.")
        sources = response.get("sources", [])

        # Build assistant message with sources
        formatted_answer = answer
        if sources:
            formatted_answer += "\n\n**Sources:**\n"
            for url in sources:
                formatted_answer += f"- {url}\n"

    except Exception as e:
        formatted_answer = f"Error contacting backend: {e}"

    # Display assistant message
    with st.chat_message("assistant"):
        st.markdown(formatted_answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": formatted_answer}
    )
