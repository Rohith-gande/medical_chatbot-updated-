# from firebase_admin import firestore
# from datetime import datetime
# from .firebase_config import db

# def save_message(user_id, role, content):
#     chat_ref = db.collection("users").document(user_id).collection("chats").document("latest")
#     chat_ref.set({"last_updated": datetime.now()}, merge=True)
#     chat_ref.collection("messages").add({
#         "role": role,
#         "content": content,
#         "timestamp": datetime.now()
#     })

# def load_chat_history(user_id):
#     chat_ref = db.collection("users").document(user_id).collection("chats").document("latest").collection("messages")
#     chats = chat_ref.order_by("timestamp").stream()
#     return [{"role": chat.get("role"), "content": chat.get("content")} for chat in chats]


from firebase_admin import firestore
from datetime import datetime
from .firebase_config import db
 


def save_message(user_id, chat_id, role, content):
    chat_ref = (
        db.collection("users")
        .document(user_id)
        .collection("chats")
        .document(chat_id)
    )

    
    chat_ref.set({"last_updated": datetime.now()}, merge=True)

    
    chat_ref.collection("messages").add({
        "role": role,
        "content": content,
        "timestamp": datetime.now()
    })

    # ✅ Auto-generate chat title if it doesn’t exist and user sent the first message
    chat_doc = chat_ref.get()
    chat_data = chat_doc.to_dict() or {}

    if role == "user" and not chat_data.get("title"):
        auto_title = generate_chat_title(content)
        chat_ref.update({"title": auto_title})


# ---------------------------
# ✨ Generate Chat Title (like ChatGPT)
# ---------------------------
def generate_chat_title(user_message):
    """Create a short, descriptive chat title."""
    return user_message[:40] + ("..." if len(user_message) > 40 else "")


def load_chat_history(user_id, chat_id):
    chat_ref = (
        db.collection("users")
        .document(user_id)
        .collection("chats")
        .document(chat_id)
        .collection("messages")
    )
    chats = chat_ref.order_by("timestamp").stream()
    return [{"role": chat.get("role"), "content": chat.get("content")} for chat in chats]


# ---------------------------
# 🗂️ Load all chats for sidebar
# ---------------------------
def load_all_chats(user_id):
    chats_ref = (
        db.collection("users")
        .document(user_id)
        .collection("chats")
        .order_by("last_updated", direction=firestore.Query.DESCENDING)
        .stream()
    )

    chat_list = []
    for chat in chats_ref:
        data = chat.to_dict()
        chat_list.append({
            "id": chat.id,
            "title": data.get("title", "Untitled Chat"),
            "last_updated": data.get("last_updated", datetime.now()).strftime("%Y-%m-%d %H:%M"),
        })

    return chat_list


# ---------------------------
# ➕ Create a new chat session
# ---------------------------
def create_new_chat(user_id):
    chat_ref = db.collection("users").document(user_id).collection("chats").document()
    chat_ref.set({
        "title": "Untitled Chat",
        "last_updated": datetime.now()
    })
    return chat_ref.id
