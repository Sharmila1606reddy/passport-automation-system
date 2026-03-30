import json
import os

DB_PATH = "data/users.json"

def load_users():
    if not os.path.exists(DB_PATH):
        return []

    try:
        with open(DB_PATH, "r") as f:
            return json.load(f)
    except:
        return []

def save_user(user):
    users = load_users()
    users.append(user)

    with open(DB_PATH, "w") as f:
        json.dump(users, f, indent=4)