import customtkinter as ctk
import datetime
import calendar
from database import DatabaseClient
from moods import MOOD_COLORS


class CalendarWidget(ctk.CTkFrame):
    def __init__(self, parent, db: DatabaseClient, on_day_select):
        super().__init__(parent)
        self.db = db
        self.on_day_select = on_day_select
        self.current_year = datetime.date.today().year
        self.current_month = datetime.date.today().month
        self.month_cache = {}
        self.selected_date = datetime.date.today().strftime("%Y-%m-%d")
        self.build_calendar()        

    
    def build_calendar(self):
        print("Building calendar...")
        for widget in self.winfo_children():
            widget.destroy()
        cache_key = f"{self.current_year}-{self.current_month}"
        if cache_key not in self.month_cache:
            self.month_cache[cache_key] = self.db.get_entries_for_month(self.current_year, self.current_month)
        month_entries = self.month_cache[cache_key]
        print(f"Month entries: {month_entries}")

        #Navigation for calendar
        nav_frame = ctk.CTkFrame(self)
        nav_frame.grid(row=0, column=0, columnspan=7, pady=5)
        ctk.CTkButton(nav_frame, text="<", width=30, command=self.prev_month).pack(side="left", padx=5)
        ctk.CTkLabel(nav_frame, text=f"{calendar.month_name[self.current_month]} {self.current_year}", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=10)
        ctk.CTkButton(nav_frame, text=">", width=30, command=self.next_month).pack(side="left", padx=5)

        #Days in the calendar
        days = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
        for i, day in enumerate(days):
            ctk.CTkLabel(self, text=day, width=30).grid(row=1, column=i, padx=2)
        
        cal = calendar.monthcalendar(self.current_year, self.current_month)
        today_date = datetime.date.today()
        today = today_date.day if (self.current_year == today_date.year and self.current_month == today_date.month) else -1
        
        #Making buttons
        for week_num, week in enumerate(cal):
            for day_num, day in enumerate(week):
                if day == 0:
                    ctk.CTkLabel(self, text="", width=30).grid(row=week_num+2, column=day_num, padx=1, pady=1)
                else:
                    date_str = f"{self.current_year}-{self.current_month:02d}-{day:02d}"
                    entry_data = month_entries.get(date_str)
                    mood = entry_data[1] if entry_data else None
                    color = MOOD_COLORS.get(mood, "transparent") if mood else "transparent"
                    is_selected = date_str == self.selected_date
                    if day == today:
                        ctk.CTkButton(self, text=str(day), width=20, height=20, fg_color=color, corner_radius=20,
                        border_width=2, border_color="#755CE4", 
                        command=lambda d=date_str: self.on_day_select(d)).grid(row=week_num+2, column=day_num, padx=1, pady=1)
                    else:
                        border = 2 if (entry_data and not mood) or is_selected else 0
                        border_color = "white" if is_selected else None
                        ctk.CTkButton(self, text=str(day), width=20, height=20, fg_color=color, border_width=border, 
                        border_color=border_color,
                        command=lambda d=date_str: self.on_day_select(d)).grid(row=week_num+2, column=day_num, padx=1, pady=1)          
                    
    def prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.build_calendar()

    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.build_calendar()