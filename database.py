import sqlite3
import bcrypt

def initialize_db():
    conn = sqlite3.connect("journal.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS settings (key TEXT, value TEXT)")
    conn.commit()
    conn.close()

def set_password(password):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    conn = sqlite3.connect("journal.db")
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", ("password", hashed))
    conn.commit()
    conn.close()

def check_password(password):
    conn = sqlite3.connect("journal.db")
    cur = conn.cursor()
    cur.execute("SELECT value FROM settings WHERE key = ?", ("password",))
    result = cur.fetchone()
    
    if result is None:
        conn.close()
        return False
    elif bcrypt.checkpw(password.encode(), result[0]):
        conn.close()
        return True
    else:
        conn.close()
        return False
    
def has_password():
    conn = sqlite3.connect("journal.db")
    cur = conn.cursor()
    cur.execute("SELECT value FROM settings WHERE key = ?", ("password",))
    result = cur.fetchone()
    
    if result is None:
        conn.close()
        return False
    else:
        conn.close()
        return True
    
