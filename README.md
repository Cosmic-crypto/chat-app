# 🔐 Secure Encrypted Chat App (Streamlit)

This project is a **secure chat application built with Streamlit** that stores all messages **encrypted by default** using **Fernet (AES + HMAC)** from the `cryptography` library.

Messages are:
- 🔒 Encrypted at rest
- 👀 Displayed encrypted by default
- 🔓 Only decrypted when the user explicitly chooses
- 🗑 Soft-deleted (marked as deleted, not removed)

---

## 📁 Project Structure

chat_app/
│
├── chat_app.py # Main Streamlit app (chat UI + logic)
├── funcs.py # Encryption utilities (Fernet key handling)
├── login.py # User login logic
├── signup.py # User signup logic
├── messages.json # Encrypted message storage (auto-created)
├── users.json # User credential storage (auto-created)
├── secret.key # Fernet encryption key (auto-created, DO NOT SHARE)

yaml
Copy code

---

## 🧠 How It Works

### 🔑 Encryption
- Uses **Fernet symmetric encryption**
- A single key is generated once and stored in `secret.key`
- The same key is reused to encrypt/decrypt messages

### 💬 Messages
- Messages are encrypted before being written to disk
- Stored in this format:

```json
{
  "username": [
    "gAAAAABp....",
    "gAAAAABp....__DELETED__"
  ]
}
Messages are never stored in plaintext

Deleted messages are soft-deleted using a marker

🗑 Soft Delete
Instead of removing messages, deleted messages are marked:

markdown
Copy code
__DELETED__
This preserves:

Message order

Audit history

Data integrity

📄 File Breakdown
chat_app.py
The main Streamlit application.

Responsibilities:

User login/signup flow

Sending encrypted messages

Displaying encrypted messages

On-demand decryption

Soft deletion of messages

Session handling

funcs.py
Encryption utilities.

Responsibilities:

Generate Fernet key (only once)

Load and reuse the same key

Return a valid Fernet instance

This file ensures:

Keys are not regenerated

Encryption remains consistent

Fernet errors are avoided

login.py
Handles user authentication.

Responsibilities:

Verify username/password

Compare hashed passwords

Prevent invalid logins

signup.py
Handles account creation.

Responsibilities:

Create new users

Hash passwords securely

Prevent duplicate usernames

secret.key
Contains the Fernet encryption key

Auto-generated on first run

DO NOT DELETE (or messages become undecryptable)

DO NOT COMMIT to version control

Add this to .gitignore.

messages.json
Stores encrypted messages

Auto-created when the first message is sent

Never contains plaintext

🚀 Running the App
1️⃣ Install dependencies
bash
Copy code
pip install streamlit cryptography
2️⃣ Run the app
bash
Copy code
streamlit run chat_app.py
🔐 Security Notes (Important)
Never modify encrypted strings

Never strip or edit Fernet tokens

gAAAAAB... is a normal Fernet prefix

Decryption only works with the original, unmodified token

Deleting secret.key will permanently break decryption

✅ Features Summary
✔ Encrypted message storage

✔ Explicit user-controlled decryption

✔ Soft delete with deletion markers

✔ Fernet key reuse

✔ Streamlit-based UI

✔ No plaintext persistence

📌 Possible Future Improvements
Per-message permissions

Password re-entry before decrypt

Message timestamps

SQLite instead of JSON

Per-user encryption keys

🧠 Key Takeaway
This app follows a real-world security model:

Encrypted by default, decrypted only by explicit user action, and never stored in plaintext.
