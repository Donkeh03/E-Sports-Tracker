#Global Imports
import customtkinter # The main driver for the GUI app

#Local imports
import Utils# The utility class, holding functions and variables that are not class specific
from LoginPage import Login # The login page
from UserPage import UserPage # The default user page
from AdminPage import AdminPage # The higher access admin page 

#The main "driver" class. Initialises other pages and holds the function for switching pages
class MainView(customtkinter.CTk):
    #Init of the class. Makes a containter that holds all pages, and pre-init's other pages
    def __init__(self, *args, **kwargs):
        customtkinter.CTk.__init__(self, *args, **kwargs)

        #Creation of container frame for all "pages"
        Container = customtkinter.CTkFrame(self,width=Utils.X,height=Utils.Y)
        Container.pack(side = "top", fill = "both", expand = True) 
  
        Container.grid_rowconfigure(0, weight = 1)
        Container.grid_columnconfigure(0, weight = 1)

        #Creation of "frames" dictionary - Allows for pages to be swapped between using key index
        self.Frames =  {}
       
        #Generataion and pre-init of all app pages
        for Key, Page in {"login": Login, "userPage": UserPage, "adminPage": AdminPage}.items():
            Frame = Page(Container, self)
            self.Frames[Key] = Frame
            Frame.grid(row = 0, column = 0, sticky ="nsew")

        #On program start navigate to the login page
        self.ChangeDisplayedPage("login")
   
    #Core function for switching currently rendered page
    #Param frame: string. index variable for "Frames" dict
    def ChangeDisplayedPage(self, Frame : str):
        #In the event frame is none, return to prevent error. Print a debug statement
        if Frame is None:
             print("Error: No page parsed")
             return
        
        #Change rendered page to one parsed
        self.Frames[Frame].lift()

# Start of app functionality
# if not Utils.PreInitValidation():
#     Utils.Error("Unable to load app. Database inactive or missing theme config")

#customtkinter.set_default_color_theme('Theme.json')

App = MainView() # Init of the starting frame that is the root window

#Config of the main window
App.geometry(f"{Utils.Y}x{Utils.X}")
App.title("E-Sports App")

#Begin rendering of window
App.mainloop()