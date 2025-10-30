import streamlit as st
from firebase_admin import auth
from firebase_admin._auth_utils import EmailAlreadyExistsError, UserNotFoundError

def signup_user(email, password):
    try:
        user = auth.create_user(email=email, password=password)
        return user.uid
    except EmailAlreadyExistsError:
        st.error("❌ User already exists.")
        return None
    except Exception as e:
        st.error(f"Error: {e}")
        return None

def login_user(email, password):
    # Firebase Admin SDK doesn’t support password login validation directly
    # We'll simulate it for frontend testing
    st.info("⚠️ Firebase Admin SDK doesn’t handle user login directly.")
    st.info("You can later replace this with Firebase Client SDK for actual login.")
    return email  # simulate user_id

def logout_user():
    st.session_state.clear()
    st.success("Logged out successfully ✅")
