import shutil
import os
from datetime import datetime
import json  # Import json module for config.json handling
from models.models import User  # Import user model from models
import secrets

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
    main_db_path = DB_PATH  # "database/urban_mobility.db"

    if not os.path.exists(backup_path):
        print("Backup file does not exist. Restore failed.")
        return

    # Overwrite the main database file with the backup
    shutil.copy2(backup_path, main_db_path)
    print(f"Database restored successfully from: {backup_path}")

    # Optionally, update config.json to point to the main database file (recommended for consistency)
    config_path = os.path.join("database", "config.json")
    if os.path.exists(config_path):
        with open(config_path, "r") as config_file:
            config = json.load(config_file)
        config["db_path"] = main_db_path
        with open(config_path, "w") as config_file:
            json.dump(config, config_file)

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

def generate_one_time_code():
    # Only super admin should call this!
    config_path = os.path.join("database", "config.json")
    if not os.path.exists(config_path):
        print("Config file does not exist. Cannot generate code.")
        return

    # Generate a secure random code
    code = secrets.token_urlsafe(8)  # Example: 'G5s8k2Lm'
    with open(config_path, "r") as config_file:
        config = json.load(config_file)

    config["one_time_code"] = code

    with open(config_path, "w") as config_file:
        json.dump(config, config_file)

    print(f"One-time code generated for system admin: {code}")
    return code


def UI_backup_database(Logged_in_user: User):
    from models.models import UserRole
    while True:
        print("SELECT AN OPTION:\n 1: Backup database\n 2: Restore database\n 3: Exit")
        match input("Enter your choice: ").strip():
            case '1':
                backup_database()
            case '2':
                if Logged_in_user.role == UserRole.SUPER_ADMIN:
                    backup_filename = list_and_select_backup()
                    if backup_filename:
                        restore_database(backup_filename)
                elif Logged_in_user.role == UserRole.SYSTEM_ADMIN:
                    print("Enter the one-time code to restore the database:")
                    code = input("One-time code: ").strip()
                    with open("database/config.json", "r") as config_file:
                        config = json.load(config_file)
                    if code == config.get("one_time_code"):
                        backups = [f for f in os.listdir(BACKUP_DIR) if f.endswith(".db")]
                        if not backups:
                            print("No backup files found.")
                            continue
                        newest_backup = max(backups, key=lambda f: os.path.getctime(os.path.join(BACKUP_DIR, f)))
                        print(f"Confirm restoration of backup: {newest_backup}")
                        confirm = input("Type 'yes' to confirm: ").strip().lower()
                        if confirm != 'yes':
                            print("Restoration cancelled.")
                            continue
                        print(f"Restoring newest backup: {newest_backup}")
                        restore_database(newest_backup)
                        generate_one_time_code()
                    else:
                        print("Invalid one-time code. Restore failed.")
            case '3':
                print("Exiting backup utility.")
                break
            case _:
                print("Invalid option. Please try again.")