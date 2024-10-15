from app import FileManager
from app.player import Player


def role_to_text(players):
    # replaces player's role value with string
    for player in players:
        match player["role"]:
            case 1:
                player["role"] = "speaker 1"
            case 2:
                player["role"] = "speaker 2"
            case 3:
                player["role"] = "speaker 3"
            case _:
                player["role"] = "fill"
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


def search_player(searchTerm):
    # search box autocomplete for adding players
    playerData = FileManager.open_player_data()
    result_names = [name for name in playerData if searchTerm.lower() in name.lower()]
    return result_names


def add_player(name, rating=1000, role=0, role2=0):
    # roles: 0=fill 1=first speaker etc.
    playerData = FileManager.open_player_data()

    if name not in playerData:
        playerData[name] = {
            "name": name,
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


def list_players(sort_alpha=False) -> list[Player]:
    player_data = FileManager.open_player_data()

    if sort_alpha:
        sorted_players = [name for name in sorted(player_data.keys())]
        return sorted_players

    sorted_players = [player for player in sorted(player_data.values(), key=lambda x: x["rating"], reverse=True)]

    return role_to_text(sorted_players)


def get_player_dict_by_names(player_list) -> dict:
    player_data = FileManager.open_player_data()
    named_players = {
        name: player_data[name] for name in player_list if name in player_data
    }
    return named_players


def update_players_data(players):
    player_data = FileManager.open_player_data()

    for name in players.keys():
        player_data[name] = players[name]

    FileManager.save_player_data(player_data)


def load_players_from_json(json_data):
    players = {}
    for name, data, in json_data.items():
        players[name] = Player(
            name,
            data['rating'],
            data['loss_streak'],
            data['role'],
            data.get('role2')
        )
    return players


def get_players_by_names(names: list) -> list[Player]:
    players = load_players_from_json(FileManager.open_player_data())
    return [players[name] for name in names if name in players]
