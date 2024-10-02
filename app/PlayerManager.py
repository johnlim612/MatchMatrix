from app import FileManager


def role_to_text(players):
    for _, player in players:
        match player["role"]:
            case 1: player["role"] = "speaker 1"
            case 2: player["role"] = "speaker 2"
            case 3: player["role"] = "speaker 3"
            case _: player["role"] = "fill"
        player["rating"] = round(player["rating"])
    return players


def SubmitNewStudent(player_data):
    player_data["role"] = int(player_data.get("role", 0))
    player_data["role2"] = int(player_data.get("role2", 0))
    player_data["rating"] = int(player_data["rating"])

    # password = player_data.pop('password', None)
    add_player(
        name=player_data["name"],
        rating=player_data["rating"],
        role=player_data["role"],
        role2=player_data["role2"],
    )


# search box autocomplete for adding players
def search_player(searchTerm):
    playerData = FileManager.open_player_data()
    result_names = [name for name in playerData if searchTerm.lower() in name.lower()]
    return result_names


# roles: 0=fill 1=first speaker etc.
def add_player(name, rating=1000, role=0, role2=0):
    playerData = FileManager.open_player_data()

    if name not in playerData:
        playerData[name] = {
            "rating": rating,
            "role": role,
            "role2": role2,
            "loss_streak": 0,
        }

    FileManager.save_player_data(playerData)


def delete_player(name):
    playerData = FileManager.open_player_data()

    if name in playerData:
        del playerData[name]

    FileManager.save_player_data(playerData)


def list_players(sort_alpha=False):
    player_data = FileManager.open_player_data()

    if sort_alpha:
        sorted_players = [name for name in sorted(player_data.keys())]
        return sorted_players

    sorted_players = {
        name: data
        for name, data in sorted(
            player_data.items(), key=lambda x: x[1]["rating"], reverse=True
        )
    }

    return role_to_text(sorted_players)


def get_players_by_names(player_list):
    player_data = FileManager.open_player_data()
    named_players = {name: player_data[name] for name in player_list if name in player_data}
    return named_players


def update_players_data(players):
    player_data = FileManager.open_player_data()

    for name in players.keys():
        player_data[name] = players[name]

    FileManager.save_player_data(player_data)
