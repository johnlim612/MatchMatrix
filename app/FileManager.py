import json, pytz, sys, os
from config import DATA_FOLDER
from datetime import datetime

sys.executable

player_data_path = os.path.join(DATA_FOLDER, "PlayerData.json")
last_updated_path = os.path.join(DATA_FOLDER, "LastUpdated.txt")


def open_player_data():
    print(f"Full path to PlayerData.json: {player_data_path}")
    with open(player_data_path, "r") as f:
        try:
            data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error: File not found or invalid JSON.")
        return data


def open_last_submitted_data():
    with open(last_updated_path, "r") as f:
        try:
            data = f.read()
        except (FileNotFoundError, json.JSONDecodeError):
            print("error with opening last submitted data or is empty")
        return data


def save_player_data(data):
    with open(player_data_path, "w") as f:
        json.dump(data, f, indent=4)


def update_last_submitted():
    # pst_date = datetime.now();
    # YY-mm-dd H:M
    pst_date = datetime.now(pytz.timezone("US/Pacific"))
    dt_string = pst_date.strftime("%A, %Y-%m-%d %I:%M %p")

    with open(last_updated_path, "w") as f:
        f.write(dt_string)


def add_player_names():
    player_data = open_player_data()
    for name, data in player_data.items():
        data["name"] = name
    save_player_data(player_data)
