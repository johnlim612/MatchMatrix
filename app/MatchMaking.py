from app import PlayerManager
from app.player import Team


def balance_teams(players: list, required_positions):
    # copies players with primary, secondary, and fill roles.
    primary_pool = [p for p in players if p.primary_pos in required_positions]
    secondary_pool = [p for p in players if p.secondary_pos in required_positions]
    fill_pool = [p for p in players if p.primary_pos == 0]

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
                if p != p1 and p.position == position and p.name not in assigned_players
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

    total_team1 = team1.total_rating
    total_team2 = team2.total_rating

    if abs(total_team1 - total_team2) > 0:
        pass  # for more balancing optimizations in the future
    return team1, team2


def get_balanced_teams(players: list, required_positions=[1, 2, 3]):
    # generates a list of player objects
    named_players = PlayerManager.get_players_by_names(players)

    # creates two balanced teams
    team1, team2 = balance_teams(named_players, required_positions)
    print("")
    print("team1: ", team1, "\n")
    print("team2: ", team2, "\n")

    # converts to list of dictionaries for GET request
    return team1.players_to_dicts(), team2.players_to_dicts()


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
    # retrieves names as dictionary of dictionary
    losing_players = PlayerManager.get_player_dict_by_names(losing_player_names)
    winning_players = PlayerManager.get_player_dict_by_names(winning_player_names)

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
