from json import load, dump
from pathlib import Path
from auth import hash_password

USER_FILE = Path("chat_app/users.json")

def sign_up(username: str, password: str) -> bool | str:
    username = username.strip().lower()

    if USER_FILE.exists():
        users = load(USER_FILE.open())
    else:
        users = {}

    if username in users:
        return "Username already exists"

    users[username] = hash_password(password)

    with USER_FILE.open("w") as f:
        dump(users, f, indent=2)

    return True
