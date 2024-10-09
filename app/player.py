class Player:
    def __init__(self, name, rating, loss_streak, primary_pos, secondary_pos=None):
        self.name = name
        self.rating = rating
        self.primary_pos = primary_pos
        self.secondary_pos = secondary_pos
        self.loss_streak = loss_streak
        self.position = primary_pos  # default pos

    def __repr__(self):
        return f"\n{self.name} ({self.position}) - Rating: {self.rating}, Loss Streak: {self.loss_streak}"

    def to_dict(self, include_current_pos=False):
        # converts players to dictionary
        data_dict = {
            'name': self.name,
            'rating': self.rating,
            'primary_pos': self.primary_pos,
            'secondary_pos': self.secondary_pos,
            'loss_streak': self.loss_streak
        }

        if include_current_pos:
            data_dict["position"] = self.position

        return data_dict


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
        return f"Total Rating: {self.total_rating}\nPlayers: {','.join(p.name for p in self.players)}"

    def players_to_dicts(self):
        return [player.to_dict(True) for player in self.players]
