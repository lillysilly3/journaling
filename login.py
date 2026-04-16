import customtkinter as ctk
from database import check_password as db_check_password

class LoginScreen(ctk.CTkFrame):
    def __init__(self, parent, on_login_success):
        super().__init__(parent)
        self.on_login_success = on_login_success

        #Title
        label = ctk.CTkLabel(self, text="My Journal", font=ctk.CTkFont(size=24, weight="bold"))
        label.pack(pady=30)

        #Password
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Enter password", show="*", width=200)
        self.password_entry.pack(pady=10)

        #Login button
        button = ctk.CTkButton(self, text="Login", command=self.check_password)
        button.pack(pady=10)
        self.password_entry.bind("<Return>", lambda event: self.check_password())
        self.password_entry.bind("<space>", lambda event: self.check_password())

        #Error message
        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.pack()

    def check_password(self):
        password = self.password_entry.get()
        if db_check_password(password):
            self.on_login_success()
        else:
            self.error_label.configure(text="Wrong password!")
