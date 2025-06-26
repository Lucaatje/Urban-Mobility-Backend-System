from database.db import get_db_connection
from utils.input_validation import username_checker, password_checker
from models.models import User, UserRole
from utils.commands_ui import clear_console
from datetime import datetime, timedelta
from utils.password_utils import hash_password
from utils.data_encryption import encrypt, decrypt
from logs.logger import write_log
import bcrypt
import json
import sqlite3

CONFIG_PATH = "database/config.json"


HIGHLIGHT = '\033[7m'  # Inverse (white-on-black or black-on-white)
COMMENT = '\033[90m' # Grey
SUCCES = '\033[32m' # Green
BUTTON = '\033[34m'  # Blue
WARNING = '\033[31m' # Red
RESET = '\033[0m' # Return to normal (Always use this after coloring data)



def login(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    if len(username) == 0 and len(password) == 0: 
        return False, "Enter username and password."
    if len(username) == 0: 
        return False, "Enter username."
    if len(password) == 0: 
        return False, "Enter password."

    # Laad alle gebruikers op (gebruikersnaam is encrypted in DB)
    cursor.execute("SELECT id, username, email, password, role FROM users")
    users = cursor.fetchall()
    conn.close()

    # Doorloop gebruikers, decrypt gebruikersnaam, en vergelijk
    for user in users:
        user_id, enc_username, enc_email, hashed_password, user_role = user

        try:
            decrypted_username = decrypt(enc_username)
        except Exception as e:
            continue  # Sla corrupte records over

        if decrypted_username == username:
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                write_log(username, "Logged in", "", suspicious=False)
                return User(user_id, decrypted_username, hashed_password, decrypt(enc_email), UserRole(user_role)), f"Gebruiker '{username}' succesvol ingelogd."
            else:
                write_log(username, "Unsuccessful login", f"username: {username} is used for a login attempt with a wrong password", suspicious=True)
                return False, "Gebruikersnaam en of wachtwoord verkeerd."

    return False, "Gebruikersnaam en of wachtwoord verkeerd."




def register(username, email, password, role, executed_by):
    conn = get_db_connection()
    cursor = conn.cursor()

    valid, message = username_checker(username)
    if not valid:
        return valid, message

    valid, message = password_checker(password)
    if not valid:
        return valid, message
    
    # valid, message = email_checker(email)
    # if not valid:
    #     return valid, message

    hashed_password = hash_password(password)

    encrypted_username = encrypt(username)
    encrypted_email = encrypt(email)

    try:
        cursor.execute("""
        INSERT INTO users (username, email, password, role)
        VALUES (?, ?, ?, ?)
        """, (encrypted_username, encrypted_email, hashed_password, role.value))
        conn.commit()
        write_log(executed_by, "New user is created", f"username: {username}")
        return valid, f"Gebruiker '{username}' succesvol geregistreerd."
    except Exception as e:
        write_log(executed_by, "Tried creating new user", f"username: {username}")
        return False, f"Registratiefout: {e}"
    finally:
        conn.close()



def update(user_id, username, email, password, role, selected_user, logged_in_user):
    conn = get_db_connection()
    cursor = conn.cursor()

    if username != '':
        valid, message = username_checker(username)
        if not valid:
            return valid, message
        enc_username = encrypt(username)
    else:
        username = selected_user.username
        enc_username = encrypt(username)  # nodig voor storage

    if password != '':
        valid, message = password_checker(password)
        if not valid:
            return valid, message
        if selected_user.user_id != logged_in_user.user_id:
            valid, message = temp_password_add(username, password, datetime.now() + timedelta(hours=1))
            if not valid:
                return valid, message
        else:
            valid, message = update_new_password(logged_in_user.username, password)

    if email == '':
        email = selected_user.email
    # Hier zou je een email_checker() kunnen toevoegen
    enc_email = encrypt(email)

    try:
        cursor.execute("""
            UPDATE users
            SET username = ?, email = ?, role = ?
            WHERE id = ?
        """, (enc_username, enc_email, role.value, user_id))
        conn.commit()
        write_log(username, "User is updated", f"User {selected_user.username} is updated", suspicious=False)
        return True, f"Gebruiker '{username}' succesvol geüpdatet."
    except Exception as e:
        write_log(username, "Tried updating user", f"Tried updating user {selected_user.username}", suspicious=True)
        return False, f"Updatefout: {e}"
    finally:
        conn.close()



def delete(selected_user, executed_by):
    while True:
        clear_console()
        print(f"Are you sure you want to delete this account?")
        print(f"{BUTTON}[YES]{RESET} {COMMENT}Press: 1{RESET}")
        print(f"{BUTTON}[NO]{RESET} {COMMENT}Press: 2{RESET}")

        choice = input("\nSelect an option: ").strip().lower()

        if choice == '1': break
        if choice == '2': return False, ''

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        encrypted_username = encrypt(selected_user.username)

        cursor.execute("""
            DELETE FROM users
            WHERE id = ?
        """, (selected_user.user_id,))

        cursor.execute("""
            DELETE FROM temp_passwords
            WHERE username = ?
        """, (encrypted_username,))
        conn.commit()
        write_log(executed_by, "User is deleted", f"User {selected_user.username} is deleted", suspicious=False)
        return True, f"{SUCCES}Gebruiker '{selected_user.username}' succesvol verwijderd.{RESET}"
    except Exception as e:
        write_log(executed_by, "Tried deleting user", f"{selected_user.username} ", suspicious=True)
        return False, f"{WARNING}Verwijderfout: {e}{RESET}"
    finally:
        conn.close()


        

def retrieve_users(page_number):
    conn = get_db_connection()
    cursor = conn.cursor()
    row_start = (page_number - 1) * 10

    query = "SELECT id, username, email, password, role FROM users LIMIT 10 OFFSET ?"
    cursor.execute(query, (row_start,))
    rows = cursor.fetchall()

    users = []
    for row in rows:
        id, enc_username, enc_email, password, role_str = row
        try:
            username = decrypt(enc_username)
        except Exception:
            username = "[Fout bij decryptie username]"
        try:
            email = decrypt(enc_email)
        except Exception:
            email = "[Fout bij decryptie email]"
        role = UserRole(role_str)
        user = User(id, username, password, email, role)
        users.append(user)

    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]

    conn.close()
    return users, user_count

