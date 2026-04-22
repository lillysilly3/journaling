import customtkinter as ctk
import datetime
from database import DatabaseClient
from calendar_widget import CalendarWidget
from moods import MOODS, MOOD_COLORS
from theme import COLORS

class JournalScreen(ctk.CTkFrame):
    def __init__(self, parent, db: DatabaseClient, fg_color=COLORS["frame"]):
        super().__init__(parent)
        self.db = db
        self.current_mood = ""
        self.current_date = datetime.date.today().strftime("%Y-%m-%d")

        #Grid
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        #Frames
        self.top_frame = ctk.CTkFrame(self, fg_color=COLORS["bg"])
        self.top_frame.grid(row=0, columnspan=2, sticky="ew", padx=5, pady=5)

        self.left_frame = ctk.CTkFrame(self, fg_color=COLORS["bg"],)
        self.left_frame.grid(row=1, column=0, sticky="ns", padx=5, pady=5)

        self.right_frame = ctk.CTkFrame(self, fg_color=COLORS["bg"],)
        self.right_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        #Top button
        ctk.CTkButton(self.top_frame, text="💾", corner_radius=200, width=0, height=0, fg_color=COLORS["accent"], hover_color=COLORS["button_hover"], text_color="white", command=self.save_entry).pack(side="left", padx=10, pady=10)

        #Right frame grid
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(0, weight=0)
        self.right_frame.grid_rowconfigure(1, weight=2)

        #Date label
        today = datetime.date.today().strftime("%Y %B %d")
        self.date_label = ctk.CTkLabel(self.right_frame, text=today, text_color=COLORS["label"], font=ctk.CTkFont(size=18, weight="bold"))
        self.date_label. grid(row=0, column=0, sticky="w", padx=10, pady=10)
        

        #Textbox
        self.entry_textbox = ctk.CTkTextbox(self.right_frame, fg_color=COLORS["entry"], text_color=COLORS["text"], width=200)
        self.entry_textbox.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        #Entry
        self.load_entry(datetime.date.today().strftime("%Y-%m-%d"))

        #Left frame grid
        self.left_frame.grid_rowconfigure(0, weight=0)
        self.left_frame.grid_rowconfigure(1, weight=0)
        self.left_frame.grid_rowconfigure(2, weight=1)
        self.left_frame.grid_columnconfigure(0, weight=1)

        #Calendar
        self.calendar = CalendarWidget(self.left_frame, db, self.load_entry)
        self.calendar.grid(row=0, column=0, padx=5, pady=5)
        
        #Mood tracker
        self.mood_frame = ctk.CTkFrame(self.left_frame)
        self.mood_frame.grid(row=1, column=0, padx=5, pady=5)
        ctk.CTkLabel(self.mood_frame, text="How do you feel today?", text_color=COLORS["label"], font=ctk.CTkFont(weight="bold")).pack(pady=5)

        for mood, color in MOODS:
            ctk.CTkButton(self.mood_frame, text=mood, text_color=COLORS["text"], fg_color=color, width=160, command=lambda m=mood: self.set_mood(m)).pack(pady=2)

    def save_entry(self):
        date = self.current_date
        content = self.entry_textbox.get("1.0", "end-1c")
        print(f"Saving: {date}, {content}")
        self.db.save_entry(date, content, self.current_mood)
        self.calendar.month_cache.clear()
        self.calendar.build_calendar()
        self.load_entry(date)
        print("Entry saved!")

    def load_entry(self, date):
        self.current_date = date
        print(f"Loading entry for: {date}")
        result = self.db.get_entry(date)
        print(f"Result: {result}")
        self.entry_textbox.delete("1.0", "end")
        if result:
            content, mood = result
            self.entry_textbox.insert("1.0", content)
            self.current_mood = mood if mood else ""
        else:
            self.current_mood = ""
        mood_emoji = self.current_mood.split()[0] if self.current_mood else ""
        display_date = datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%Y %B %d")
        self.date_label.configure(text=f"{display_date} {mood_emoji}")

    def set_mood(self, mood):
        self.current_mood = mood
        print(f"Mood set: {mood}")

    