import json
import pytz
from datetime import datetime
import sys
sys.executable

playerDataFilePath = ("PlayerData.json")
lastSubmittedDataFilePath = ("LastUpdated.txt")

def open_player_data():
    with open(playerDataFilePath, 'r') as f:
        try:
            data = json.load(f)
        except:
            print("error with opening player data or is empty")
        return data

def open_last_submitted_data():
    with open(lastSubmittedDataFilePath, 'r') as f:
        try:
            data = f.read()
        except:
            print("error with opening last submitted data or is empty")
        return data

def update_player_data(data):
    with open(playerDataFilePath, 'w') as f:
        json.dump(data, f, indent=4)

def update_last_submitted():
    # pst_date = datetime.now();
    # YY-mm-dd H:M
    pst_date = datetime.now(pytz.timezone('US/Pacific'))
    dt_string = pst_date.strftime("%A, %Y-%m-%d %I:%M %p")

    with open(lastSubmittedDataFilePath, 'w') as f:
        f.write(dt_string)