def retrieve_system_admins(page_number):
    conn = get_db_connection()
    cursor = conn.cursor()
    row_start = (page_number - 1) * 10

    # Only fetch SYSTEM_ADMINISTRATOR users
    query = """
        SELECT id, username, email, password, role
        FROM users
        WHERE role = ?
        LIMIT 10 OFFSET ?
    """
    cursor.execute(query, (UserRole.SYSTEM_ADMIN.value, row_start))
    rows = cursor.fetchall()

    users = []
    for row in rows:
        id, enc_username, enc_email, password, role_str = row
        try:
            username = decrypt(enc_username)
        except Exception:
            username = "[Fout bij decryptie username]"
        try:
            email = decrypt(enc_email)
        except Exception:
            email = "[Fout bij decryptie email]"
        role = UserRole(role_str)
        user = User(id, username, password, email, role)
        users.append(user)

    # Get total count of SYSTEM_ADMINISTRATOR users
    # cursor.execute("SELECT COUNT(*) FROM users WHERE role = ?", (UserRole.SYSTEM_ADMINISTRATOR.value,))
    # user_count = cursor.fetchone()[0]

    conn.close()
    return users

def store_restore_code(selected_user, code, backup_filename):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        record = cursor.execute("""
            SELECT id
            FROM restore_codes
            WHERE user_id = ?
        """, (selected_user.user_id,)).fetchone()

        if record:
            cursor.execute("""
                UPDATE restore_codes
                SET restore_code = ?, backup_filename = ?
                WHERE id = ?
            """, (encrypt(code), encrypt(backup_filename), record[0]))
        else:
            cursor.execute("""
                INSERT INTO restore_codes (user_id, restore_code, backup_filename)
                VALUES (?, ?, ?)
            """, (selected_user.user_id, encrypt(code), encrypt(backup_filename)))
        conn.commit()
    except Exception as e:
        raise ValueError(f"Updatefout: {e}")
    finally:
        conn.close()

