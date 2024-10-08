from app import PlayerManager
from collections import defaultdict


class Player:
    def __init__(self, name, rating, loss_streak, primary_pos, secondary_pos=None):
        self.name = name
        self.rating = rating
        self.primary_pos = primary_pos
        self.secondary_pos = secondary_pos
        self.loss_streak = loss_streak
        self.primary_pos = primary_pos  # default pos

    def __repr__(self):
        return f"{self.name} ({self.position}) - Rating: {self.rating}, Loss Streak: {self.loss_streak}"


class Team:
    def __init__(self):
        self.players = []
        self.positions_filled = set()

    def add_player(self, player):
        self.players.append(player)
        self.positions_filled.add(player.position)

    @property
    def total_rating(self):
        return sum(player.rating for player in self.players)

    def has_open_position(self, position):
        return position not in self.positions_filled

    def __repr__(self):
        return f"{self.name} - Total Rating: {self.total_rating}\nPlayers: {','.join(p.name for p in self.players)}"


def balance_teams(players: list, required_positions):
    # primary_pool = [p for p in players if p.primary_pos in required_positions]
    primary_pool = [p for p in players if p.primary_pos != "fill"]
    secondary_pool = [
        p
        for p in players
        if p.secondary_pos in required_positions and p.primary_pos != p.secondary_pos
    ]
    fill_pool = [p for p in players if p.primary_pos == "fill"]

    # sort players by rating
    primary_pool.sort(key=lambda p: p.rating, reverse=True)
    secondary_pool.sort(key=lambda p: p.rating, reverse=True)
    fill_pool.sort(key=lambda p: p.rating, reverse=True)

    team1 = Team()
    team2 = Team()

    assigned_players = set()

    for position in required_positions:
        p1 = next(
            (
                p
                for p in primary_pool
                if p.position == position and p.name not in assigned_players
            ),
            None,
        )
        p2 = next(
            (
                p
                for p in primary_pool
                if p.position == position and p.name not in assigned_players
            ),
            None,
        )

        if p1:
            team1.add_player(p1)
            assigned_players.add(p1.name)
        if p2:
            team2.add_player(p2)
            assigned_players.add(p2.name)

        # If position is not filled, use secondary players
        if position not in team1.positions_filled:
            sp1 = next(
                (
                    p
                    for p in secondary_pool
                    if p.secondary_pos == position and p.name not in assigned_players
                ),
                None,
            )
            if sp1:
                sp1.position = sp1.secondary_pos
                team1.add_player(sp1)
                assigned_players.add(sp1.name)
        if position not in team2.positions_filled:
            sp2 = next(
                (
                    p
                    for p in secondary_pool
                    if p.secondary_pos == position and p.name not in assigned_players
                ),
                None,
            )
            if sp2:
                sp2.position = sp2.secondary_pos
                team2.add_player(sp2)
                assigned_players.add(sp2.name)

    # Fill remaining spots with fill players or left-over primary/secondary players
    remaining_pool = [
        p
        for p in primary_pool + secondary_pool + fill_pool
        if p.name not in assigned_players
    ]
    for p in remaining_pool:
        if len(team1.players) <= len(team2.players):
            team1.add_player(p)
        else:
            team2.add_player(p)
        assigned_players.add(p.name)

    # Balance teams by rating (optional optimization)
    total_team1 = team1.total_rating
    total_team2 = team2.total_rating

    if abs(total_team1 - total_team2) > 0:
        # Optional: Add a fine-tuning step to swap players for better balancing
        pass

    return team1, team2


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

    print("\nteam1: ", team1)
    print("\nteam2: ", team2)

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
    keys = list(grouped_players.keys())

    for i in range(len(keys)):
        new_role = keys[i]
        new_players_list = grouped_players[new_role]
    for role, players_list in grouped_players.items():
        if role == 0:
            continue
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
    return (
        max(20, min(rating_change, 200))
        if is_winning_team
        else min(-20, max(rating_change, -200))
    )


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
