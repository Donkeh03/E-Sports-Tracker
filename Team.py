#A dataclass 'struct' to hold the data of a team

class Team():
    def __init__(self, TeamID : int, TeamName : str, IsRegistered : int, Score : int, GameID : int):
        self.TeamID = TeamID
        self.TeamName = TeamName
        self.IsRegistered = IsRegistered
        self.Score = Score
        self.Game = GameID