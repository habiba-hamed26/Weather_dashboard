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
            city TEXT NOT NULL,
            temperature REAL,
            humidity REAL,
            windspeed REAL,
            description TEXT,
            searched_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # store favorite cities
    c.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL UNIQUE,
            country TEXT,
            added_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


# search history 

def save_search(city, temperature, humidity, windspeed, description):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        """INSERT INTO searches (city, temperature, humidity, windspeed, description) VALUES (?, ?, ?, ?, ?)""", (city, temperature, humidity, windspeed, description)
             )
    conn.commit()
    conn.close()


def get_history(limit=10):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        """SELECT city, temperature, humidity, windspeed, description, searched_at
           FROM searches
           ORDER BY id DESC LIMIT ?""", (limit,)
    )
    rows = c.fetchall()
    conn.close()
    return rows


def clear_all_history():    # delete all records from the searches table
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM searches")
    conn.commit()
    conn.close()


#favorites 

def add_favorite(city, country):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO favorites (city, country) VALUES (?, ?)", (city, country))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # city is already a favorite
    conn.close()


def remove_favorite(city):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM favorites WHERE city = ?", (city,))
    conn.commit()
    conn.close()


def get_favorites(): #returns all favorite cities ordered by most recently added.
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT city, country FROM favorites ORDER BY added_at DESC")
    rows = c.fetchall()
    conn.close()
    return rows


def is_favorite(city): # checks if a city is in the favorites table and returns True or False.
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT 1 FROM favorites WHERE city = ?", (city,))
    row = c.fetchone()
    conn.close()
    return row is not None
