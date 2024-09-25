def role_to_text(players):
    for player in players:
        match player["role"]:
            case 1: player["role"] = "speaker 1"
            case 2: player["role"] = "speaker 2"
            case 3: player["role"] = "speaker 3"
            case _: player["role"] = "fill"
        player["rating"] = round(player["rating"])
    return players

