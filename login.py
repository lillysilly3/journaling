import customtkinter as ctk
from database import DatabaseClient

class LoginScreen(ctk.CTkFrame):
    def __init__(self, parent, on_login_success, on_reset, db: DatabaseClient):
        super().__init__(parent)
        self.on_login_success = on_login_success
        self.on_reset = on_reset
        self.db = db

        #Title
        label = ctk.CTkLabel(self, text="My Journal", font=ctk.CTkFont(size=24, weight="bold"))
        label.pack(pady=30)

        #Password
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Enter password", show="*", width=200)
        self.password_entry.pack(pady=10)

        #Login button
        button = ctk.CTkButton(self, text="Login", command=self.check_password)
        button.pack(pady=10)
        self.password_entry.bind("<Return>", lambda event: self.db.check_password())
        self.password_entry.bind("<space>", lambda event: self.db.check_password())

        #Show password chekbox
        self.show_password_var = ctk.BooleanVar()
        ctk.CTkCheckBox(self, text="Show password", variable=self.show_password_var, command=self.toggle_password).pack(pady=5)

        #Hint button
        hint_button = ctk.CTkButton(self, text="Forgot password?", command=self.show_hint)
        hint = self.db.get_setting("hint")
        if hint:
            hint_button.pack(pady=5)

        #Reset button
        self.reset_button = ctk.CTkButton(self, text="Reset password", command=self.confirm_reset)

        #Error message
        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.pack()

    def check_password(self):
        password = self.password_entry.get()
        if self.db.check_password(password):
            self.on_login_success()
        else:
            self.error_label.configure(text="Wrong password!")

    def show_hint(self):
        hint = self.db.get_setting("hint")
        if hint:
            if self.error_label.cget("text") == f"Hint: {hint}":
                self.error_label.configure(text="")
            else:
                self.error_label.configure(text=f"Hint: {hint}")
                self.reset_button.pack(pady=5)

    def toggle_password(self):
        if self.show_password_var.get():
            self.password_entry.configure(show="")
        else:
            self.password_entry.configure(show="*")

    def confirm_reset(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Reset password")
        popup.geometry("300x150")
        
        ctk.CTkLabel(popup, text="All data will be deleted. Are you sure?").pack(pady=10)
        
        button_frame = ctk.CTkFrame(popup)
        button_frame.pack(pady=10)
        ctk.CTkButton(button_frame, text="Reset", command=lambda: [self.on_reset(), popup.destroy()]).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="Cancel", command=popup.destroy).pack(side="left", padx=10)
