from database.db import get_db_connection
from utils.input_validation import username_checker, password_checker
from models.models import User, UserRole
from utils.commands_ui import clear_console


HIGHLIGHT = '\033[7m'  # Inverse (white-on-black or black-on-white)
COMMENT = '\033[90m' # Grey
SUCCES = '\033[32m' # Green
BUTTON = '\033[34m'  # Blue
WARNING = '\033[31m' # Red
RESET = '\033[0m' # Return to normal (Always use this after coloring data)

def login(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    if len(username) == 0 and len(password) == 0: return False, "Enter username and password."
    if len(username) == 0: return False, "Enter username."
    if len(password) == 0: return False, "Enter password."

    # CREATE HASH-FUNCTION: Hash password before comparing password with the password inside database.
    
    cursor.execute("SELECT id, username, email, password, role FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        return User(user[0], user[1], user[3], user[2], UserRole(user[4])), f"Gebruiker '{username}' succesvol ingelogd."
    else:
        return False, "Gebruikersnaam en of wachtwoord verkeerd."



def register(username, email, password, role):
    conn = get_db_connection()
    cursor = conn.cursor()

    valid, message = username_checker(username)
    if not valid:
        return valid, message

    valid, message = password_checker(password)
    if not valid:
        return valid, message

    try:
        cursor.execute("""
        INSERT INTO users (username, email, password, role)
        VALUES (?, ?, ?, ?)
        """, (username, email, password, role.value))
        conn.commit()
        return valid, f"Gebruiker '{username}' succesvol geregistreerd."
    except Exception as e:
        return False, f"Registratiefout: {e}"
    finally:
        conn.close()

def update(user_id, username, email, password, role, selected_user):
    conn = get_db_connection()
    cursor = conn.cursor()

    if username != '':
        valid, message = username_checker(username)
        if not valid:
            return valid, message
    else:
        username = selected_user.username

    # MOST LIKELY WILL GET A EMAIL_CHECKER() ASWELL!

    if password != '':
        valid, message = password_checker(password)
        if not valid:
            return valid, message
    else:
        password = selected_user.password_hash
    
    try:
        cursor.execute("""
            UPDATE users
            SET username = ?, email = ?, password = ?, role = ?
            WHERE id = ?
        """, (username, email, password, role.value, user_id))
        conn.commit()
        return True, f"Gebruiker '{username}' succesvol geupdate."
    except Exception as e:
        return False, f"Updatefout: {e}"
    finally:
        conn.close()

def delete(selected_user):
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
        cursor.execute("""
            DELETE FROM users
            WHERE id = ?
        """, (selected_user.user_id,))
        conn.commit()
        return True, f"{SUCCES}Gebruiker '{selected_user.username}' succesvol verwijderd.{RESET}"
    except Exception as e:
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
        id, username, email, password, role_str = row
        role = UserRole(role_str)
        user = User(id, username, password, email, role)
        users.append(user)
    
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]

    conn.close()
    return users, user_count

