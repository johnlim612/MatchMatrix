import os
from flask import jsonify
import json

playerDataFilePath = os.path.abspath("PlayerData.json")


def SubmitNewStudent(data):
    print("form data: ", data)
    try:
        # Do additional validation if needed
        with open(playerDataFilePath, 'a') as json_file:
            json.dump(data, json_file)
            json_file.write('\n')  # Add a new line for each entry
        return jsonify({"message": "Rating submitted successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)})
