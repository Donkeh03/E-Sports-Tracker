#The admin page class is unlike the other pages as it gives the user (admin) direct access to the database wherein they can add, update and remove value as they desire though the user interface

import customtkinter # Used for making the GUI
import Utils # Used for a variety of things in the object
import DatabaseManager # Used to get data to be displayed
from Match import Match # Used for type declaration in a function
from Team import Team # Used for type declaration in a function
from Game import Game # Used for type delcaration in a function
from time import strptime # Used to validate the date input by a user

#AdminPage as a class is far more advanced as it deals with input from the user and manipulation of the database. As such more code is required to ensure saftey
class AdminPage(customtkinter.CTkFrame):
    def __init__(self, parent, controller): 
        customtkinter.CTkFrame.__init__(self, parent)
         
         #Making of the control and connection class level variables:
        # - Control used for page switching functionality
        # - Connection used for getting data from the database
        self.Control = controller
        self.Connection = DatabaseManager.DBManager()

        #The main navigation of this page - SideBar has 3 GUI buttons each show an admin a specific part of the database they can edit; matches, teams and games
        SideBar = customtkinter.CTkFrame(self, height=Utils.Y, width=Utils.RelXSize(0.095), fg_color='#000000')
        SideBar.place(relx=0, rely=0.5, anchor=customtkinter.W)
        
        #Creation and placing of the 3 GUI buttons for each 'sub-page'
        MatchBtnIcon = Utils.MakeCtkImageFromName("MatchIcon.png", (45,45))
        MatchesBtn = customtkinter.CTkButton(SideBar, text="", image=MatchBtnIcon, corner_radius=8, height=Utils.RelYSize(0.07, SideBar), width=Utils.RelXSize(0.75, SideBar), command=self.SwitchToMatchView, fg_color='#403939', hover_color='#252222')
        MatchesBtn.place(relx=0.5, rely=0.25, anchor=customtkinter.N)
       
        TeamsBtnIcon = Utils.MakeCtkImageFromName("TeamEditIcon.png", (45,45))
        TeamsBtn = customtkinter.CTkButton(SideBar, text="", image=TeamsBtnIcon, corner_radius=8, height=Utils.RelYSize(0.07, SideBar), width=Utils.RelXSize(0.75, SideBar), command=self.SwitchToTeamView, fg_color='#403939', hover_color='#252222')
        TeamsBtn.place(relx=0.5, rely=0.5, anchor=customtkinter.N)

        GameBtnIcon = Utils.MakeCtkImageFromName("GamesEditIcon.png", (45,45))
        GamesBtn = customtkinter.CTkButton(SideBar, text="", image=GameBtnIcon, corner_radius=8, height=Utils.RelYSize(0.07, SideBar), width=Utils.RelXSize(0.75, SideBar), command=self.SwitchToGameView, fg_color='#403939', hover_color='#252222')
        GamesBtn.place(relx=0.5, rely=0.75, anchor=customtkinter.N)

        #The main frame acts as a holding frame for the content that needs to be displayed (index 0 of main frame's children)
        self.MainFrame = customtkinter.CTkFrame(self, height=Utils.RelYSize(0.70), width=Utils.RelXSize(1.1), corner_radius=24, fg_color='#000000')
        self.MainFrame.place(relx=0.5325,rely=0.035, anchor=customtkinter.N)

        #The title for the frame, this contextualise the displayed data. (index 1 of main frame's children)
        self.MainFrameTitle = customtkinter.CTkLabel(self.MainFrame, height=Utils.RelYSize(0.15, self.MainFrame), width=Utils.RelXSize(0.75, self.MainFrame), font=('Inter', 40, 'bold'))
        self.MainFrameTitle.place(relx=0.15, rely=0.05, anchor=customtkinter.W)

        #At the end of the init, once the core UI has been made, call SwitchToMatchView. This is the page that should be loaded for the admin first
        self.SwitchToMatchView()

    #This method deals with loading all the matches in the database and configuring the UI to let an admin edit and add new matches to the database
    def SwitchToMatchView(self):
        #Like the UserPage, a list of items to be purged is made
        PurgeList = self.FindItemsToPurge()

        #Sub-function with the purpose of un-rendering the 'CRUDFrame' and removing any inputs from the entry boxes and clears the message label 
        def CloseCRUDWindow():
            #Un-rendering the frame
            CRUDFrame.place_forget()

            #Clearing the inputs of each entry box
            InputDateEntry.delete(0,len(InputDateEntry.get()))
            InputGameEntry.set('')
            InputTeam1Entry.set('')
            InputTeam2Entry.set('')
            InputTeam1ScoreEntry.delete(0,len(InputTeam1ScoreEntry.get()))
            InputTeam2ScoreEntry.delete(0,len(InputTeam2ScoreEntry.get()))

            #Clearing the text of message label
            MsgLbl.configure(text="")

        #Validation function for the match input boxes - feedback occurs via the message label. This function is also an intermediate step before the db call is made. A breakdown of checks done;
        #Initally the format of date is checked to be DD-MM-YYYY
        #Then both score boxes are check to contain integer values
        #Then the team names and game name selected are converted to their ID values
        #If all is well, either the update or create method is invoked depeding on MatchID parsed
        #(MatchID is parsed as the update function needs it for the WHERE clause. It is also used to determine if the user is making a new match or updating an existing one - as db primary keys start at 0)
        def ValidateInputBoxes(MatchID : int = -1):
            #Getting then checking the date input
            Date = InputDateEntry.get()

            #The check is in a try catch block otherwise errors arise i.e. blank inputs
            try:
                ValidDateFormat = strptime(Date,"%d-%m-%Y")
            except:
                DisplayMessageInColour("Date must be in DD-MM-YYYY format", '#850101')
                return

            #Getting then checking the team score values
            Team1Score = InputTeam1ScoreEntry.get()
            Team2Score = InputTeam2ScoreEntry.get()

            #Function attempts to type cast the string to an int - any character will cause an error and thus shouldn't be allowed
            if not Utils.IsStringInt(Team1Score) or not Utils.IsStringInt(Team2Score):
                DisplayMessageInColour("Please enter numbers for the team scores", '#850101')
                return

            #Getting and checking the team and game names
            Team1Name, Team2Name, GameName = InputTeam1Entry.get(), InputTeam2Entry.get() ,InputGameEntry.get()

            #If their length is 0, the user hasn't input a team/game yet
            if len(Team1Name) == 0 or len(Team2Name) == 0 or len(GameName) == 0:
                DisplayMessageInColour("Please input team names and game name", '#850101')
                return

            #Ensures that the teams playing are not the same team
            if Team1Name == Team2Name:
                DisplayMessageInColour("Teams cannot be the same!", '#850101')
                return

            #Varaible names are reused and overwritten as the database stores team/game names as their primary key index value
            #Because of this the values returned are actually integers
            #First variable is a boolean success
            ValidTeamNames, Team1Name, Team2Name = self.Connection.GetTeamIDFromTeamName(Team1Name, Team2Name)
            
            #If the query returns false (not successful) inform the user
            if not ValidTeamNames:
                DisplayMessageInColour("Invalid team names", '#850101')
                return
            
            ValidGameName, GameName = self.Connection.GetGameIDFromGameName(GameName)

            if not ValidGameName:
                DisplayMessageInColour("Invalid game name", '#850101')
                return
            
            #If all checks have been passed then compute the winning team with a ternary operator and call the relevant function with the user's inputted data
            if ValidDateFormat and Utils.IsStringInt(Team1Score) and Utils.IsStringInt(Team2Score) and ValidTeamNames and ValidGameName:
                WinningTeam = 1 if Team1Score < Team2Score else 0
                #If the matchID parsed is above 0 we know it's primary key is being used and so must need updating, else we are making a new record
                if MatchID > 0:
                    self.Connection.UpdateMatch(Match(MatchID, ValidDateFormat, Team1Name, Team2Name, GameName, WinningTeam, Team1Score, Team2Score))
                    DisplayMessageInColour("Match updated sucessfully", '#028A0F')
                else:
                    self.Connection.MakeNewMatch(ValidDateFormat, Team1Name, Team2Name, GameName, WinningTeam, Team1Score, Team2Score)
                    DisplayMessageInColour("Match added", '#028A0F')
            else:
                DisplayMessageInColour("Unable to find team/game name", '#850101')

        #Given an optional match object, configure the input display. If an object is parsed the populate the entry fields with the pre-existing data to be edited
        #By default assume none has been parsed, therefore only config the title's text and bind to validation function parsing none (as the record is to-be-made)
        def ConfigureInputDisplay(PreFillingData : Match = None) -> customtkinter.CTkFrame:
            #If there was an object parsed, config the entry boxes
            if PreFillingData:
                #Configure the title text
                CRUDTitle.configure(text='Update Match', font=('Inter', 40, 'bold'))

                #Insert the values from the object to the entry boxes 
                InputDateEntry.insert(0, Utils.ReverseDate(str(PreFillingData.Date))) # The date is stored as YYYY-MM-DD so needs to revered to DD-MM-YYYY for correctness
                InputGameEntry.set(PreFillingData.GamePlayed)
                InputTeam1Entry.set(PreFillingData.Team1)
                InputTeam2Entry.set(PreFillingData.Team2)
                InputTeam1ScoreEntry.insert(0, PreFillingData.Team1Score)
                InputTeam2ScoreEntry.insert(0, PreFillingData.Team2Score)

                #Binding of the submit button to the validation function
                SubmitBtn.configure(command=lambda : ValidateInputBoxes(PreFillingData.MatchID))
            else:
                #Cofigure text to be 'Add new match' opposed to 'update'
                CRUDTitle.configure(text='Make New Match', font=('Inter', 40, 'bold'))
                
                #Binding of the submit button the same validation method, but no parsing as this is for a record to-be-made
                SubmitBtn.configure(command=ValidateInputBoxes)
            
            #After the content of the frame has been config'ed. place the frame to make it visible to the user
            CRUDFrame.place(relx=0.5, rely=1, anchor=customtkinter.S)

        #A small almost utility funtion that takes a hex colour string and a message. This is how feedback of errors or succession is shown to the user
        def DisplayMessageInColour(Message : str, Colour : str):
            MsgLbl.configure(text=Message, text_color=Colour, font=('Inter', 26, 'bold'))

        #In the UserPage class, a more UI 'fancy' interface is employed, but here in the admin page, a more barebones UI is made that is more effective as display raw data
        #This function generates such a UI and retuns the root parent
        def GenerateCompactMatchDisplay(MatchData : Match) -> customtkinter.CTkFrame:
            #A narrow frame that holds all of the proceding UI elements
            BackgroundFrame = customtkinter.CTkFrame(ScrollingFrame, width=Utils.RelXSize(0.9, ScrollingFrame), height=Utils.RelYSize(0.15, ScrollingFrame), fg_color='#3C3939')

            #DateLbl is a text label which displays the date of the match. Positioned in the lower left corner of the background
            dateLbl = customtkinter.CTkLabel(BackgroundFrame, text=MatchData.Date, width=Utils.RelXSize(0.15, BackgroundFrame), height=Utils.RelYSize(0.255, BackgroundFrame), font=('inter', 17, 'bold'))
            dateLbl.place(relx=0.185, rely=0.65, anchor=customtkinter.N)

            #GameLbl is a text label that shows the name of the game which was played. Positon vertically above the date in a bigger font
            gameLbl = customtkinter.CTkLabel(BackgroundFrame, text=MatchData.GamePlayed, width=Utils.RelXSize(0.3, BackgroundFrame), height=Utils.RelYSize(0.3, BackgroundFrame), font=('inter', 23, 'bold'))
            gameLbl.place(relx=0.185, rely=0.075, anchor=customtkinter.N)

            #Team1Lbl is a text label showing the name of team 1
            Team1Lbl = customtkinter.CTkLabel(BackgroundFrame, text=MatchData.Team1, width=Utils.RelXSize(0.1, BackgroundFrame), height=Utils.RelYSize(0.205, BackgroundFrame), font=('inter', 16, 'bold'))
            Team1Lbl.place(relx=0.445, rely=0.4, anchor=customtkinter.S)

            #Team2Lbl is a text label showing the name of team 2
            Team2Lbl = customtkinter.CTkLabel(BackgroundFrame, text=MatchData.Team2, width=Utils.RelXSize(0.1, BackgroundFrame), height=Utils.RelYSize(0.205, BackgroundFrame), font=('inter', 16, 'bold'))
            Team2Lbl.place(relx=0.445, rely=0.6, anchor=customtkinter.N)

            #Team1ScoreLbl is a text label showing the score of team 1
            Team1ScoreLbl = customtkinter.CTkLabel(BackgroundFrame, text=MatchData.Team1Score, width=Utils.RelXSize(0.05, BackgroundFrame), height=Utils.RelYSize(0.205, BackgroundFrame), font=('inter', 16, 'bold'))
            Team1ScoreLbl.place(relx=0.575, rely=0.4, anchor=customtkinter.S)

            #Team2ScoreLbl is a text label showing the score of team 2
            Team2ScoreLbl = customtkinter.CTkLabel(BackgroundFrame, text=MatchData.Team2Score, width=Utils.RelXSize(0.05, BackgroundFrame), height=Utils.RelYSize(0.205, BackgroundFrame), font=('inter', 16, 'bold'))
            Team2ScoreLbl.place(relx=0.575, rely=0.6, anchor=customtkinter.N)

            #This button is used for accessing the edit popup for the record being displayed
            EditButton = customtkinter.CTkButton(BackgroundFrame, width=Utils.RelXSize(0.2, BackgroundFrame), height=Utils.RelYSize(0.4, BackgroundFrame), text='Edit', fg_color='#191919', font=('inter', 20, 'bold'), command=lambda : ConfigureInputDisplay(MatchData))
            EditButton.place(relx=0.95, rely=0.5, anchor=customtkinter.E)

            #Returning of the root frame to caller
            return BackgroundFrame

        #The first step of the function is to configure the text of the title so that it matches the content that is about to be displayed on it
        self.MainFrameTitle.configure(text="Manage Matches")
        
        #Button in the top corner of the main frame that opens the popup for adding a new match
        AddMatchButton = customtkinter.CTkButton(self.MainFrame, width=Utils.RelXSize(0.155), height=Utils.RelYSize(0.055), text="Add Match", command=ConfigureInputDisplay, fg_color='#3E3E3E', font=('Inter', 18, 'bold'))
        AddMatchButton.place(relx=0.95, rely=0.05, anchor=customtkinter.E)

        #Placement of the frame that will hold of the matches
        ScrollingFrame = customtkinter.CTkScrollableFrame(self.MainFrame, width=Utils.RelXSize(0.9, self.MainFrame), height=Utils.RelYSize(0.8, self.MainFrame), corner_radius=12, bg_color='transparent')
        ScrollingFrame.place(relx=0.5, rely=0.975, anchor=customtkinter.S)

        #A frame that holds the input boxes for either a new match or updating a match
        CRUDFrame = customtkinter.CTkFrame(self.MainFrame, width=Utils.RelXSize(1.125, ScrollingFrame), height=Utils.RelYSize(1.2501, ScrollingFrame), corner_radius=22, fg_color='#262626')
        
        #The title of the frame, changes depending on if the user is updating or making a new match
        CRUDTitle = customtkinter.CTkLabel(CRUDFrame, width=Utils.RelXSize(0.5, CRUDFrame), height=Utils.RelYSize(0.1, CRUDFrame))
        CRUDTitle.place(relx=0.5, rely=0.025, anchor=customtkinter.N)

        #The close button for the crud frme
        PopUpFrameClose = customtkinter.CTkButton(CRUDFrame, width=Utils.RelXSize(0.00175, CRUDFrame), height=Utils.RelYSize(0.035), text="X", font=('inter', 13, 'bold'), fg_color='#850101', hover_color='#252222', corner_radius=12, command=CloseCRUDWindow)
        PopUpFrameClose.place(relx=0.975, rely=0.03, anchor=customtkinter.NE)

        #Making the date entry box and label for the box to provide context. Then placing them on the interface
        InputDateLbl = customtkinter.CTkLabel(CRUDFrame, width=Utils.RelXSize(0.20, CRUDFrame), height=Utils.RelYSize(0.075,CRUDFrame), text='Input Date:', font=('inter', 22, 'bold'))
        InputDateEntry = customtkinter.CTkEntry(CRUDFrame, width=Utils.RelXSize(0.295, CRUDFrame), height=Utils.RelYSize(0.055,CRUDFrame), placeholder_text='DD-MM-YYYY')

        InputDateLbl.place(relx=0.05, rely=0.2, anchor=customtkinter.W)
        InputDateEntry.place(relx=0.05, rely=0.3, anchor=customtkinter.W)

        #Making the game entry box and label for the box to provide context. Then placing them on the interface
        InputGameLbl = customtkinter.CTkLabel(CRUDFrame, width=Utils.RelXSize(0.20, CRUDFrame), height=Utils.RelYSize(0.075,CRUDFrame), text='Input Game:', font=('inter', 22, 'bold'))
        InputGameEntry = customtkinter.CTkComboBox(CRUDFrame, width=Utils.RelXSize(0.295, CRUDFrame), height=Utils.RelYSize(0.055,CRUDFrame), values=self.Connection.GetAllRegisteredGameNames(), dropdown_font=('inter', 16, 'normal'), state='readonly')

        InputGameLbl.place(relx=0.95, rely=0.2, anchor=customtkinter.E)
        InputGameEntry.place(relx=0.95, rely=0.3, anchor=customtkinter.E)

        #Making the team 1 and 2 entry boxes and labels for them to provide context. Then placing them on the interface
        TeamNames = self.Connection.GetAllRegisteredTeamNames()
        InputTeam1Lbl = customtkinter.CTkLabel(CRUDFrame, width=Utils.RelXSize(0.20, CRUDFrame), height=Utils.RelYSize(0.075,CRUDFrame), text='Input Team 1:', font=('inter', 22, 'bold'))
        InputTeam1Entry = customtkinter.CTkComboBox(CRUDFrame, width=Utils.RelXSize(0.295, CRUDFrame), height=Utils.RelYSize(0.055,CRUDFrame), values=TeamNames, state='readonly', dropdown_font=('inter', 16, 'normal'))

        InputTeam2Lbl = customtkinter.CTkLabel(CRUDFrame, width=Utils.RelXSize(0.20, CRUDFrame), height=Utils.RelYSize(0.075,CRUDFrame), text='Input Team 2:', font=('inter', 22, 'bold'))
        InputTeam2Entry = customtkinter.CTkComboBox(CRUDFrame, width=Utils.RelXSize(0.295, CRUDFrame), height=Utils.RelYSize(0.055,CRUDFrame), values=TeamNames, state='readonly', dropdown_font=('inter', 16, 'normal'))

        InputTeam1Lbl.place(relx=0.25, rely=0.4, anchor=customtkinter.E)
        InputTeam1Entry.place(relx=0.35, rely=0.5, anchor=customtkinter.E)

        InputTeam2Lbl.place(relx=0.25, rely=0.575, anchor=customtkinter.E)
        InputTeam2Entry.place(relx=0.35, rely=0.675, anchor=customtkinter.E)

        #Making the score entry boxes and labels for them to provide context. Then placing them on the interface
        InputTeam1ScoreLbl = customtkinter.CTkLabel(CRUDFrame, width=Utils.RelXSize(0.20, CRUDFrame), height=Utils.RelYSize(0.075,CRUDFrame), text='Input Team 1 Score:', font=('inter', 22, 'bold'))
        InputTeam1ScoreEntry = customtkinter.CTkEntry(CRUDFrame, width=Utils.RelXSize(0.1, CRUDFrame), height=Utils.RelYSize(0.055,CRUDFrame), placeholder_text='-')

        InputTeam2ScoreLbl = customtkinter.CTkLabel(CRUDFrame, width=Utils.RelXSize(0.20, CRUDFrame), height=Utils.RelYSize(0.075,CRUDFrame), text='Input Team 2 Score:', font=('inter', 22, 'bold'))
        InputTeam2ScoreEntry = customtkinter.CTkEntry(CRUDFrame, width=Utils.RelXSize(0.1, CRUDFrame), height=Utils.RelYSize(0.055,CRUDFrame), placeholder_text='-')

        InputTeam1ScoreLbl.place(relx=0.675, rely=0.4, anchor=customtkinter.W)
        InputTeam1ScoreEntry.place(relx=0.755, rely=0.5, anchor=customtkinter.W)

        InputTeam2ScoreLbl.place(relx=0.675, rely=0.575, anchor=customtkinter.W)
        InputTeam2ScoreEntry.place(relx=0.755, rely=0.675, anchor=customtkinter.W)

        #Making the message label, which sits at the bottom of the interface - used for displaying feedback to the user
        MsgLbl = customtkinter.CTkLabel(CRUDFrame, width=Utils.RelXSize(0.85), height=Utils.RelYSize(0.075), fg_color='transparent', text="")
        MsgLbl.place(relx=0.5, rely=1, anchor=customtkinter.S)

        #Making a large button that the user can click to submit the data inputted to the database
        #This is bound to the validation function which makes an internal call to update or delete
        SubmitBtn = customtkinter.CTkButton(CRUDFrame, width=Utils.RelXSize(0.25, CRUDFrame), height=Utils.RelYSize(0.075, CRUDFrame), text='Submit', font=('Inter', 26, 'bold'), corner_radius=24)
        SubmitBtn.place(relx=0.5, rely=0.75, anchor=customtkinter.N)

        #Now that the interface has been constructed - the match data can be collected
        MatchData = self.Connection.GetMostRecentMatches(100)

        #Iteration over the match data, for each match in the list a user interface is made and ocnfigured, before it is placed within the scrolling frame
        for match in MatchData:
            UI = GenerateCompactMatchDisplay(match)
            UI.pack(pady=15)

        #As the interface has been completely done, the purge list can be interated over and destroyed
        for Widget in PurgeList:
            Widget.destroy()

    #This method deals with loading all the teams in the database and configuring the UI to let an admin edit and add new teams to the database
    def SwitchToTeamView(self):
        #Like the UserPage, a list of items to be purged is made
        PurgeList = self.FindItemsToPurge()

        #This function validates the team name, score, registration and game name values to ensure they can be parsed to the database without causing issues
        #First the name is checked to be more than 0 chars (empty) and less than 20
        #Second the team score is checked to be an integer value
        #Then, the registeration box is check to ensure it's state is either 0 or 1
        #Finally the game name input is checked to be within the games table, then db calls are made
        def ValidateTeamNameAndScore(TeamID : int = -1):
            #Getting the team name
            TeamName = TeamNameEntry.get()

            #Checking the team names length is above min and less than max
            if len(TeamName) <= 0:
                DisplayMessageInColour("Name cannot be empty!", '#850101')
                return
            elif len(TeamName) > 20:
                DisplayMessageInColour("Name is too long, must be less than 20 chars", '#850101')
                return

            #Getting the team score
            TeamScore = TeamScoreEntry.get()

            #Ensuring input is in fact an integer
            if not Utils.IsStringInt(TeamScore):
                DisplayMessageInColour("Score must be a number", '#850101')
                return

            #Getting the registeration value
            IsRegistered = TeamRegVar.get()

            #Ensuring its state is  0 or 1 and nothing else
            #!= cant be used as for some reason the if logic breaks
            if IsRegistered == 0 or IsRegistered == 1:
                pass
            else:
                DisplayMessageInColour("Team must be registered or not!", '#850101')
                return

            #Getting the team name
            TeamGame = TeamGameEntry.get()

            #Determine if the input is valid and convert it to the corrosponding ID
            IsTeamGameValid, TeamGame = self.Connection.GetGameIDFromGameName(TeamGame)

            #If game name isn't valid, output an error
            if not IsTeamGameValid:
                DisplayMessageInColour("Invalid team game", '#850101')
                return
            
            #If team ID is more than -1 then we want to update the record in the database, if it is -1 then we want to make a new record
            if TeamID > -1:
                #Parse inputted values as a team object to the update function
                self.Connection.UpdateTeam(Team(TeamID, TeamName, IsRegistered, int(TeamScore), TeamGame))
                DisplayMessageInColour("Updated Team", '#028A0F')
            else:
                #Parse input values to make new function as single params (team object can't be formed as id is missing)
                self.Connection.MakeNewTeam(TeamName, TeamScore, IsRegistered, TeamGame)
                DisplayMessageInColour("Team Succesfully Registered", '#028A0F')
            
        #A small almost utility funtion that takes a hex colour string and a message. This is how feedback of errors or succession is shown to the user
        def DisplayMessageInColour(Message : str, Colour : str):
            MessageLbl.configure(text=Message, text_color=Colour, font=('Inter', 26, 'bold'))
        
        #This function configures the input frames children. If a team object is parsed, then it will pre-fill all the input boxes, if not just config the submit button
        def ConfigureInputFrame(team : Team = None):
            #If the team parsed is not none, pre-fill the input boxes
            if team:
                InputFrameTitle.configure(text='Edit Team')
                TeamNameEntry.insert(0,team.TeamName)
                TeamScoreEntry.insert(0,team.Score)
                SubmitBtn.configure(command=lambda : ValidateTeamNameAndScore(team.TeamID))
                TeamRegYes.select() if team.IsRegistered == 1 else TeamRegNo.select()
                TeamGameEntry.set(self.Connection.GetGameNameFromGameID(team.Game))
            else:# Else just leave the input boxes alone
                InputFrameTitle.configure(text='Create Team')
                SubmitBtn.configure(command=ValidateTeamNameAndScore)
                TeamRegYes.select()

            #Once the input frame is configed place it on the interface to make it visible to the user
            InputFrame.place(relx=0.5, rely=1, anchor=customtkinter.S)

        #This function is bound to the small 'X' on the input frame. It also clears all current inputs and resets the frame to its inital state
        def CloseInputFrame():
            #Remove the frame from being rendered
            InputFrame.place_forget()

            #Clear all the input box values
            TeamNameEntry.delete(0,len(TeamNameEntry.get()))
            TeamScoreEntry.delete(0,len(TeamScoreEntry.get()))
            TeamGameEntry.set('')

            #Clear the message labels text
            MessageLbl.configure(text='')

            #Reset the reg radio buttons
            TeamRegNo.deselect()
            TeamRegYes.deselect()

        #Given a team object, generate a banner to hold its data. Also provides the access for user's to edit a specific record
        def GenerateTeamBanner(team : Team) -> customtkinter.CTkFrame:
            #A narrow frame that holds all of the proceding UI elements
            BackgroundFrame = customtkinter.CTkFrame(ScrollingFrame, width=Utils.RelXSize(0.9, ScrollingFrame), height=Utils.RelYSize(0.15, ScrollingFrame), fg_color=('#3C3939' if team.IsRegistered else '#292929'))

            #Text label to display the name of the team
            TeamName = customtkinter.CTkLabel(BackgroundFrame, width=Utils.RelXSize(0.3,BackgroundFrame), height=Utils.RelYSize(0.8,0), text=team.TeamName, font=('inter', 32, 'bold'))
            TeamName.place(relx=0.1, rely=0.5, anchor=customtkinter.W)

            #Visual box and text label to display the score of the team
            TeamScoreBox = customtkinter.CTkFrame(BackgroundFrame, width=Utils.RelXSize(0.075, BackgroundFrame), height=Utils.RelYSize(0.55, BackgroundFrame), corner_radius=12, fg_color='#000000')
            TeamScoreBoxLbl = customtkinter.CTkLabel(TeamScoreBox, width=Utils.RelXSize(0.75, TeamScoreBox), height=Utils.RelYSize(0.75, TeamScoreBox), text=team.Score, font=('inter', 22, 'bold'))

            #Placement of elements on banner
            TeamScoreBox.place(relx=0.55, rely=0.2, anchor=customtkinter.N)
            TeamScoreBoxLbl.place(relx=0.5, rely=0.1, anchor=customtkinter.N)

            #This button is used for accessing the edit popup for the record being displayed
            EditButton = customtkinter.CTkButton(BackgroundFrame, width=Utils.RelXSize(0.2, BackgroundFrame), height=Utils.RelYSize(0.4, BackgroundFrame), text='Edit', fg_color='#191919', font=('inter', 20, 'bold'), command=lambda:ConfigureInputFrame(team))
            EditButton.place(relx=0.95, rely=0.5, anchor=customtkinter.E)

            #Return fully made frame to the caller
            return BackgroundFrame

        #The first step of the function is to configure the text of the title so that it matches the content that is about to be displayed on it
        self.MainFrameTitle.configure(text="Manage Teams")

        #Placement of the frame that will hold of the teams
        ScrollingFrame = customtkinter.CTkScrollableFrame(self.MainFrame, width=Utils.RelXSize(0.9, self.MainFrame), height=Utils.RelYSize(0.8, self.MainFrame), corner_radius=12, bg_color='transparent')
        ScrollingFrame.place(relx=0.5, rely=0.975, anchor=customtkinter.S)

        #Button in the top corner of the main frame that opens the popup for registering a new team
        AddTeamButton = customtkinter.CTkButton(self.MainFrame, width=Utils.RelXSize(0.155), height=Utils.RelYSize(0.055), text="Add Team", fg_color='#3E3E3E', font=('Inter', 18, 'bold'), command=ConfigureInputFrame)
        AddTeamButton.place(relx=0.95, rely=0.05, anchor=customtkinter.E)

        #A frame that holds the input boxes for either a new team or updating a team
        InputFrame = customtkinter.CTkFrame(self.MainFrame, width=Utils.RelXSize(1.125, ScrollingFrame), height=Utils.RelYSize(1.2501, ScrollingFrame), corner_radius=22, fg_color='#262626')
        
        #The title of the frame, changes depending on if the user is updating or making a new team
        InputFrameTitle = customtkinter.CTkLabel(InputFrame, width=Utils.RelXSize(0.5, InputFrame), height=Utils.RelYSize(0.1, InputFrame), text='', font=('Inter', 30, 'bold'))
        InputFrameTitle.place(relx=0.5, rely=0.025, anchor=customtkinter.N)

        #The close button for the input frme
        PopUpFrameClose = customtkinter.CTkButton(InputFrame, width=Utils.RelXSize(0.00175, InputFrame), height=Utils.RelYSize(0.035), text="X", font=('inter', 13, 'bold'), fg_color='#850101', hover_color='#252222', corner_radius=12, command=CloseInputFrame)
        PopUpFrameClose.place(relx=0.975, rely=0.03, anchor=customtkinter.NE)

        #The title and text entry for the name of the team
        TeamNameTitle = customtkinter.CTkLabel(InputFrame, width=Utils.RelXSize(0.35, InputFrame), height=Utils.RelYSize(0.075, InputFrame), text="Input Team Name:", font=('inter', 28, 'bold'))
        TeamNameEntry = customtkinter.CTkEntry(InputFrame, width=Utils.RelXSize(0.325, InputFrame), height=Utils.RelYSize(0.075, InputFrame), placeholder_text='Team Name')

        TeamNameTitle.place(relx=0.025, rely=0.25, anchor=customtkinter.W)
        TeamNameEntry.place(relx=0.055, rely=0.325, anchor=customtkinter.W)

        #Title and text input for the name of the game that the team plays
        TeamGameLbl = customtkinter.CTkLabel(InputFrame, width=Utils.RelXSize(0.35, InputFrame), height=Utils.RelYSize(0.075, InputFrame), text="Input Team Game:", font=('inter', 28, 'bold'))
        TeamGameEntry = customtkinter.CTkComboBox(InputFrame, width=Utils.RelXSize(0.275, InputFrame), height=Utils.RelYSize(0.075, InputFrame), values=self.Connection.GetAllRegisteredGameNames(),dropdown_font=('Inter', 18, 'normal'), state='readonly')
        
        TeamGameLbl.place(relx=0.975, rely=0.25, anchor=customtkinter.E)
        TeamGameEntry.place(relx=0.955, rely=0.325, anchor=customtkinter.E)

        #Title and text input for the score of the team
        TeamScoreLbl = customtkinter.CTkLabel(InputFrame, width=Utils.RelXSize(0.35, InputFrame), height=Utils.RelYSize(0.075, InputFrame), text="Input Team Score:", font=('inter', 28, 'bold'))
        TeamScoreEntry = customtkinter.CTkEntry(InputFrame, width=Utils.RelXSize(0.2, InputFrame), height=Utils.RelYSize(0.055, InputFrame), placeholder_text='-')

        TeamScoreLbl.place(relx=0.025, rely=0.5, anchor=customtkinter.W)
        TeamScoreEntry.place(relx=0.05, rely=0.555, anchor=customtkinter.W)

        #Label, variable, yes and no buttons for the selection of if the team is registered or not
        TeamRegLbl = customtkinter.CTkLabel(InputFrame, width=Utils.RelXSize(0.35, InputFrame), height=Utils.RelYSize(0.075, InputFrame), text="Registered:", font=('inter', 28, 'bold'))
        TeamRegVar = customtkinter.IntVar(value=0)
        TeamRegYes = customtkinter.CTkRadioButton(InputFrame, text='Yes', variable=TeamRegVar, value=1)
        TeamRegNo = customtkinter.CTkRadioButton(InputFrame, text='No', variable=TeamRegVar, value=0)

        TeamRegLbl.place(relx=0.975, rely=0.5, anchor=customtkinter.E)
        TeamRegYes.place(relx=0.855, rely=0.555, anchor=customtkinter.E)
        TeamRegNo.place(relx=0.965, rely=0.555, anchor=customtkinter.E)

        #The button that submits the data to the validation function, and to the database (if acceptable)
        SubmitBtn = customtkinter.CTkButton(InputFrame, width=Utils.RelXSize(0.25, InputFrame), height=Utils.RelYSize(0.075 ,InputFrame), text='Submit', font=('Inter', 26, 'bold'), corner_radius=24)
        SubmitBtn.place(relx=0.5, rely=0.75, anchor=customtkinter.N)

        #A text label that displays messages to the user (mainly error/success statements)
        MessageLbl = customtkinter.CTkLabel(InputFrame, text='', width=Utils.RelXSize(0.75, InputFrame), height=Utils.RelYSize(0.075))
        MessageLbl.place(relx=0.5, rely=0.95, anchor=customtkinter.S)

        #Get a list of all the teams registered first then un-registered
        Teams = self.Connection.GetTeamsSortedByRegistered()

        #Iterate over each team and make an interface element for them, then place it on the scrolling frame
        for team in Teams:
            UI = GenerateTeamBanner(team)
            UI.pack(pady=15)

        #As the interface has been completely done, the purge list can be interated over and destroyed
        for Widget in PurgeList:
            Widget.destroy()

    #This method deals with loading all the games in the database and configuring the UI to let an admin edit and add new games to the database
    def SwitchToGameView(self):
        #Like the UserPage, a list of items to be purged is made
        PurgeList = self.FindItemsToPurge()

        #A small almost utility funtion that takes a hex colour string and a message. This is how feedback of errors or succession is shown to the user
        def DisplayMessageInColour(Message : str, Colour : str):
            MessageLbl.configure(text=Message, text_color=Colour, font=('Inter', 26, 'bold'))

        #When the submit button is clicked, validate the registered state and that the game name input isnt too long or empty
        #If the inputs are valid, make the correct database call to either update or insert new record
        def ProcessSubmitClick(GameID : int = -1):
            GameName = GameNameEntry.get()

            if len(GameName) <= 0:
                DisplayMessageInColour("Name cannot be empty!", '#850101')
                return
            elif len(GameName) > 20:
                DisplayMessageInColour("Name is too long!", '#850101')
                return
            
            IsRegistered = GameRegVar.get()

            if IsRegistered == 0 or IsRegistered == 1:
                pass
            else:
                DisplayMessageInColour("Team must be registered or not!", '#850101')
                return

            if GameID > -1:
                self.Connection.UpdateGame(Game(GameID, GameName, IsRegistered))
                DisplayMessageInColour("Successfully Update Game", '#028A0F')
                return
            else:
                self.Connection.MakeNewGame(GameName, IsRegistered)
                DisplayMessageInColour("Successfully Created Game", '#028A0F')
                return

        #Configuration of the input frame, if a game is parsed then pre-configure the input frame with its values, if not then just configure the submit and title text
        def ConfigureInputFrame(Game : Game = None):
            if Game:
                InputFrameTitle.configure(text='Edit Game')
                GameNameEntry.insert(0,Game.Name)
                SubmitBtn.configure(command=lambda : ProcessSubmitClick(Game.GameID))
                GameRegYes.select() if Game.IsRegistered == 1 else GameRegNo.select()
            else:
                InputFrameTitle.configure(text='Create Game')
                SubmitBtn.configure(command=ProcessSubmitClick)
                GameRegYes.select()

            InputFrame.place(relx=0.5, rely=1, anchor=customtkinter.S)

        #When the input frames close button is clicked, remove all currently input data and clear the message label
        def CloseInputFrame():
            InputFrame.place_forget()

            GameNameEntry.delete(0,len(GameNameEntry.get()))
            MessageLbl.configure(text='')
            GameRegNo.deselect()
            GameRegYes.deselect()

        #Given a game object, generate a banner to display its data to the admin, also gives them the ability to edit it's data
        def GenerateGameBanner(Game : Game):
            #A narrow frame that holds all of the proceding UI elements
            BackgroundFrame = customtkinter.CTkFrame(ScrollingFrame, width=Utils.RelXSize(0.9, ScrollingFrame), height=Utils.RelYSize(0.15, ScrollingFrame), fg_color=('#3C3939' if Game.IsRegistered else '#292929'))

            #Text label displaying the name of the game
            GameName = customtkinter.CTkLabel(BackgroundFrame, width=Utils.RelXSize(0.3,BackgroundFrame), height=Utils.RelYSize(0.8,0), text=Game.Name, font=('inter', 32, 'bold'))
            GameName.place(relx=0.1, rely=0.5, anchor=customtkinter.W)

            #This button is used for accessing the edit popup for the record being displayed
            EditButton = customtkinter.CTkButton(BackgroundFrame, width=Utils.RelXSize(0.2, BackgroundFrame), height=Utils.RelYSize(0.4, BackgroundFrame), text='Edit', fg_color='#191919', font=('inter', 20, 'bold'), command=lambda:ConfigureInputFrame(Game))
            EditButton.place(relx=0.95, rely=0.5, anchor=customtkinter.E)

            return BackgroundFrame

        #The first step of the function is to configure the text of the title so that it matches the content that is about to be displayed on it
        self.MainFrameTitle.configure(text="Manage Games")

        #Placement of the frame that will hold of the teams
        ScrollingFrame = customtkinter.CTkScrollableFrame(self.MainFrame, width=Utils.RelXSize(0.9, self.MainFrame), height=Utils.RelYSize(0.8, self.MainFrame), corner_radius=12, bg_color='transparent')
        ScrollingFrame.place(relx=0.5, rely=0.975, anchor=customtkinter.S)

        #Button in the top corner of the main frame that opens the popup for registering a new game
        AddGameButton = customtkinter.CTkButton(self.MainFrame, width=Utils.RelXSize(0.155), height=Utils.RelYSize(0.055), text="Add Game", fg_color='#3E3E3E', font=('Inter', 18, 'bold'), command=ConfigureInputFrame)
        AddGameButton.place(relx=0.95, rely=0.05, anchor=customtkinter.E)

        #A frame that holds the input boxes for either a new game or updating a game
        InputFrame = customtkinter.CTkFrame(self.MainFrame, width=Utils.RelXSize(1.125, ScrollingFrame), height=Utils.RelYSize(1.2501, ScrollingFrame), corner_radius=22, fg_color='#262626')
        
        #The title of the frame, changes depending on if the user is updating or making a new game
        InputFrameTitle = customtkinter.CTkLabel(InputFrame, width=Utils.RelXSize(0.5, InputFrame), height=Utils.RelYSize(0.1, InputFrame), text='', font=('Inter', 30, 'bold'))
        InputFrameTitle.place(relx=0.5, rely=0.025, anchor=customtkinter.N)

        #The close button for the input frme
        PopUpFrameClose = customtkinter.CTkButton(InputFrame, width=Utils.RelXSize(0.00175, InputFrame), height=Utils.RelYSize(0.035), text="X", font=('inter', 13, 'bold'), fg_color='#850101', hover_color='#252222', corner_radius=12, command=CloseInputFrame)
        PopUpFrameClose.place(relx=0.975, rely=0.03, anchor=customtkinter.NE)

        #Text input and title for the game name input
        GameNameTitle = customtkinter.CTkLabel(InputFrame, width=Utils.RelXSize(0.35, InputFrame), height=Utils.RelYSize(0.075, InputFrame), text="Input Game Name:", font=('inter', 28, 'bold'))
        GameNameEntry = customtkinter.CTkEntry(InputFrame, width=Utils.RelXSize(0.325, InputFrame), height=Utils.RelYSize(0.075, InputFrame), placeholder_text='Game Name')

        GameNameTitle.place(relx=0.025, rely=0.49, anchor=customtkinter.W)
        GameNameEntry.place(relx=0.055, rely=0.555, anchor=customtkinter.W)

        #The title. varible and radio buttons for the registered state of a game
        GameRegLbl = customtkinter.CTkLabel(InputFrame, width=Utils.RelXSize(0.35, InputFrame), height=Utils.RelYSize(0.075, InputFrame), text="Registered:", font=('inter', 28, 'bold'))
        GameRegVar = customtkinter.IntVar(value=0)
        GameRegYes = customtkinter.CTkRadioButton(InputFrame, text='Yes', variable=GameRegVar, value=1)
        GameRegNo = customtkinter.CTkRadioButton(InputFrame, text='No', variable=GameRegVar, value=0)

        GameRegLbl.place(relx=0.975, rely=0.49, anchor=customtkinter.E)
        GameRegYes.place(relx=0.855, rely=0.555, anchor=customtkinter.E)
        GameRegNo.place(relx=0.965, rely=0.555, anchor=customtkinter.E)

        #The button at the bottom of the input frame which lets the user submit the inputted data to the database, once going thorugh the process validations
        SubmitBtn = customtkinter.CTkButton(InputFrame, width=Utils.RelXSize(0.25, InputFrame), height=Utils.RelYSize(0.075 ,InputFrame), text='Submit', font=('Inter', 26, 'bold'), corner_radius=24)
        SubmitBtn.place(relx=0.5, rely=0.75, anchor=customtkinter.N)

        #Text label below the submit button, used for displaying messages, typically error or success, to the user
        MessageLbl = customtkinter.CTkLabel(InputFrame, text='', width=Utils.RelXSize(0.75, InputFrame), height=Utils.RelYSize(0.075))
        MessageLbl.place(relx=0.5, rely=0.95, anchor=customtkinter.S)

        #Get a list of game objects from the database, False is parsed as we want to ignore the IsRegistered only check and get all games, ordered by registration
        Games = self.Connection.GetGamesPlayed(False)

        #Iterate over the game objects and make a UI element for each one, which is then placed on the interface
        for game in Games:
            UI = GenerateGameBanner(game)
            UI.pack(pady=15)

        #As the interface has been completely done, the purge list can be interated over and destroyed
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