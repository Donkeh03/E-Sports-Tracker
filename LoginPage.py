#This class is the login page that a user is initally taken to when the app is loaded.
#This page has, 2 GUI buttons from which the user selects if they want to be a normal "user" (lower access) or admin (higher access, database access)

#Global imports
import customtkinter # Used for making the GUI

#Local imports
import Utils # Used for sizing UI elements relativley

class Login(customtkinter.CTkFrame):
    #Init of the page and it's widgets
    #Controller is a linkage to MainView's ChangeDisplayedPage method
    def __init__(self, Parent, Controller):
        customtkinter.CTkFrame.__init__(self, Parent, Utils.X, Utils.Y)
        
        # Control is set as a class level variable so that other methods within the class can utilise the page switch mechanic
        self.Control = Controller 

        #Construction of the title for the page
        LoginTitle = customtkinter.CTkLabel(self, text ="Login", font=('Roboto', 46, 'bold'), corner_radius=24, width=Utils.RelXSize(0.95), height=Utils.RelYSize(0.1))
        LoginTitle.place(relx=0.5, rely=0, anchor=customtkinter.N)

        #Getting the images to be used in the login buttons
        UserIcon = Utils.MakeCtkImageFromName("UserIcon.png", (100,100))
        AdminUserIcon = Utils.MakeCtkImageFromName("AdminUserIcon.png", (100,100))

        #Construction of the 2 buttons the user needs to press to access the system
        NonAdminLogin = customtkinter.CTkButton(self, text="User", image=UserIcon, corner_radius=26, width=Utils.RelXSize(0.35), height=Utils.RelYSize(0.25), command = lambda : self.Control.ChangeDisplayedPage("userPage"), fg_color='#191717',compound="top", font=('Inter', 30, 'bold'), hover_color='#252222')
        AdminLogin = customtkinter.CTkButton(self, text="Admin", image=AdminUserIcon, corner_radius=26, width=Utils.RelXSize(0.35), height=Utils.RelYSize(0.25), command = self.ActivateAdminLogin, fg_color='#191717', compound="top", font=('Inter', 30, 'bold'), hover_color='#252222')
       
        self.AdminPassword = customtkinter.CTkEntry(self, placeholder_text="Password...", corner_radius=24, width=Utils.RelXSize(0.25), height=Utils.RelYSize(0.05))

        #Placement of buttons on screen
        NonAdminLogin.place(relx=0.15, rely=0.5, anchor=customtkinter.W)
        AdminLogin.place(relx=0.85, rely=0.5, anchor=customtkinter.E)
        
        
    #Class method for activating the password input box on click of the Admin button
    def ActivateAdminLogin(self):
        self.AdminPassword.bind('<Return>', self.AdminLogin)
        self.AdminPassword.place(relx=0.825, rely=0.75, anchor=customtkinter.E)

    #Class method binding for the login event
    def AdminLogin(self, _):
        Password = self.AdminPassword.get()
        if Password == "test":
            self.Control.ChangeDisplayedPage("adminPage")