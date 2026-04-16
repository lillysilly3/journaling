import customtkinter as ctk
from database import DatabaseClient

class SetupScreen(ctk.CTkFrame):
    def __init__(self, parent, on_setup_complete, db: DatabaseClient):
        super().__init__(parent)
        self.on_setup_complete = on_setup_complete
        self.db = db

        #Setup title
        label = ctk.CTkLabel(self, text="Welcome to your Journal!\nCreate your password", font=ctk.CTkFont(size=18, weight="bold"))
        label.pack(pady=30)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Enter password", show="", width=200)
        self.password_entry.pack(pady=10)

        self.confirm_entry = ctk.CTkEntry(self, placeholder_text="Confirm password", show="", width=200)
        self.confirm_entry.pack(pady=10)

        button = ctk.CTkButton(self, text="Create password", command=self.save_password)
        button.pack(pady=10)
        self.password_entry.bind("<Return>", lambda event: self.save_password())
        self.password_entry.bind("<space>", lambda event: self.save_password())

        #Hint
        self.hint_entry = ctk.CTkEntry(self, placeholder_text="Enter a password hint (optional)", width=200)
        self.hint_entry.pack(pady=10)

        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.pack()

    def save_password(self):
        password_entry = self.password_entry.get()
        confirm_entry = self.confirm_entry.get()
        if password_entry == "" or confirm_entry == "":
            self.error_label.configure(text="Please fill in both fields")
        elif password_entry == confirm_entry:
            if " " in password_entry:
                self.error_label.configure(text="Password cannot contain spaces!")
                return
            elif len(password_entry) < 4:
                self.error_label.configure(text="Password must be at least 4 characters!")
                return
            elif len(password_entry) > 32:
                self.error_label.configure(text="Password cannot exceed 32 characters!")
                return
            
            #Password set
            self.db.set_password(password_entry)
            
            #Hint set
            hint = self.hint_entry.get()
            if hint != "":
                self.db.save_setting("hint", hint)
            
            self.on_setup_complete()
        else:
            self.error_label.configure(text="Passwords do not match")