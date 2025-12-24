from cryptography.fernet import Fernet
from pathlib import Path

KEY_FILE = Path("chat_app/secret.key")

def get_fernet() -> Fernet:
    if not KEY_FILE.exists():
        key = Fernet.generate_key()
        KEY_FILE.write_bytes(key)
    else:
        key = KEY_FILE.read_bytes()

    return Fernet(key)
