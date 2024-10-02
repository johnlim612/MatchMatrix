from app import PlayerManager
from collections import defaultdict


def create_teams(players: list):
    # Get and sort players
    player_list = PlayerManager.get_players_by_names(players)
    sorted_players = sort_players_by_role_and_rating(player_list)

    grouped_players = group_players_by_role(sorted_players)

    team1, team2 = [], []

    # Distribute players by role into the teams
    distribute_players_by_role(grouped_players, team1, team2)

    # Balance remaining players not in roles.
    balance_flex_players(grouped_players[0], team1, team2)

    return team1, team2


def sort_players_by_role_and_rating(player_list):
    return sorted(player_list.items(), key=lambda x: (x[1]["role"], -x[1]["rating"]))


def group_players_by_role(sorted_players):
    grouped_players = defaultdict(list)
    for name, player in sorted_players:
        role = player["role"]
        grouped_players[role].append(player)
    return grouped_players


# Returns total rating of team
def calculate_team_strength(team):
    return sum(player["rating"] for player in team)


# Assigns top 2 players in role to either team accordingly
def assign_strongest_players(players_list, team1, team2):
    if calculate_team_strength(team1) <= calculate_team_strength(team2):
        team1.append(players_list[0])
        team2.append(players_list[1])
    else:
        team2.append(players_list[0])
        team1.append(players_list[1])


# Pushes remaining players to secondsary or flex roles
def assign_extra_players(players_list, grouped_players):
    for player in players_list[2:]:
        if "role2" in player:
            grouped_players[player["role2"]].append(player)  # Assign to secondary role
        else:
            grouped_players[0].append(player)  # Assign to flex role


# Main function to distribute players by role into teams
def distribute_players_by_role(grouped_players, team1, team2):
    for role, players_list in grouped_players.items():
        if len(players_list) >= 2:
            assign_strongest_players(players_list, team1, team2)
            assign_extra_players(players_list, grouped_players)
        elif len(players_list) == 1:
            # Assign the only player to the weaker team
            if calculate_team_strength(team1) <= calculate_team_strength(team2):
                team1.append(players_list[0])
            else:
                team2.append(players_list[0])


# Function to balance flex players (role 0) between teams
def balance_flex_players(flex_players, team1, team2):
    for i, player in enumerate(flex_players):
        if i % 2 == 0:
            team2.append(player)
        else:
            team1.append(player)

    # If there's an odd number of flex players, balance the teams
    if len(flex_players) % 2 == 1 and len(team1) != len(team2):
        team1.append(team2.pop())


def calculate_rating_change(team_rating_diff, is_winning_team: bool):
    BASE_RATING_GAIN = 50
    # rating_change = (BASE_RATING_GAIN + (player["rating"] - average_enemy_rating) * (-1 / 10))
    rating_change = BASE_RATING_GAIN + team_rating_diff * (-1 / 10)
    return max(20, min(rating_change, 200)) if is_winning_team else min(-20, max(rating_change, -200))


def get_average_rating(player_list):
    total_rating = sum(player["rating"] for player in player_list.values())
    return total_rating / len(player_list)


def update_player_rating(player, rating_change, is_winning_team: bool):
    player["rating"] += rating_change
    player["loss_streak"] = 0 if is_winning_team else player.get("loss_streak", 0) + 1


def update_players_ratings(winning_player_names, losing_player_names):

    losing_players = PlayerManager.get_players_by_names(losing_player_names)
    winning_players = PlayerManager.get_players_by_names(winning_player_names)

    losing_avg = get_average_rating(losing_players)
    winning_avg = get_average_rating(winning_players)
    
    team_rating_diff = winning_avg - losing_avg

    winning_rating_change = calculate_rating_change(team_rating_diff, True)
    losing_rating_change = calculate_rating_change(team_rating_diff, False)

    # Update player ratings in player_data directly
    for player in winning_players.values():
        update_player_rating(player, winning_rating_change, True)
        PlayerManager.update_players_data(winning_players)

    for player in losing_players.values():
        update_player_rating(player, losing_rating_change, False)
        PlayerManager.update_players_data(losing_players)

   
