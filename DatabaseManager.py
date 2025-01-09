#Database manager is a class that is meant to be instanced in various pages and allows another class to call the database for it's data
#Login is handeled on the init of the class, method functions deal with queries and forign key formatting, to ensure returned data can be used instantly

#Global imports
import mysql.connector # Required import for making queries to a MySQL database

#Local imports
import Match # Used to constructing matches
import Team # Used for constructing teams
import Game # Used for making games
import Utils # Used for erroring

class DBManager():
    #Class constructor that makes a login to the database and accesses the sen4000 database
    #In the event of an error - a critical error popup is displayed
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                    host = "localhost",
                    user = "root",
                    password = "",
                    database = "sen4000")
        except:
            Utils.Error("Unable to connect to database")
            return
        
        #Init of the cache dict's. Which map Team/Game ID's to their names
        self.TeamNameCache = {}
        self.GameNameCache = {}

    #Function that gets X amount of the most recent matches from the database
    def GetMostRecentMatches(self, NumberOfMatches : int):
        #Open a querable connection to the database
        QueryConnection = self.connection.cursor()

        #Query the database for the X most recent matches, ordered by date descending
        QueryConnection.execute(f"SELECT * FROM `matches` ORDER BY `matches`.`Date` DESC LIMIT {NumberOfMatches}")

        #Fetch all data collected from the query
        MatchData = QueryConnection.fetchall()

        #Init an empty list that will hold X many match objects formed from the data collected
        Matches = []

        #Iterate over the rows from the database and convert them into match objects
        #Each object made doesnt include the raw data, but the formatted version
        #i.e. team id's are convered to their names - this makes the data instantly usable once it is returned instead of having to go through an intermideary step before being displayed 
        for match in MatchData:
            Matches.append(Match.Match(match[0], match[1], self.GetTeamNameFromTeamID(match[2]),self.GetTeamNameFromTeamID(match[3]),self.GetGameNameFromGameID(match[4]), match[5], match[6], match[7]))

        #Return the list of formed match objects to the caller
        return Matches
    
    #For the combo boxes in the admin page, a list of valid game names is needed. 
    #This method gets all the currently registered game's names and returns them to the caller
    def GetAllRegisteredGameNames(self):
        #Init a connection to the database
        QueryConnection = self.connection.cursor()

        #Execute a query on the database to get all game names from currently registered games
        QueryConnection.execute(f"SELECT `GameName` FROM `Games` WHERE `IsRegistered` = 1")
        
        #Fetch all the data from the query
        GameNames = QueryConnection.fetchall()
        
        #If there is no data, return 'No Games' to be displayed on the combo box input
        if len(GameNames) <= 0:
            return 'No Games'
        
        #Becuase there is data, return the game name data to the caller
        return [GameName[0] for GameName in GameNames]
    
    #The combo box inputs in the match input need a list of values to selct from the dropdown
    #This method gets all the team names that are current registered
    def GetAllRegisteredTeamNames(self):
        #Init a connection to the database
        QueryConnection = self.connection.cursor()

        #Execute a query on the database to get all game names from currently registered teams
        QueryConnection.execute(f"SELECT `TeamName` FROM `teams` WHERE `IsRegistered` = 1")
        
        #Fetch all the data from the query
        TeamNames = QueryConnection.fetchall()
        
        #If there is no data, return 'No teams' to be displayed on the combo box input
        if len(TeamNames) <= 0:
            return 'No Teams'
        
        #Becuase there is data, return a lsit of team names to the caller
        return [TeamName[0] for TeamName in TeamNames]

    #The update match function takes a match object and uses its class attributes as paramters to form the query
    #Returns true if successful, false if not. Try except used to catch all errors with the query and commiting the change
    def UpdateMatch(self, match : Match.Match) -> bool:
        #Making a connection to the database
        QueryConnection = self.connection.cursor()

        #Catch all errors in either commiting to the database or the UPDATE query
        try:
            #Executing the query on the database, based on the matchID
            QueryConnection.execute(f"UPDATE `matches` SET `Date`= %s,`Team1`= %s,`Team2`= %s,`GamePlayed`= %s,`WinningTeam`= %s,`Team1Score`= %s,`Team2Score`= %s WHERE `MatchId` = %s", (match.Date, match.Team1, match.Team2, match.GamePlayed, match.WinningTeam, match.Team1Score, match.Team2Score, match.MatchID))

            #Commiting the query to the database so that the change stays
            self.connection.commit()

            #Return true as query was successful
            return True
        except:
            #Return false as an error occured
            return False

    #The make new match function takes in seperate values that the match has, but parses them as params in the SQL query
    #MatchID is 'dropped' as the database will deal with it at insertion time
    #Returns true if successful, false if not. Try except used to catch all errors with the query and commiting the change
    def MakeNewMatch(self, MatchDate : str, Team1Name : str, Team2Name : str, GameName : str, WinningTeam : str, Team1Score : str, Team2Score : str) -> bool:
        #Making a connection to the database to let us run queries
        QueryConnection = self.connection.cursor()

        #Catch any errors in commits or queries
        try:
            #Construt and then execue the query on the database
            QueryConnection.execute(f"INSERT INTO `matches`(`Date`, `Team1`, `Team2`, `GamePlayed`, `WinningTeam`, `Team1Score`, `Team2Score`) VALUES (%s,%s,%s,%s,%s,%s,%s)", (MatchDate, Team1Name, Team2Name, GameName, WinningTeam, Team1Score, Team2Score))

            #Commit the change to the db
            self.connection.commit()
            
            #Execute the query to increase a team's score by 1 based on the winner
            QueryConnection.execute(f"UPDATE `teams` SET `Score` = `Score` + 1 WHERE `TeamId` = {Team1Name if WinningTeam == 0 else Team2Name}")

            #Commit change to db
            self.connection.commit()

            #Return true as all queries ran successfully
            return True
        except:
            #Return false due to error
            return False

    #Given the properties of a team, consutrct and then exectue a query on the server to insert them as a new record
    #Returns true if successful, false if not. Try except used to catch all errors with the query and commiting the change
    def MakeNewTeam(self, TeamName : str, TeamScore : int, IsRegistered : int, TeamGame : int) -> bool:
        #Opening a connection to the database
        QueryConnection = self.connection.cursor()

        #try catch block to ensure errors in query or commit don't break the program
        try:
            #Constructing a escaped query to insert the team into the database 
            QueryConnection.execute(f"INSERT INTO `teams` (`TeamName`, `Score`, `IsRegistered`, `GameID`) VALUES (%s, %s, %s, %s)", (TeamName, TeamScore, IsRegistered, TeamGame))

            #commiting the change to the database to ensure it remains
            self.connection.commit()

            #return true as the new team has been successfully made
            return True
        except:
            #false is returned as an error occured
            return False

    #Given a team object, use its attributes to construct an update query for the record
    #Returns true if successful, false if not. Try except used to catch all errors with the query, commiting change or updating cache dict
    def UpdateTeam(self, TeamData : Team.Team) -> bool:
        #Making a connection to the database
        QueryConnection = self.connection.cursor()
        
        #Catch any errors in update logic
        try:
            #Executing the query on the database, ensuring to only affect the given teamID
            QueryConnection.execute(f"UPDATE `teams` SET `TeamName`= %s,`IsRegistered`= %s,`Score`= %s,`GameID`= %s WHERE `TeamId` =  %s", (TeamData.TeamName, TeamData.IsRegistered, TeamData.Score, TeamData.Game, TeamData.TeamID))

            #Commiting the query to the database so that the change stays
            self.connection.commit()

            #Updating the cache to prevent invalid old cache error
            self.TeamNameCache[TeamData.TeamID] = TeamData.TeamName

            #return true as all was successful
            return True
        except:
            #return false due to an error arisng
            return False

    #Get scores makes a list of N team objects and retuns it to the sender (used in scoreboard and game scoreboard display)
    def GetScores(self, NumberOfScores : int):
        #Open a querable connection to the database
        QueryConnection = self.connection.cursor()

        #Query the database for X number of scores, ordered by score descending
        QueryConnection.execute(f"SELECT * FROM `teams` WHERE `IsRegistered`= 1 ORDER BY `teams`.`Score` DESC LIMIT {NumberOfScores}")

        #Fetch all data collected from the query
        ScoreData = QueryConnection.fetchall()

        #Init an empty list that will hold X many team objects formed from the data collected
        Scores = []

        for score in ScoreData:
            Scores.append(Team.Team(score[0], score[1], score[2], score[3], score[4]))
        
        return Scores

    #Get all the games that are played (registered) from the db and return them. comprehended as a list of game objects
    def GetGamesPlayed(self, RegisteredCheck : bool = True):
        #Open a querable connection to the database
        QueryConnection = self.connection.cursor()

        if RegisteredCheck:
            #Query the database for all the registered games
            QueryConnection.execute(f"SELECT * FROM `games` WHERE `IsRegistered` = 1")
        else:
            #Query the database for all the games
            QueryConnection.execute(f"SELECT * FROM `games` ORDER BY `games`.`IsRegistered` DESC")

        #Fetch all data collected from the query
        GameData = QueryConnection.fetchall()

        #Init an empty list that will hold many game objects formed from the data collected
        GamesPlayed = []

        #for each game in the returned data, make a game object and append it to the list
        for game in GameData:
            GamesPlayed.append(Game.Game(game[0], game[1], game[2]))
        
        #Return the list of the games played
        return GamesPlayed

    #Given a GameID return the team names and their score to the caller, who match the parsed GameID
    def GetTeamAndScoresFromGameID(self, GameID : int):
        #Open a querable connection to the database
        QueryConnection = self.connection.cursor()

        #Query the database for all the registered games
        QueryConnection.execute(f"SELECT `TeamName`, `Score` FROM `teams` WHERE `IsRegistered` = 1 AND `GameID` = {GameID}")

        #Get the data from the query
        TeamsAndScores = QueryConnection.fetchall()

        #Init a blank dict to store all of the teams and their relative score
        TeamScoreDict = {}

        #Iterate over the team and scores within the returned data, for every record, insert the data into the dictionary
        for TeamsAndScore in TeamsAndScores:
            TeamScoreDict[TeamsAndScore[0]] = TeamsAndScore[1]

        #Return the dictinary to the caller
        return TeamScoreDict

    #Conversion function that queries the database for the name of a team based on a provided index
    #Function uses a cache to reduce the amount of potential database calls to improve response time
    def GetTeamNameFromTeamID(self, TeamID : int):
        #Check the cache for the parsed TeamID. If it exists, return the value
        if TeamID in self.TeamNameCache.keys():
            return self.TeamNameCache[TeamID]

        #Make a queryable connection to the database
        QueryConnection = self.connection.cursor()

        #Get the team name from the team's ID
        QueryConnection.execute(f"SELECT `TeamName` FROM `teams` WHERE `TeamId` = {TeamID}")

        #Return the name of the team to the caller
        #The name of the team is nested inside a list and then a set, hence the [0][0] to index them both properly
        #As we have got past the cache check, this value isnt in the cache, so it needs to be added
        TeamName = QueryConnection.fetchall()[0][0]
        self.TeamNameCache[TeamID] = TeamName

        return TeamName
    
    #Duplicate of GetTeamNameFromTeamID, but for game name with a game ID
    #Function uses a cache to reduce the amount of potential database calls to improve response time
    def GetGameNameFromGameID(self, GameID : int):
        #Check the cache for the parsed TeamID. If it exists, return the value
        if GameID in self.GameNameCache.keys():
            return self.GameNameCache[GameID]
        
        #Open connection to the database
        QueryConnection = self.connection.cursor()

        #Select the name of the game with the given ID
        QueryConnection.execute(f"SELECT `GameName` FROM `games` WHERE `GameId` = {GameID}")

        #From the returned data, extract the name from the query and add it to cache dict
        GameName = QueryConnection.fetchall()[0][0]
        self.GameNameCache[GameID] = GameName

        #Return the converted game name to caller
        return GameName
    
    #Unlike the GetScores function which orders by score and only gets registered teams
    #This function gets all teams and orders them registered to un-registered
    def GetTeamsSortedByRegistered(self):
        #Open a query to the database
        QueryConnection = self.connection.cursor()

        #Select all teams and order the results by their registered value
        QueryConnection.execute("SELECT * FROM `teams` ORDER BY `teams`.`IsRegistered` DESC")

        #Fetch all the data from the query
        TeamData = QueryConnection.fetchall()

        #Init an empty list to hold all of the team objects
        Teams = []

        #For each team in the returned data, make a team object and append it to the list
        for team in TeamData:
            Teams.append(Team.Team(team[0], team[1], team[2], team[3], team[4]))

        #Return the list of teams back to the caller
        return Teams
    
    #Given a game object, construct and update the given row in the database
    #Returns true if successful, false if not. Try except used to catch all errors with the query, commiting the change and updating cache dict
    def UpdateGame(self, GameData : Game.Game) -> bool:
        #Open a connection to the database
        Connection = self.connection.cursor()

        #Catch all errors
        try:
            #Update the game record matching the ID value in the parse object
            Connection.execute(f"UPDATE `games` SET `GameName`= %s,`IsRegistered`= %s WHERE `GameId` =  %s", (GameData.Name, GameData.IsRegistered, GameData.GameID))

            #Commit the update to the database
            self.connection.commit()

            #Updating the cache to reflect the updated name, to prevent old cache read errors
            self.GameNameCache[GameData.GameID] = GameData.Name

            #Return true as everything was successful
            return True
        except:
            #Return flase as an error arouse during runtime
            return False

    #Given the values needed to make a game, construct and execute a query to add the game as a new row
    #Returns true if successful, false if not. Try except used to catch all errors with the query and commiting the change
    def MakeNewGame(self, GameName : str, IsRegistered : int) -> bool:
        #Open a connection to manipulate the database
        Connection = self.connection.cursor()

        try:
            #insert a new record into the db with the values parsed
            Connection.execute(f"INSERT INTO `games`(`GameName`, `IsRegistered`) VALUES (%s, %s)", (GameName, IsRegistered))

            #Save the changes to the database
            self.connection.commit()

            #Return true as query and commit were successful
            return True
        except:
            #Return false as an error occured
            return False


    def GetGameIDFromGameName(self, GameName) -> bool | int:
        #If the game name parsed is an empty string, return false
        if len(GameName) <= 0: return False, 0

        #If the game name parsed is in the cache, iter over the dict until the game name is found, then return the key as that is the ID
        if GameName in self.GameNameCache.values():
            for GameID, gameName in self.GameNameCache.items():
                if gameName == GameName:
                    return True, GameID
                
        #Open connection to the database
        QueryConnection = self.connection.cursor()

        #Select the name of the game with the given ID
        QueryConnection.execute(f"SELECT `GameId` FROM `games` WHERE `GameName` = '{GameName}'")

        GameID = QueryConnection.fetchall()[0][0]
       
        if GameID:
            return True, GameID
        else:
            return False, 0
    

    def GetTeamIDFromTeamName(self, Team1Name, Team2Name) -> bool | int:
        #If the parsed team names have a length less than 0, return false
        if len(Team1Name) <= 0 or len(Team2Name) <= 0: return False, 0, 0

        #Cache check. If both of the names parsed are in the team name cache the database call can be avoided.
        #To get the IDs, iterate over the team cache and find the matching names, once either is found set the corrosponding variable to the key (ID)
        if Team1Name in self.TeamNameCache.values() and Team2Name in self.TeamNameCache.values():
            Team1ID, Team2ID = 0, 0

            for Index, Value in self.TeamNameCache.items():
                if Value == Team1Name:
                    Team1ID = Index
                elif Value == Team2Name:
                    Team2ID = Index
            
            return True, Team1ID, Team2ID

        #Open connection to the database
        QueryConnection = self.connection.cursor()

        #Select the ID of the teams from their names
        QueryConnection.execute(f"SELECT `TeamId` FROM `teams` WHERE `TeamName` = %s OR `TeamName` = %s", (Team1Name, Team2Name))

        #Get the data from the the query
        TeamNameData = QueryConnection.fetchall()
        
        #From the retrived data, return true and the team ID's
        return True, TeamNameData[0][0], TeamNameData[1][0]