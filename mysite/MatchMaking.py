import FileManager
import PlayerManager

def SubmitNewStudent(player_data):
    player_data['role'] = int(player_data.get('role', 0))
    player_data['role2'] = int(player_data.get('role2', 0))
    player_data['rating'] = int(player_data['rating'])

    # password = player_data.pop('password', None)
    add_player(name=player_data['name'], rating=player_data['rating'], role=player_data["role"], role2=player_data["role2"])

# search box autocomplete for adding players
def search_player(searchTerm):
    playerData = FileManager.open_player_data()
    result_names = [player['name'] for player in playerData if searchTerm in player['name'].lower()]
    return result_names

#roles: 0=fill 1=first speaker etc.
def add_player(name, rating=1000, role=0, role2=0):
    playerData = FileManager.open_player_data()

    #if player does not exist, add player
    if not any(player["name"] == name for player in playerData):
        new_player = {"name": name, "rating": rating, "role": role, "role2": role2, "loss_streak": 0}
        playerData.append(new_player)

    FileManager.update_player_data(playerData)

def delete_player(name):
    playerData = FileManager.open_player_data()
    open_data = [player for player in playerData if player['name'] != name]
    FileManager.update_player_data(open_data)

def list_players(sort_alpha = False):
    playerData = FileManager.open_player_data()
    if (sort_alpha):
        players = [player for player in sorted(playerData, key=lambda x: x['name'])]
        return players
    players = [player for player in sorted(playerData, key=lambda x: x['rating'], reverse=True)]
    players = PlayerManager.role_to_text(players)
    return players

def get_players_by_names(player_list):
    playerData = FileManager.open_player_data()
    player_list = [player for player in playerData if player['name'] in player_list]
    return player_list

def create_teams(players : list):
    player_list = get_players_by_names(players)

    # Sort players by role and then by rating (ascending) note: include reverse=False for opposite
    sorted_players = sorted(player_list, key=lambda x: (x['role'], -x['rating']), reverse=False)

    # Group players by role
    grouped_players = {0 : []}
    for player in sorted_players:
        role = player['role']
        if role not in grouped_players:
            grouped_players[role] = []
        grouped_players[role].append(player)

    # Initialize teams
    team1 = []
    team2 = []

    # Fill each role with one player when possible
    for role, players_list in grouped_players.items():
        if role == 0:
            continue

        # print('\nlist of grouped players ', role, players_list)
        team1_stronger = sum(player['rating'] for player in team1) > sum(player['rating'] for player in team2)
        if len(players_list) >= 2:
            if not team1_stronger:
                team1.append(players_list[0])
                team2.append(players_list[1])
            else:
                team2.append(players_list[0])
                team1.append(players_list[1])

            # Fill off role (3+ per role) players to second role or flex
            off_role_players = players_list[2:]

            for player in off_role_players:
                if "role2" not in player:
                    grouped_players[0].append(player)
                    continue

                if player["role2"] not in grouped_players:
                    grouped_players[player['role2']] = []

                # adjust player to secondary role
                grouped_players[player['role2']].append(player)

        elif len(players_list) == 1:
            # Only one player with this role, assign to the team that needs it
            if len(team1) == len(team2):
                team2.append(players_list[0]) if team1_stronger else team1.append(players_list[0])
                continue

            if len(team1) < len(team2):
                team1.append(players_list[0])
                continue

            team2.append(players_list[0])

    for i, player in enumerate(grouped_players[0]):
        if i % 2 == 0:
            # add to team2 first since team 1 will always have more if odd "fill" players
            team2.append(player)
        else:
            team1.append(player)
    if len(grouped_players[0]) % 2 == 1 and len(team1) != len(team2):
        team1.append(team2.pop())

    return team1, team2

def change_player_rating(players, team_rating_diff, team_won: bool):
    BASE_RATING_GAIN = 50
    # rating_change = (BASE_RATING_GAIN + (player["rating"] - average_enemy_rating) * (-1 / 10))

    rating_change = (BASE_RATING_GAIN + team_rating_diff * (-1 / 10))

    if team_won:
        rating_change = max(20, min(rating_change, 200))  # Ensuring rating_increase is between 20 and 200
        for player in players:
            player["rating"] = player["rating"] + rating_change
            player["loss_streak"] = 0
    else:
        rating_change = min(-20, max(rating_change, -200))  # Ensuring rating_increase is between -20 and -200
        for player in players:
            player["rating"] = player["rating"] - rating_change
            player["loss_streak"] += 1

def get_average_rating(player_list):
    total_rating = sum(player['rating'] for player in player_list)
    return total_rating/len(player_list)

def update_players_ratings(winning_player_names, losing_player_names):
    playerData = FileManager.open_player_data()
    losing_players = [player for player in playerData if player['name'] in losing_player_names]
    winning_players = [player for player in playerData if player['name'] in winning_player_names]
    losing_avg = get_average_rating(losing_players)
    winning_avg = get_average_rating(winning_players)
    team_rating_diff = winning_avg - losing_avg

    change_player_rating(winning_players, team_rating_diff, True)
    change_player_rating(losing_players, team_rating_diff, False)

    for player in playerData:
        for updated_player in (winning_players + losing_players):
            if player['name'] == updated_player['name']:
                player['rating'] = updated_player['rating']  # Update player rating
                player['loss_streak'] = updated_player['loss_streak']
    FileManager.update_player_data(playerData)



# def main():
#     return

# if __name__ == "__main__":
#     main()

