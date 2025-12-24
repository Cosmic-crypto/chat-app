import streamlit as st
from pathlib import Path
from json import load, dump
from funcs import get_fernet
from login import login
from signup import sign_up

# -------------------- Constants --------------------

MSG_FILE = Path("chat_app/messages.json")
DELETED_MARKER = "__DELETED__"

fernet = get_fernet()

st.title("💬 Secure Chat App")

# -------------------- Session State --------------------

if "user" not in st.session_state:
    st.session_state.user = None

# -------------------- Auth --------------------

if st.session_state.user is None:
    mode = st.radio("Choose mode", ["Login", "Sign up"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if mode == "Sign up":
        password2 = st.text_input("Repeat password", type="password")

        if st.button("Create account"):
            if not username or not password:
                st.error("All fields required")
            elif password != password2:
                st.error("Passwords do not match")
            else:
                result = sign_up(username, password)
                if result is True:
                    st.success("Account created. You can now log in.")
                else:
                    st.error(result)

    else:  # Login
        if st.button("Login"):
            result = login(username, password)
            if result is True:
                st.session_state.user = username.strip().lower()
                st.rerun()
            else:
                st.error(result)

    st.stop()

# -------------------- Message Storage --------------------

def load_messages() -> dict:
    if MSG_FILE.exists():
        with MSG_FILE.open() as f:
            return load(f)
    return {}

def save_messages(messages: dict):
    with MSG_FILE.open("w") as f:
        dump(messages, f, indent=2)

messages = load_messages()

# -------------------- Chat Input --------------------

st.success(f"Logged in as **{st.session_state.user}**")

user_input = st.chat_input("Type a message (encrypted)")

if user_input:
    encrypted = fernet.encrypt(user_input.encode()).decode()
    messages.setdefault(st.session_state.user, []).append(encrypted)
    save_messages(messages)
    st.rerun()

# -------------------- Display Messages --------------------

st.subheader("🔒 Encrypted Messages")

if not messages:
    st.info("No messages yet")
else:
    for user, user_messages in messages.items():
        for i, encrypted in enumerate(user_messages):
            with st.chat_message(user):

                # If message was deleted
                if encrypted.endswith(DELETED_MARKER):
                    st.error("🗑 Message deleted")
                    continue

                # Show encrypted content only
                st.code(encrypted.removeprefix("gAAAAAB"), language="text")

                col1, col2 = st.columns(2)

                # Decrypt (explicit)
                if col1.button("Decrypt", key=f"decrypt_{user}_{i}"):
                    decrypted = fernet.decrypt(
                        encrypted.encode()
                    ).decode()
                    st.success(decrypted)

                # Soft delete
                if col2.button("Delete", key=f"delete_{user}_{i}"):
                    messages[user][i] = encrypted + DELETED_MARKER
                    save_messages(messages)
                    st.rerun()