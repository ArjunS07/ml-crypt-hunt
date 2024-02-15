import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Used for the generate_passphrase function in functions.py
WORD_LIST: list[str] = (
    open(f"{BASE_DIR}/utils/clean_words.txt", "r").read().splitlines()
)
VALID_USERNAMES_LIST = (
    open(f"{BASE_DIR}/utils/school_user_ids.txt", "r").read().splitlines()
)

# Used for the generate_teams function in functions.py
HOUSE_NAMES: list[str] = ["Srishti", "Vasundhara", "Sagar", "Himgiri"]
HOUSE_COLORS: list[str] = ["green", "red", "blue", "yellow"]

# Use this to print stuff from the admin panel
WHATSAPP_MESSAGES: dict[str, str] = {
    "share_password_message": "The password for {{HOUSE_NAME}} house is {{HOUSE_PASSWORD}}.",
}

OFFLINE_POINTS_PER_QUESTION = 2
ONLINE_POINTS_PER_QUESTION = 1
