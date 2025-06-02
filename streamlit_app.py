import streamlit as st
import requests

# Set page title and layout
st.set_page_config(page_title="Chatbot with Memory", layout="wide")
st.title("Chatbot with Contextual Memory")

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Input form
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Your message:", placeholder="Type your message here...")
    submit_button = st.form_submit_button("Send")

# Handle submission
if submit_button and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    try:
        # Send request to FastAPI backend
        response = requests.post("http://localhost:8000/chat", json={"user_input": user_input})
        response.raise_for_status()
        bot_response = response.json()["response"]
        st.session_state.messages.append({"role": "bot", "content": bot_response})
    except requests.RequestException as e:
        st.error(f"Error connecting to backend: {e}")

# Display conversation
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You**: {msg['content']}")
    else:
        st.markdown(f"**Bot**: {msg['content']}")

# Clear history button
if st.button("Clear Conversation"):
    st.session_state.messages = []
    try:
        requests.post("http://localhost:8000/clear-memory")
        st.success("Conversation history cleared!")
    except requests.RequestException as e:
        st.error(f"Error clearing memory: {e}")

# Run: streamlit run streamlit_app.py