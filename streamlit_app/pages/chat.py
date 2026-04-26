"""
Chat page for the Streamlit application.
"""
import streamlit as st
from utils.api_client import query_backend, document_upload_rag

# Configure page settings
st.set_page_config(
    page_title="LangGraph Chat",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get help": None,
        "Report a Bug": None,
        "About": None
    }
)

# Redirect to home if no session
if "session_id" not in st.session_state:
    st.warning("Please start a session first.")
    st.switch_page("home.py")
    st.stop()

# Initialize logout confirmation state
if "show_logout_confirm" not in st.session_state:
    st.session_state.show_logout_confirm = False

# Header with logout button
col1, col2 = st.columns([10, 2])
with col1:
    username = st.session_state.get("username", "user")
    st.markdown(f"### 💬 Welcome, **{username}**!")
with col2:
    st.write("")
    if st.button("🔒 Logout", use_container_width=True):
        st.session_state.show_logout_confirm = True

# Logout confirmation
if st.session_state.show_logout_confirm:
    st.warning("Are you sure you want to logout?")
    col_confirm, col_cancel = st.columns(2)
    with col_confirm:
        if st.button("✅ Yes, logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.switch_page("home.py")
    with col_cancel:
        if st.button("❌ Cancel"):
            st.session_state.show_logout_confirm = False

st.title("🤖 Adaptive RAG Assistant")

# Document upload section
with st.sidebar:
    st.header("📂 Upload Documents")
    st.markdown("Supported: **PDF, TXT, DOCX**")
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["pdf", "txt", "docx"]
    )

    if uploaded_file:
        file_description = st.text_input(
            "📄 Describe your document (required)",
            max_chars=300,
            placeholder="E.g. LangGraph tutorial with workflows and code examples"
        )

        if "uploaded_files" not in st.session_state:
            st.session_state.uploaded_files = {}

        file_key = f"{uploaded_file.name}_{file_description}"

        if file_description:
            if file_key not in st.session_state.uploaded_files:
                with st.spinner("Uploading and processing document..."):
                    success = document_upload_rag(uploaded_file, file_description)
                if success:
                    st.success(f"✅ Uploaded: {uploaded_file.name}")
                    st.session_state.uploaded_files[file_key] = True
                else:
                    st.error(f"❌ Upload failed: {uploaded_file.name}")
            else:
                st.info(f"✅ Already uploaded: {uploaded_file.name}")
        else:
            st.warning("Please describe your document before uploading.")

    st.divider()
    st.markdown(f"**Session ID:**")
    st.code(st.session_state["session_id"][:8] + "...", language=None)

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for role, text in st.session_state.chat_history:
    st.chat_message(role).write(text)

# User input — use session_id instead of jwt_token
user_input = st.chat_input("Ask a question about your document...")

if user_input:
    st.session_state.chat_history.append(("user", user_input))
    with st.spinner("Thinking..."):
        response = query_backend(user_input, st.session_state["session_id"])
    st.session_state.chat_history.append(("assistant", response))
    st.rerun()
