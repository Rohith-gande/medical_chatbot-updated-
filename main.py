import streamlit as st
from datetime import datetime
from app import initialize_chains
from src.auth import signup_user, login_user, logout_user
from src.chat_history import (
    save_message,
    load_chat_history,
)
from src.sidebar import render_sidebar

# Initialize RAG + Rewrite chains once
rag_chain, rewrite_chain = initialize_chains()

# Streamlit page setup
st.set_page_config(page_title="Medical Chatbot", layout="wide")

# Session state setup
if "user" not in st.session_state:
    st.session_state.user = None
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None


# ---------------- AUTH SECTION ----------------
def show_login_signup():
    st.title("Medical Chatbot Login")

    tab1, tab2 = st.tabs(["🔐 Login", "🆕 Sign Up"])

    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            user = login_user(email, password)
            if user:
                st.session_state.user = user
                st.success(f"Welcome back, {email}!")
                st.rerun()

    with tab2:
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_password")
        if st.button("Sign Up"):
            uid = signup_user(email, password)
            if uid:
                st.session_state.user = uid
                st.success("Account created successfully!")
                st.rerun()


# ---------------- CHAT SECTION ----------------
def show_chat_ui():
    render_sidebar(st.session_state.user)

    # Main Chat UI
    st.title("🩺 Medical Chatbot")
    st.caption("Ask any medical-related question. (Gemini + Pinecone)")

    if not st.session_state.current_chat_id:
        st.info("🆕 Start a new chat to begin.")
        return

    # Load chat history
    messages = load_chat_history(st.session_state.user, st.session_state.current_chat_id)
    for chat in messages:
        with st.chat_message(chat["role"]):
            st.write(chat["content"])

    # Input for new message
    user_query = st.chat_input("Ask your question about medicine...")
    if user_query:
        # Show user message
        with st.chat_message("user"):
            st.write(user_query)
        save_message(st.session_state.user, st.session_state.current_chat_id, "user", user_query)

        with st.spinner("Rewriting your query for better search..."):
            rewritten_query = rewrite_chain.run(query=user_query).strip()

        with st.chat_message("assistant"):
            st.info(f"🔁 **Rewritten Query:** {rewritten_query}")
            response = rag_chain.invoke({"input": rewritten_query})
            answer = response["answer"]
            st.write(answer)

        # Save assistant message
        save_message(st.session_state.user, st.session_state.current_chat_id, "assistant", answer)


# ---------------- MAIN APP FLOW ----------------
def main():
    if not st.session_state.user:
        show_login_signup()
    else:
        show_chat_ui()


if __name__ == "__main__":
    main()
