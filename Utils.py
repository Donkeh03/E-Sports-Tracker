#Utility class holding myarid functions and variables

import customtkinter # Used for doing type declaration in functions
import os # Used for file pathing to file e.g. theme.json
import DatabaseManager # Used to make a bare instance of the class, which ensures database is active
import ctypes # Used as the gateway to the error message function
from PIL import Image # Used for reading in images

X, Y = 768, 1024 # The size of the window in pixels
ImageDir = os.path.join(os.getcwd(), "Images") # The basefile path for accessing images
# Global utility functions

# Given a float 'decimal' (0.00-1.00) return the size an object should be, relative to the root window size or another widget
def RelXSize(decimal : float, Window : customtkinter.CTkBaseClass = None):
    if Window:
        #print(f"Obj: {Window.widgetName}:: Size(w): {Window._current_width}")
        return int(decimal * Window._desired_width)
    else:
        #print(f"Obj: None:: Size(w): {int(decimal * X)}")
        return int(decimal * X)

def RelYSize(decimal: float, Window : customtkinter.CTkBaseClass = None):
    if Window:
        #print(f"Obj: {Window.widgetName}:: Size (h): {Window._current_height}")
        return int(decimal * Window._desired_height)
    else:
        #print(f"Obj: None:: Size(h): {int(decimal * Y)}")
        return int(decimal * Y)

#Error message function using the bulit in windows erroring method. Taking a string to be displayed to the user.
#This function is meant for quite serious errors as it takes the user out of the app
def Error(ErrorMessage : str):
   ctypes.windll.user32.MessageBoxW(0, f"An error occured:\n{ErrorMessage}", "Fatal Error", 0)
   exit()

#Before the MainView object in main is init'ed we need to ensure that the Theme.json file is in the local dir, to make the app look proper.
#Also need to ensure that the database is active, without it the app is non functional
def PreInitValidation():
    customtkinterColourConfig : bool = os.path.isfile(os.path.join(os.getcwd(), "Theme.json"))
    DatabaseManager.DBManager()

    return customtkinterColourConfig

#Given a date in the YYYY-MM-DD format (which is the format as gotten from the database) we reverse it to be DD-MM-YYYY
def ReverseDate(DateString : str):
    #Split the string at the '-' to extract the day, month and year as a list of values
    DateParts = str(DateString).split("-")

    #Then reverse the list which gets it into the dd-mm-yyyy format
    DateParts.reverse()

    #Finally we insert two '-' inbetween the parts of the date to properly format it
    DateParts.insert(1, "-"), DateParts.insert(3,"-")

    #Return the parts of the array joined to a string
    return "".join(DateParts)

#Checking function - Given a string value determine if it is an integer
def IsStringInt(StringCheck : str) -> bool:
    #Attempt to type cast the string to an integer
    try:
        int(StringCheck)
        #If the type cast didn't error - the return will run so we know the value is an int
        return True
    except: # In the event of an error - return false as the value is not a pure int
        return False

#Given the name of image as a string and the X,Y dimensions of the image, get the file and load it with PIL
#Then make the image using the CTkImage class and return it to caller
def MakeCtkImageFromName(ImageName : str, ImageGeometry : tuple):
    image = Image.open(os.path.join(ImageDir, ImageName))
    ctkImage = customtkinter.CTkImage(dark_image=image, size=ImageGeometry)

    return ctkImage