#This is the page that a normal user would access.It lets them view the matches, scoreboard and registered games, all of which are stored in the database

#Global imports
import customtkinter # Used for making the GUI

#Local imports
import Utils # Used for relativly sizing UI elements
import DatabaseManager # Used to get data to be displayed
from Match import Match # Used for type declaration in a function
from Team import Team # Used for type declaration in a function
from Game import Game # Used for type delcaration in a function

class UserPage(customtkinter.CTkFrame):
    def __init__(self, parent, controller): 
        customtkinter.CTkFrame.__init__(self, parent, Utils.X, Utils.Y)
         
        #Making of the control and connection class level variables:
        # - Control used for page switching functionality
        # - Connection used for getting data from the database
        self.Control = controller
        self.Connection = DatabaseManager.DBManager()

        #The main navigation of this page - SideBar has 3 GUI buttons each show a user a specific part of the app; Recent matches, Scoreboard and Games
        SideBar = customtkinter.CTkFrame(self, height=Utils.Y, width=Utils.RelXSize(0.095), fg_color='#000000')
        SideBar.place(relx=0, rely=0.5, anchor=customtkinter.W)
        
        #Creation and placing of the 3 GUI buttons for each 'sub-page'
        MatchBtnIcon = Utils.MakeCtkImageFromName("MatchIcon.png", (45,45))
        MatchesBtn = customtkinter.CTkButton(SideBar, text="", image=MatchBtnIcon, corner_radius=8, height=Utils.RelYSize(0.07, SideBar), width=Utils.RelXSize(0.75, SideBar), command=self.SwitchToMatchesDisplay, fg_color='#403939', hover_color='#252222')
        MatchesBtn.place(relx=0.5, rely=0.25, anchor=customtkinter.N)
       
        ScoreboardBtnIcon = Utils.MakeCtkImageFromName("ScoreboardIcon.png", (45,45))
        ScoreBoardBtn = customtkinter.CTkButton(SideBar, text="", image=ScoreboardBtnIcon, corner_radius=8, height=Utils.RelYSize(0.07, SideBar), width=Utils.RelXSize(0.75, SideBar), command=self.SwitchToScoreboadDisplay, fg_color='#403939', hover_color='#252222')
        ScoreBoardBtn.place(relx=0.5, rely=0.5, anchor=customtkinter.N)

        GameBtnIcon = Utils.MakeCtkImageFromName("GameIcon.png", (45,45))
        GamesBtn = customtkinter.CTkButton(SideBar, text="", image=GameBtnIcon, corner_radius=8, height=Utils.RelYSize(0.07, SideBar), width=Utils.RelXSize(0.75, SideBar), command=self.SwitchToGamesDisplay, fg_color='#403939', hover_color='#252222')
        GamesBtn.place(relx=0.5, rely=0.75, anchor=customtkinter.N)
        
        #The main frame acts as a holding frame for the content that needs to be displayed (index 0 of main frame's children)
        self.MainFrame = customtkinter.CTkFrame(self, height=Utils.RelYSize(0.70), width=Utils.RelXSize(1.1), corner_radius=24, fg_color='#000000')
        self.MainFrame.place(relx=0.5325,rely=0.035, anchor=customtkinter.N)

        #The title for the frame, this contextualise the displayed data. (index 1 of main frame's children)
        self.MainFrameTitle = customtkinter.CTkLabel(self.MainFrame, font=('Roboto', 40, 'bold'), height=Utils.RelYSize(0.15, self.MainFrame), width=Utils.RelXSize(0.75, self.MainFrame))
        self.MainFrameTitle.place(relx=0.15, rely=0.05, anchor=customtkinter.W)

        #At the end of the init, once the core UI has been made, call SwitchToMatchesDisplay. This is the page that should be loaded for the user first
        self.SwitchToMatchesDisplay()

    #Class method for switching the main frame's content to the 5 most recent matches
    def SwitchToMatchesDisplay(self): 
        #A function's sub-function. Needed for generating a UI element that displays a matches data based on the parsed Match
        #Returns a CTkframe 'background'. The UI is generated in a nested way, background holds everything
        def GenerateMatchUI(MatchData : Match) -> customtkinter.CTkFrame:
            #Creation of a background, the holder for everything else in the UI
            background = customtkinter.CTkFrame(self.MainFrame, width=Utils.RelXSize(0.9, self.MainFrame), height=Utils.RelYSize(0.15, self.MainFrame), corner_radius=24)

            #DateLbl is a text label which displays the date of the match. Positioned in the lower left corner of the background
            dateLbl = customtkinter.CTkLabel(background, text=Utils.ReverseDate(MatchData.Date), width=Utils.RelXSize(0.15, background), height=Utils.RelYSize(0.275, background), font=('Roboto', 20, 'bold'))
            dateLbl.place(relx=0.185, rely=0.65, anchor=customtkinter.N)

            #GameLbl is a text label that shows the name of the game which was played. Positon vertically above the date in a bigger font
            gameLbl = customtkinter.CTkLabel(background, text=MatchData.GamePlayed, width=Utils.RelXSize(0.3, background), height=Utils.RelYSize(0.35, background), font=('Roboto', 26, 'bold'))
            gameLbl.place(relx=0.185, rely=0.075, anchor=customtkinter.N)

            #MatchStats is an invisible frame which contains the team vs team text and the scores either team achieved
            #Without this invisible frame, positioning and sizing is much harder, most notable for smaller UI elements
            MatchStats = customtkinter.CTkFrame(background, width=Utils.RelXSize(0.55, background), height=Utils.RelYSize(0.4, background), fg_color="transparent")
            MatchStats.place(relx=0.95, rely=0.5,anchor=customtkinter.E)

            #TeamLbl is a text label which has the text of the 2 teams that fought each other. Positioned horizontally centeral
            TeamLbl = customtkinter.CTkLabel(MatchStats,text=f"{MatchData.Team1} vs. {MatchData.Team2}", width=Utils.RelXSize(0.65, MatchStats), height=Utils.RelYSize(1, MatchStats), font=('Roboto', 20, 'bold'), text_color='#FFFFFF')
            TeamLbl.place(relx=0.5, rely=0, anchor=customtkinter.N)

            #Both ScoreBoxes are coloured red by defualt to make showing the winner easier, as only 1 box needs to have it colour re-configured
            #Team1ScoreBox is a box which will contain a text label for team 1's score in the game. Positoned to the left of TeamLbL
            Team1ScoreBox = customtkinter.CTkFrame(MatchStats, width=Utils.RelXSize(0.1, MatchStats), height=Utils.RelYSize(1,MatchStats), fg_color='transparent')
            Team1ScoreBox.place(relx=0.05, rely=0.5, anchor=customtkinter.W)

            #Same as Team1ScoreBox, but for team 2 with their data
            Team2ScoreBox = customtkinter.CTkFrame(MatchStats, width=Utils.RelXSize(0.1, MatchStats), height=Utils.RelYSize(1,MatchStats), fg_color='transparent')
            Team2ScoreBox.place(relx=0.95, rely=0.5, anchor=customtkinter.E)

            #Team1ScoreBoxLbl is a text label that shows the score team 1 acheived in this match. Positioned in the center of the recently made box
            Team1ScoreBoxLbl =  customtkinter.CTkLabel(Team1ScoreBox, text=MatchData.Team1Score, width=Utils.RelXSize(1, Team1ScoreBox), height=Utils.RelYSize(1, Team1ScoreBox), font=('Inter', 18, 'bold'), corner_radius=8, fg_color='#A30F0F')
            Team1ScoreBoxLbl.place(relx=0.5, rely=0, anchor=customtkinter.N)

            #Text label the same as Team1ScoreBoxLbl, with team 2's data
            Team2ScoreBoxLbl =  customtkinter.CTkLabel(Team2ScoreBox, text=MatchData.Team2Score, width=Utils.RelXSize(1, Team2ScoreBox), height=Utils.RelYSize(1, Team2ScoreBox), font=('Inter', 18, 'bold'), corner_radius=8, fg_color='#A30F0F')
            Team2ScoreBoxLbl.place(relx=0.5, rely=0, anchor=customtkinter.N)
            
            #Now that the main UI elements have been made, the winning team needs their score box to be green
            #To achieve this, re-configure the colour of the winners score box.
            #0 means team 1 won
            #1 means team 2 won
            if MatchData.WinningTeam == 0:
                Team1ScoreBoxLbl.configure(fg_color="#18A30F")
            else:
                Team2ScoreBoxLbl.configure(fg_color="#18A30F")

            #With a now fully made UI, return it to the caller
            return background
        
        #The first step of the function is to configure the text of the title so that it matches the content that is about to be displayed on it
        self.MainFrameTitle.configure(text="Recent Matches")
        
        #Call the database manager to make a query on the database for the X most recent matches (X is 5, but in future could be more)
        Matches = self.Connection.GetMostRecentMatches(5)

        #PurgeList is a list of UI element, ignoring the 0 and 1 indexes of the mainframes children, which are to be deleted later
        #This is needed as this function is called again, when the user navigates back to this page, duplicate UI's would be made
        #As a result the old UI's need to be purged, but doing so at this point causes a 'DictionarySizeChanged during iteration' error
        #So they are stored in a list to be deleted at a later date. When the list is complied the old UI elements are un-rendered with obj.forget_place()
        PurgeList = self.FindItemsToPurge()
        
        #Now that the old UI elements are gone, the new UI elements can be made, with a simple iteration over the list of matches and a call to the generate UI function
        for PosIndex, Game in enumerate(Matches):
            UI = GenerateMatchUI(Game)
            UI.place(relx=0.5, rely=(0.125 + (0.175 * PosIndex)), anchor=customtkinter.N)

        #Now that the page is fully rendered, the old UI objects can be destroyed
        for Widget in PurgeList:
            Widget.destroy()

    #Function for switching the main display to the "scoreboard", inititaly a scrolling frame is made and the headers for the table are made, then the core UI elments are made via the sub-function
    def SwitchToScoreboadDisplay(self): # TODO add buttons to change the top amount shown
        #Before the core UI elements are made the existing UI elements from other pages that user MainFrame need to be forgotten
        PurgeList = self.FindItemsToPurge()

        #Dictionary mapping placement colours, 1st - 3rd, with some hex colour codes - these are used when colouring the place number text label
        PlacementColourIndex = {
            1 : "#DFB40F", # Golden-yellow
            2 : "#C0C0C0", # Metalic-ish silver
            3 : "#B86818"} # Copper-like Bronze

        #The generator sub function for making a score board panel based on the team object parsed. Similar to the match sub-function a CTkFrame is returned with nested child elements
        #Place is parsed as it is isn't stored within the team object and the data from the database is returned sorted by score descending
        def GenerateScoreBoardPanel(TeamScore : Team, Place : int) -> customtkinter.CTkFrame:
            #Creation of a background, the holder for everything else in the UI. Parented to the ScrollingFrame made ealier
            BannerBackground = customtkinter.CTkFrame(ScrollingFrame, width=Utils.RelXSize(0.9, ScrollingFrame), height=Utils.RelYSize(0.15, ScrollingFrame), corner_radius=24, fg_color='#3C3939')

            #This is the black rounded box around the place value for this banner element. Positoned to the far left of the background
            PlaceValueBox = customtkinter.CTkFrame(BannerBackground, width=Utils.RelXSize(0.0775, BannerBackground), height=Utils.RelYSize(0.5725, BannerBackground), fg_color='#000000', corner_radius=10)
            PlaceValueBox.place(relx=0.05, rely=0.5, anchor=customtkinter.W)
            
            #The text label made for the above box, coloured using the placement index in the next step, defualted to white for 4th-xth
            PlaceBoxLbl = customtkinter.CTkLabel(PlaceValueBox,text=f"{Place}.", width=Utils.RelXSize(0.5, PlaceValueBox), height=Utils.RelYSize(0.5, PlaceValueBox), font=('Inter', 26, 'bold'), bg_color='#000000', text_color='#FFFFFF')
            PlaceBoxLbl.place(relx=0.5, rely=0.1, anchor=customtkinter.N)
            
            #If the team is within the top 3, reconfigure their place' text colour to use the hex colour in the dict
            if Place <= 3:
                PlaceBoxLbl.configure(text_color=PlacementColourIndex[Place])

            #The text label for the team for this banner element, the biggest text element of this UI element, positined centeral to the banner
            TeamNameLbl = customtkinter.CTkLabel(BannerBackground,text=TeamScore.TeamName, width=Utils.RelXSize(0.5, BannerBackground), height=Utils.RelYSize(0.6, BannerBackground), font=('Inter', 30, 'bold'))
            TeamNameLbl.place(relx=0.5, rely=0.2, anchor=customtkinter.N)

            #Duplicate box made for the score of the team, but on the opposite side of the banner
            ScoreValueBox = customtkinter.CTkFrame(BannerBackground, width=Utils.RelXSize(0.0775, BannerBackground), height=Utils.RelYSize(0.5725, BannerBackground), fg_color='#000000', corner_radius=10)
            ScoreValueBox.place(relx=0.95, rely=0.5, anchor=customtkinter.E)

            #Text label that is placed in the above box, this displays the current score of the team parsed
            ScoreBoxLbl = customtkinter.CTkLabel(ScoreValueBox ,text=TeamScore.Score, width=Utils.RelXSize(0.5, ScoreValueBox), height=Utils.RelYSize(0.5, ScoreValueBox), font=('Inter', 26, 'bold'), bg_color='#000000', text_color='#FFFFFF')
            ScoreBoxLbl.place(relx=0.5, rely=0.1, anchor=customtkinter.N)

            #Returning the inital background to the caller where it will be placed.
            return BannerBackground

        #Specifically for this interface, a scrolling frame is needed as there could be many results that need to be displayed, if this was a normal frame the interface elements would be come far too small
        #Because of that, a scrolling frame is used to achieve similar sizing for each banner element. Positioned to be nearly as big as MainFrame, in the center
        ScrollingFrame = customtkinter.CTkScrollableFrame(self.MainFrame, width=Utils.RelXSize(0.9, self.MainFrame), height=Utils.RelYSize(0.8, self.MainFrame), corner_radius=12, bg_color='transparent')
        ScrollingFrame.place(relx=0.5, rely=0.975, anchor=customtkinter.S)

        #An invisible frame used for holding the text lables that act as headers for the value displayed in the scoreboard
        #This is placed just below the title of the page, but not attached to the scrolling frame to make it sticky to the top regardess of scrolled position
        HeaderFrame = customtkinter.CTkFrame(self.MainFrame, width=Utils.RelXSize(0.9, ScrollingFrame), height=Utils.RelYSize(0.0525, ScrollingFrame), fg_color='transparent', bg_color='transparent')
        HeaderFrame.place(relx=0.5, rely=0.0975, anchor=customtkinter.N)

        #For the header, 3 text lables are needed, 1 for each section of the scoreboard; place, team and score. Below each are instanced and palaced
        PlaceLbl = customtkinter.CTkLabel(HeaderFrame, width=Utils.RelXSize(0.175, HeaderFrame), height=(Utils.RelYSize(1, HeaderFrame)), text="Place", font=('Inter', 22, 'bold'))
        TeamLbl = customtkinter.CTkLabel(HeaderFrame, width=Utils.RelXSize(0.175, HeaderFrame), height=(Utils.RelYSize(1, HeaderFrame)), text="Team", font=('Inter', 22, 'bold'))
        ScoreLbl = customtkinter.CTkLabel(HeaderFrame, width=Utils.RelXSize(0.175, HeaderFrame), height=(Utils.RelYSize(1, HeaderFrame)), text="Score", font=('Inter', 22, 'bold'))

        PlaceLbl.place(relx=0, rely=0.5, anchor=customtkinter.W)
        TeamLbl.place(relx=0.4, rely=0.5, anchor=customtkinter.W)
        ScoreLbl.place(relx=1, rely=0.5, anchor=customtkinter.E)

        #Configuration of the main frame's title so that the user knows what page they have accessed
        self.MainFrameTitle.configure(text="Scoreboard")

        #This value is the amount of records to get from the database when it is queried 
        ScoreoardSize = 10 # TODO make this value the button the user clicks
        
        #Gets a list of team objects formed from the data gathered in the query 
        Scores = self.Connection.GetScores(ScoreoardSize)

        #Iteration over the list and the list index. For each element in the list a new UI element containing the teams score, team name and their place
        for Pos, Score in enumerate(Scores):
            #Parse the data to the generator function (Pos has 1 added to make it human formatted instead of computer formatted)
            ScoreUI = GenerateScoreBoardPanel(Score, Pos + 1)
            #Each UI is then adoorned to the scrolling frame. (place hasn't been used as it has issues with placemnt on scrolling frames)
            ScoreUI.pack(pady=25)

        #Now that the interface has been made, the older widgets can be destroyed
        for Widget in PurgeList:
            Widget.destroy()

    #Fucntion that switches the MainFrame to display the games that are played by the e-sports teams
    def SwitchToGamesDisplay(self):
        #Generating the list of UI elements to forget and delete later, making room for the updated UI
        PurgeList = self.FindItemsToPurge()

        #Given the GameID for a game, generate the scoreboard like display using the data from the database
        #GameID is the primary key in the database for games
        #Function is called when a game is clicked
        def DisplayTeamScoresForSpecificGameID(GameID : int):
            #Get a list of elements from the PopupFrame to be deleted, this allows the new UI to be generated properly
            OldIcons = self.FindItemsToPurge(PopUpFrame)

            #Using the database, generate a dictionary of team names and their current score, for the teams that play the given game
            TeamScoreDict = self.Connection.GetTeamAndScoresFromGameID(GameID)
            
            #As you can't do tri-variable loop, an external variable is needed to keep track of the index
            #Starts at 1 otherwise the first UI element would have no vertical padding
            Index = 1

            #Iterate over the dict of teams and their score. For each element in the dict, make a place for them on the pop up scoreboard
            for TeamName, Score in TeamScoreDict.items():
                #Making and palcing the background frame for the score-card
                Background = customtkinter.CTkFrame(PopUpFrame, width=Utils.RelXSize(0.8, PopUpFrame), height=Utils.RelYSize(0.15, PopUpFrame), corner_radius=12, fg_color='#3C3939')
                Background.place(relx=0.1, rely=(0.175 * Index), anchor=customtkinter.W)

                #The text label that shows the name of the team
                TeamNameLbl = customtkinter.CTkLabel(Background, width=Utils.RelXSize(0.5, Background), height=Utils.RelYSize(0.8, Background), text=TeamName, font=('Inter', 22, 'bold'))
                TeamNameLbl.place(relx=0.095, rely=0.5, anchor=customtkinter.W)

                #Decorative rounded box for the team's score
                ScoreValueBox = customtkinter.CTkFrame(Background, width=Utils.RelXSize(0.1, Background), height=Utils.RelYSize(0.8, Background))
                ScoreValueBox.place(relx=0.8, rely=0.5, anchor=customtkinter.E)
                
                #Text label placed within the rounded box, displaying the teams score
                ScoreValueBoxLbl = customtkinter.CTkLabel(ScoreValueBox, width=Utils.RelXSize(0.95,ScoreValueBox), height=Utils.RelYSize(0.95, ScoreValueBox), text=Score, font=('inter', 18, 'bold'))
                ScoreValueBoxLbl.place(relx=0.5, rely=0.05, anchor=customtkinter.N)

                #Now at the end of the loop, increment the index value by 1
                Index += 1

            #Now that the interface has been logically layed out, the root frame is placed to render it all at once
            PopUpFrame.place(relx=0.5, rely=0.3, anchor=customtkinter.N)

            #With the new UI in place, the old widgets can be deleted
            for widget in OldIcons:
                widget.destroy()

        #Function that makes the button for showing a game played by the teams. Also adds the binding to the above function
        def GenerateGameButton(Game : Game) -> customtkinter.CTkButton:
            GameBtn = customtkinter.CTkButton(ScrollingFrame, width=Utils.RelXSize(0.1), height=(Utils.RelYSize(0.1)), text=Game.Name, corner_radius=12, command=lambda: DisplayTeamScoresForSpecificGameID(Game.GameID), fg_color='#333333', hover_color='#111111', font=('inter', 18, 'bold'))

            return GameBtn

        #Configure the title text of MainFrame to inform users on the purpose of the data which the page displays
        self.MainFrameTitle.configure(text="Registered Games")

        #As there could be a myarid of games played, a scrolling frame is made to house all the buttons that will be made
        ScrollingFrame = customtkinter.CTkScrollableFrame(self.MainFrame, width=Utils.RelXSize(0.9, self.MainFrame), height=Utils.RelYSize(0.8, self.MainFrame), corner_radius=12, bg_color='transparent')
        ScrollingFrame.place(relx=0.5, rely=0.975, anchor=customtkinter.S)

        #As the game buttons needs to be interactable a pop-up is made ahead of time. it isn't placed yet as that is done on-the-fly when the score-cards are generated
        PopUpFrame = customtkinter.CTkFrame(self.MainFrame, width=Utils.RelXSize(0.725, ScrollingFrame), height=Utils.RelYSize(0.55, ScrollingFrame), corner_radius=24, fg_color='#111111', bg_color='transparent')

        #The frame needs a close button otherwise it would get in the way, so this is made for that purpose
        PopUpFrameClose = customtkinter.CTkButton(PopUpFrame, width=Utils.RelXSize(0.00175, PopUpFrame), height=Utils.RelYSize(0.035), text="X", font=('inter', 13, 'bold'), fg_color='#850101', hover_color='#252222', corner_radius=12, command=lambda:PopUpFrame.place_forget())
        PopUpFrameClose.place(relx=0.975, rely=0.03, anchor=customtkinter.NE)

        #Now that the main interface has been configured, the data can be collected from the database
        GamesPlayed = self.Connection.GetGamesPlayed()

        #Iteration over the list of game obejcts collected from the database
        #For each game object a UI button is made, pack is used becuase CTkScrollingFrame's do not seem to support .place()
        
        for Index, game in enumerate(GamesPlayed):
            UI = GenerateGameButton(game)
            UI.pack(padx=10, side='left', anchor=customtkinter.N)
       
       #Once the entire interface has been rendered, the old widgets can be destroyed for the new UI to take its place
        for Widget in PurgeList:
            Widget.destroy()

    #Function to un-render the children of a given widget, which are going to be deleted in order for new UI elements to be made
    def FindItemsToPurge(self, Widget : customtkinter.CTkBaseClass = None):
        #List of widgets to be deleted, returned at the end of the function
        ToBeDestroyed = []

        #As a class variable can't be the defualt for an argument, it is set here
        if Widget == None:
            Widget = self.MainFrame

        #Iterate over the children of the holding widget
        #Enumerate is used to get the index without needing an external variable
        #0 and 1 are ignored as 0 is the frame itself and 1 is the title
        for ChildIndex, Widget in enumerate(Widget.children.values()):
            if ChildIndex > 1:
                #Un-render the UI element and then add it to the list 
                Widget.place_forget()
                ToBeDestroyed.append(Widget)

        #Return the list of elements to be destroyed
        return ToBeDestroyed