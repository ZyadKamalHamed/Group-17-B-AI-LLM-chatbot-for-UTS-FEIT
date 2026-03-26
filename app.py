import streamlit as st

st.set_page_config(
    page_title="UTS FEIT Chatbot",
    layout="centered"
)

with st.container(border=False, horizontal=True, vertical_alignment="center"):
    st.title("UTS FEIT Chatbot")
    # Add horizontal space between title and button
    st.space("small")
    if st.button("↻ Restart", type="primary"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

st.caption("Only return the input")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type here..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

response = f"Echo: {prompt}"

with st.chat_message("assistant"):
    st.markdown(response)

st.session_state.messages.append(
    {
        "role": "assistant",
        "content": response
    }
)