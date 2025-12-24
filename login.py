from json import load
from pathlib import Path
from auth import verify_password

USER_FILE = Path("chat_app/users.json")

def login(username: str, password: str) -> bool | str:
    username = username.strip().lower()

    if not USER_FILE.exists():
        return "No users registered"

    users = load(USER_FILE.open())

    if username not in users:
        return "Invalid username or password"

    if verify_password(password, users[username]):
        return True

    return "Invalid username or password"
