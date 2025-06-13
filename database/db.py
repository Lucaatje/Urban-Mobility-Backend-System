import sqlite3

DB_PATH = "urban_mobility.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn



def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS travellers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        birthday TEXT NOT NULL,
        gender TEXT CHECK(gender IN ('male', 'female')) NOT NULL,
        street_name TEXT,
        house_number TEXT,
        zip_code TEXT,
        city TEXT,
        email_address TEXT UNIQUE,
        mobile_phone TEXT,
        driving_license_number TEXT UNIQUE
        REGISTRATION_DATE TEXT DEFAULT (datetime('now','localtime')
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scooters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        brand TEXT,
        model TEXT,
        serial_number TEXT UNIQUE,
        top_speed INTEGER,
        battery_capacity INTEGER,
        state_of_charge INTEGER,
        target_soc_min INTEGER,
        target_soc_max INTEGER,
        latitude REAL,
        longitude REAL,
        out_of_service INTEGER CHECK(out_of_service IN (0, 1)),
        mileage INTEGER,
        last_maintenance TEXT
    )
    """)

    conn.commit()
    conn.close()
