import customtkinter as ctk
from login import LoginScreen
from database import DatabaseClient
from setup import SetupScreen
from journal import JournalScreen
from theme import COLORS

def on_login_success():
    print("logged in!")
    global login_screen
    global app
    global db
    login_screen.destroy()
    journal_screen = JournalScreen(app,db)
    journal_screen.pack(expand=True, fill="both")
    app.geometry("900x600")

def on_setup_complete():
    global setup_screen
    global login_screen
    global db
    setup_screen.pack_forget()
    login_screen = LoginScreen(app, on_login_success, on_reset, db)
    login_screen.pack(expand=True, fill="both")

def on_reset():
    global login_screen
    global setup_screen
    global db
    db.reset()
    login_screen.destroy()
    setup_screen = SetupScreen(app, on_setup_complete, db)
    setup_screen.pack(expand=True, fill="both")

def on_closing():
    global db
    global app
    db.close()
    app.destroy()

app = ctk.CTk()
app.title("My Journal")
app.geometry("500x500")
ctk.set_appearance_mode("light")

#Initialising database
db = DatabaseClient()

#Declaration before usage
setup_screen = None
login_screen = None

if db.has_password():
    login_screen = LoginScreen(app, on_login_success, on_reset, db)
    login_screen.pack(expand=True, fill="both")
else:
    setup_screen = SetupScreen(app, on_setup_complete, db)
    setup_screen.pack(expand=True, fill="both")
    
app.mainloop()


