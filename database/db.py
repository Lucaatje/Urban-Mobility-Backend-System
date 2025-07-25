import sqlite3, bcrypt
from models.models import UserRole
import os, json
from utils.data_encryption import encrypt

CONFIG_PATH = "database/config.json"

def get_db_connection():
    # Load the database path from config.json
    with open(CONFIG_PATH, "r") as config_file:
        config = json.load(config_file)
        db_path = config.get("db_path", "database/urban_mobility.db")

    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn



def init_db():
    # Load the database path from config.json
    with open(CONFIG_PATH, "r") as config_file:
        config = json.load(config_file)
        db_path = config.get("db_path", "database/urban_mobility.db")

    # Check if the database file exists
    if os.path.exists(db_path):
        return

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
        driving_license_number TEXT UNIQUE,
        REGISTRATION_DATE TEXT DEFAULT (datetime('now','localtime'))
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

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS temp_passwords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        expire_date DATETIME
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS restore_codes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        restore_code TEXT NOT NULL,
        backup_filename TEXT NOT NULL
    )
    """)

    username = 'super_admin'
    email = 'admin@gmail.com'
    password = 'Admin_123?'
    role = UserRole.SUPER_ADMIN

    encrypted_username = encrypt(username)
    encrypted_email = encrypt(email)

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    

    cursor.execute("""
        INSERT INTO users (username, email, password, role)
        VALUES (?, ?, ?, ?)
        """, (encrypted_username, encrypted_email, hashed_password, role.value))

    conn.commit()
    conn.close()
