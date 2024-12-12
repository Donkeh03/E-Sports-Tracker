#Dataclass for matches. This acts as a struct holding the information about a match together in a single class

class Match():
    def __init__(self, MatchId : int, Date : str, Team1Name : str, Team2Name : str, GamePlayedName : str, WinningTeam : int, Team1Score : int, Team2Score: int):
        self.MatchID = MatchId
        self.Date = Date
        self.Team1 = Team1Name
        self.Team2 = Team2Name
        self.GamePlayed = GamePlayedName 
        self.WinningTeam = WinningTeam
        self.Team1Score = Team1Score
        self.Team2Score = Team2Score