import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "weather.db")
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # store weather search history
    c.execute("""
        CREATE TABLE IF NOT EXISTS searches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            city TEXT NOT NULL,
            temperature REAL,
            humidity REAL,
            windspeed REAL,
            description TEXT,
            searched_at TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, city)   
        )"""
        )
    # store favorite cities
    c.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            city TEXT NOT NULL,
            country TEXT,
            added_at TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, city) 
        )"""
        )
    conn.commit()
    conn.close()


# search history 

def save_search(user_id, city, temperature, humidity, windspeed, description):
    
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
 
    c.execute(
        """UPDATE searches
           SET temperature = ?, humidity = ?, windspeed = ?, description = ?,
               searched_at = CURRENT_TIMESTAMP
           WHERE user_id = ? AND city = ?""",
        (temperature, humidity, windspeed, description, user_id, city)
    )
 
    if c.rowcount == 0:
        # No existing row for this user and city so insert a new one
        c.execute(
            """INSERT INTO searches (user_id, city, temperature, humidity, windspeed, description)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (user_id, city, temperature, humidity, windspeed, description)
        )
 
    conn.commit()
    conn.close()


def get_history(user_id, limit=10):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        """SELECT city, temperature, humidity, windspeed, description, searched_at
           FROM searches WHERE user_id = ? ORDER BY id DESC LIMIT ?""",
        (user_id, limit)
    )
    rows = c.fetchall()
    conn.close()
    return rows


def clear_all_history(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM searches WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()


#favorites 

def add_favorite(user_id, city, country):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO favorites (user_id, city, country) VALUES (?, ?, ?)", (user_id, city, country))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # city is already a favorite
    conn.close()


def remove_favorite(user_id, city):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM favorites WHERE user_id = ? AND city = ?", (user_id, city))
    conn.commit()
    conn.close()


def get_favorites(user_id): #returns all favorite cities ordered by most recently added.
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT city, country FROM favorites WHERE user_id = ? ORDER BY added_at DESC", (user_id,))
    rows = c.fetchall()
    conn.close()
    return rows


def is_favorite(user_id, city): # checks if a city is in the favorites table and returns True or False.
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT 1 FROM favorites WHERE user_id = ? AND city = ?", (user_id, city))
    row = c.fetchone()
    conn.close()
    return row is not None
