import sqlite3
import bcrypt
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "journal.db")

class DatabaseClient():
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS settings (key TEXT, value TEXT)")
        self.conn.commit()        

    def set_password(self, password):
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        self.cur.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", ("password", hashed))
        self.conn.commit()

    def check_password(self, password):
        self.cur.execute("SELECT value FROM settings WHERE key = ?", ("password",))
        result = self.cur.fetchone()
        
        if result is None:
            return False
        elif bcrypt.checkpw(password.encode(), result[0].encode()):
            return True
        else:
            return False
        
    def has_password(self):
        self.cur.execute("SELECT value FROM settings WHERE key = ?", ("password",))
        result = self.cur.fetchone()
        
        if result is None:
            return False
        else:
            return True
        
    def save_setting(self, key, value):
        self.cur.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
        self.conn.commit()

    def get_setting(self, key):
        self.cur.execute("SELECT value FROM settings WHERE key = ?", (key,))
        result= self.cur.fetchone()
        if result is None:
            return None
        else:
            return result[0]
        
    def reset(self):
        self.cur.execute("DELETE FROM settings")
        self.conn.commit()

    def close(self):
        self.conn.close()
    
