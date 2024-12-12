#Dataclass for a game that is played

class Game():
    def __init__(self, GameID : int, Name : str, IsRegistered : int):
        self.GameID = GameID
        self.Name = Name
        self.IsRegistered = IsRegistered