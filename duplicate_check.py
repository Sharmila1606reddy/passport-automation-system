from database import load_users
from Levenshtein import ratio

def check_duplicate(name, dob, id_number):
    users = load_users()

    for user in users:
        if user["id"] == id_number:
            return "EXACT_DUPLICATE"

        similarity = ratio(name.lower(), user["name"].lower())
        if similarity > 0.6 and dob == user["dob"]:
            return "POSSIBLE_DUPLICATE"

    return "NEW"