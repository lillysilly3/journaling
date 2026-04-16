import customtkinter as ctk
from login import LoginScreen
from database import initialize_db


def on_login_success():
    print("Logged in!")

initialize_db()

app = ctk.CTk()
app.title("My Journal")
app.geometry("400x500")

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

login_screen = LoginScreen(app, on_login_success)
login_screen.pack(expand=True, fill="both")

app.mainloop()