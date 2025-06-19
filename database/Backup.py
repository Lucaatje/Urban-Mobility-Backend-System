import shutil
import os
from datetime import datetime
import json  # Import json module for config.json handling

DB_PATH = "database/urban_mobility.db"  # Updated path
BACKUP_DIR = "database/backups"  # Ensure backups are stored in the database folder

def backup_database():
    if not os.path.exists(DB_PATH):
        print("Database does not exist. Backup failed.")
        return

    if not os.path.exists(BACKUP_DIR):
        print(f"Creating backups directory at: {os.path.abspath(BACKUP_DIR)}")
        os.makedirs(BACKUP_DIR)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(BACKUP_DIR, f"urban_mobility_backup_{timestamp}.db")

    shutil.copy(DB_PATH, backup_path)
    print(f"Backup created successfully: {backup_path}")

def restore_database(backup_filename):
    backup_path = os.path.join(BACKUP_DIR, backup_filename)

    if not os.path.exists(backup_path):
        print("Backup file does not exist. Restore failed.")
        return

    # Update the active database path in the existing config.json file
    config_path = os.path.join("database", "config.json")  # Ensure correct path
    if not os.path.exists(config_path):
        print("Config file does not exist. Restore failed.")
        return

    with open(config_path, "r") as config_file:
        config = json.load(config_file)

    config["db_path"] = backup_path  # Update the database path

    with open(config_path, "w") as config_file:
        json.dump(config, config_file)

    print(f"Database restored successfully from: {backup_path}")

def list_and_select_backup():
    if not os.path.exists(BACKUP_DIR):
        print("No backups directory found.")
        return None

    backups = [f for f in os.listdir(BACKUP_DIR) if f.endswith(".db")]
    if not backups:
        print("No backup files found.")
        return None

    print("Available backups:")
    for i, backup in enumerate(backups, start=1):
        print(f"{i}: {backup}")

    while True:
        try:
            selection = int(input("Select a backup by number: "))
            if 1 <= selection <= len(backups):
                return backups[selection - 1]
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def UI_backup_database():
    print("SELECT AN OPTION:\n 1: Backup database\n 2: Restore database\n 3: Exit")
    match input("Enter your choice: ").strip():
        case '1':
            backup_database()
        case '2':
            backup_filename = list_and_select_backup()
            if backup_filename:
                restore_database(backup_filename)
        case '3':
            print("Exiting backup utility.")
            return
        case _:
            print("Invalid option. Please try again.")
            UI_backup_database()