def delete_restore_code(restore_code_id, backup_path, logged_in_user):
    conn = sqlite3.connect(backup_path)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    try:
        cursor.execute("""
            DELETE FROM restore_codes
            WHERE id = ?
        """, (restore_code_id,))

        valid, message = username_checker(logged_in_user.username)
        if valid:
            cursor.execute("""
            INSERT INTO users (username, email, password, role)
            VALUES (?, ?, ?, ?)
            """, (encrypt(logged_in_user.username), encrypt(logged_in_user.email), logged_in_user.password_hash, logged_in_user.role.value))

        conn.commit()
    except Exception as e:
        raise ValueError(f"Verwijderfout: {e}")
    finally:
        conn.close()

def temp_password_add(username, password, expire_date):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT id FROM temp_passwords WHERE username = ? AND password = ?
        """, (encrypt(username), hash_password(password)))
        temp_password = cursor.fetchone()

        if temp_password:
            cursor.execute("""
                UPDATE temp_passwords 
                SET password = ?, expire_date = ?
                WHERE id = ?
            """, (hash_password(password), expire_date, temp_password[0]))
        else:
            cursor.execute("""
                INSERT INTO temp_passwords (username, password, expire_date)
                VALUES (?, ?, ?)
            """, (encrypt(username), hash(password), expire_date))
        conn.commit()
        return True, f"{SUCCES}Tijdelijk wachtwoord succesvol opgeslagen.{RESET}"
    except Exception as e:
        return False, f"{WARNING}Updatefout: {e}{RESET}"
    finally:
        conn.close()

def change_password(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT username, password, expire_date FROM temp_passwords WHERE username = ?
        """, (encrypt(username),))

        temp_password = cursor.fetchone()

        if temp_password:
            if datetime.strptime(temp_password[2], "%Y-%m-%d %H:%M:%S.%f") < datetime.now() or temp_password[1] != password:
                return False, f"{WARNING}Gebruikersnaam en of wachtwoord verkeerd.{RESET}"
            else:
                return True, None
        else:
            return False, None
    except Exception as e:
        return False, f"{WARNING}Zoekfout: {e}{RESET}"
    finally:
        conn.close()

def update_password(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    if len(password) == 0: return False, "Enter password."

    valid, message = password_checker(password)
    if not valid:
        return valid, message

    try:
        enc_username = encrypt(username)
        password_hash = hash_password(password)

        cursor.execute("""
            UPDATE users
            SET password = ?
            WHERE username = ?
        """, (password_hash, enc_username))

        cursor.execute("""
            DELETE FROM temp_passwords
            WHERE username = ?
        """, (enc_username,))
        conn.commit()
        return True, f"{SUCCES}Wachtwoord voor '{username}' succesvol geupdate.{RESET}"
    except Exception as e:
        return False, f"{WARNING}Updatefout: {e}{RESET}"
    finally:
        conn.close()

def update_new_password(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    if len(password) == 0: return False, "Enter password."

    valid, message = password_checker(password)
    if not valid:
        return valid, message

    try:
        enc_username = encrypt(username)
        password_hash = hash_password(password)

        cursor.execute("""
            UPDATE users
            SET password = ?
            WHERE username = ?
        """, (password_hash, enc_username))
        conn.commit()

        cursor.execute("""
            DELETE FROM temp_passwords
            WHERE username = ?
        """, (enc_username,))
        conn.commit()
        return True, f"{SUCCES}Wachtwoord voor '{username}' succesvol geupdate.{RESET}"
    except Exception as e:
        return False, f"{WARNING}Updatefout: {e}{RESET}"
    finally:
        conn.close()