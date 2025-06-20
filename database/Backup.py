import shutil
import os
from datetime import datetime
import json  # Import json module for config.json handling
from models.models import User  # Import user model from models
import secrets
from database.db import get_db_connection
from utils.data_encryption import encrypt, decrypt
from services.user_service import retrieve_system_admins, store_restore_code, delete_restore_code
from utils.commands_ui import clear_console

HIGHLIGHT = '\033[7m'  # Inverse (white-on-black or black-on-white)
COMMENT = '\033[90m' # Grey
SUCCES = '\033[32m' # Green
BUTTON = '\033[34m'  # Blue
WARNING = '\033[31m' # Red
RESET = '\033[0m' # Return to normal (Always use this after coloring data)

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

    clear_console()
    print("Available backups:")
    for i, backup in enumerate(backups, start=1):
        print(f"{i}: {backup}")

    while True:
        try:
            selection = input(f"Select a backup by number: {COMMENT}Return: R{RESET}").strip().lower()

            if selection == 'r':
                return None
            elif 1 <= int(selection) <= len(backups):
                return backups[int(selection) - 1]
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def print_visible_users(current_user_list, response, page_number):
    clear_console()
    print(f"Select a System Administrator by ID to generate a restore code for: {COMMENT}+ / - page up and down{RESET}")
    print(f"\n{response}")

    if len(current_user_list) != 0:
        for user in current_user_list:
            print(f"user_id: {user.user_id} - username: {user.username}")
    else:
        print("No more System Administrators found.")
    print(f"Current page: {page_number}")
    print(f"{BUTTON}[RETURN]{RESET} - {COMMENT}Press: R{RESET}")

def generate_one_time_code():
    backup_filename = list_and_select_backup()
    if not backup_filename:
        return "Can't generate restore codes without backup files."

    response = ''
    page_number = 1
    current_user_list = retrieve_system_admins(page_number)

    while True:
        print_visible_users(current_user_list, response, page_number)
        response = ''

        choice = input('\nSelect an option: ').strip().lower()

        if is_valid_id(choice, current_user_list):
            choice_int = int(choice)
            selected_user = next(user for user in current_user_list if user.user_id == choice_int)
            code = secrets.token_urlsafe(8)  # Example: 'G5s8k2Lm'
            store_restore_code(selected_user, code, backup_filename)
            return f"Code: {WARNING}{code}{RESET}"
        elif choice == '+':
            if len(current_user_list) > 9:
                page_number += 1
                current_user_list = retrieve_system_admins(page_number)
        elif choice == '-':
            if page_number > 1:
                page_number -= 1
                current_user_list= retrieve_system_admins(page_number)
        elif choice == 'r':
            return ''
        else: response = f"{WARNING}Invalid option. Please try again.{RESET}"

    print(f"One-time code generated for system admin: {code}")
    return code

def is_valid_id(choice, user_list):
    try:
        choice_int = int(choice)
    except ValueError:
        return False
    return any(user.user_id == choice_int for user in user_list)

def retrieve_code(code, logged_in_user):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, user_id, restore_code, backup_filename FROM restore_codes")
    records = cursor.fetchall()
    conn.close()

    for record in records:
        try:
            dec_code = decrypt(record[2])
            dec_backup_filename = decrypt(record[3])
        except Exception:
            continue  # Skip corrupt entries

        if code == dec_code and logged_in_user.user_id == record[1]:
            return (record[0], record[1], dec_code, dec_backup_filename)
    
    return None

def retrieve_backup_name(restore_code_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT backup_filename FROM restore_codes WHERE id = ?", (restore_code_id,))
    record = cursor.fetchone()
    conn.close()

    if record:
        return decrypt(record[0])
    else:
        raise ValueError(f"No backup name found for restore code ID {restore_code_id}")

def UI_backup_database(Logged_in_user: User):
    from models.models import UserRole
    response = None
    while True:
        clear_console()
        if response: print(f"{response}\n")
        if Logged_in_user.role == UserRole.SUPER_ADMIN:
            print("SELECT AN OPTION:\n 1: Backup database\n 2: Restore database\n 3: Generate restore code\n 4: Exit")
        else:
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
                    clear_console()
                    print("Enter the one-time code to restore the database:")
                    code = input("One-time code: ").strip()
                    # with open("database/config.json", "r") as config_file:
                    #     config = json.load(config_file)
                    record = retrieve_code(code, Logged_in_user)
                    if record:
                        backup_restore = record[3]  # Decrypted filename from retrieve_code
                        backup_path = os.path.join(BACKUP_DIR, backup_restore)

                        if not os.path.isfile(backup_path):
                            response = f"{WARNING}Backup file '{backup_restore}' not found.{RESET}"
                        else:
                            print(f"Confirm restoration of backup: {backup_restore}")
                            confirm = input("Type 'yes' to confirm: ").strip().lower()
                            if confirm == 'yes':
                                print(f"Restoring backup: {backup_restore}")
                                delete_restore_code(record[0], backup_path, Logged_in_user) # Transfer current user account aswell
                                restore_database(backup_restore)
                                response = f"{SUCCES}Database restored from '{backup_restore}'.{RESET}"
                            else:
                                response = f"{WARNING}Restoration cancelled.{RESET}"
                    else:
                        response = f"{WARNING}Invalid one-time code. Restore failed.{RESET}"
            case '3':
                if Logged_in_user.role == UserRole.SUPER_ADMIN:
                    response = generate_one_time_code()
                else:
                    print("Exiting backup utility.")
                    break
            case '4':
                if Logged_in_user.role == UserRole.SUPER_ADMIN:
                    print("Exiting backup utility.")
                    break
                else:
                    print("Invalid option. Please try again.")
            case _:
                print("Invalid option. Please try again.")