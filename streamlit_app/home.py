"""
Home page for Streamlit authentication interface.
Simplified version - bypasses Rust auth service.
"""
import uuid
import streamlit as st

# Hide sidebar nav
hide_sidebar_style = """
    <style>
        [data-testid="stSidebarNav"] { display: none; }
    </style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)

st.set_page_config(page_title="LangGraph Chat")

st.title("🤖 Welcome to Adaptive RAG Assistant")
st.markdown("An AI-powered chatbot that answers questions from your uploaded documents.")
st.divider()

# Generate a unique session ID automatically
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())

if "username" not in st.session_state:
    st.session_state["username"] = "user"

# Simple name entry to personalize the experience
with st.form("start_form"):
    name = st.text_input("Your Name (optional)", placeholder="e.g. Parth")
    submit = st.form_submit_button("Start Chatting →")

if submit:
    if name.strip():
        st.session_state["username"] = name.strip()
    st.switch_page("pages/Chat.py")
