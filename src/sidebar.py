import streamlit as st
from src.chat_history import load_all_chats, create_new_chat, load_chat_history
from src.auth import logout_user

def render_sidebar(user_email):
    st.sidebar.title("💬 Your Chats")

    # ➕ New Chat button
    if st.sidebar.button("➕ New Chat"):
        new_chat_id = create_new_chat(user_email)
        st.session_state.messages = []
        st.session_state.current_chat_id = new_chat_id
        st.success("🆕 Started a new chat!")
        st.rerun()

    # 📜 Load all previous chats
    chats = load_all_chats(user_email)

    if chats:
        for chat in chats:
            # Each chat shows its title and timestamp
            chat_label = f"{chat['title']}*"
            if st.sidebar.button(chat_label, key=chat["id"]):
                st.session_state.current_chat_id = chat["id"]
                st.session_state.messages = load_chat_history(user_email, chat["id"])
                st.rerun()
    else:
        st.sidebar.info("No previous chats found. Start a new one!")

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"👋 Logged in as **{user_email}**")

    # 🚪 Logout button
    if st.sidebar.button("Logout"):
        logout_user()
        st.session_state.clear()
        st.rerun()
