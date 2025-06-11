from database.db import get_db_connection
import re


def is_username_unique(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM users WHERE LOWER(username) = LOWER(?)", (username,))
    username_exists = cursor.fetchone() is not None
    conn.close()
    return not username_exists


def username_checker(username):
    if not (8 <= len(username) <= 10):
        return False, "Username moet tussen 8 en 10 karakters lang zijn."
    
    # Start met letter of underscore
    if not re.match(r'^[A-Za-z_]', username):
        return False, "Username moet beginnen met een letter of underscore (_)."
    
    # Toegestane karakters: letters, cijfers, underscore, apostrof, punt
    if not re.match(r"^[A-Za-z0-9_.'']+$", username):
        return False, "Username mag alleen letters, cijfers, _, ', en . bevatten."
    
    # Check uniciteit (case-insensitive)
    if not is_username_unique(username):
        return False, "Username bestaat al."
    
    return True, "Username is geldig."


def password_checker(password):
    # Lengte check
    if not (12 <= len(password) <= 30):
        return False, "Wachtwoord moet tussen 12 en 30 karakters lang zijn."

    # Minimaal één kleine letter
    if not re.search(r'[a-z]', password):
        return False, "Wachtwoord moet minimaal één kleine letter bevatten."

    # Minimaal één hoofdletter
    if not re.search(r'[A-Z]', password):
        return False, "Wachtwoord moet minimaal één hoofdletter bevatten."

    # Minimaal één cijfer
    if not re.search(r'\d', password):
        return False, "Wachtwoord moet minimaal één cijfer bevatten."

    # Minimaal één speciaal teken (zoals aangegeven)
    if not re.search(r'[~!@#$%&_\-\+=`|\\()\{\}\[\]:;\'<>,\.?\/]', password):
        return False, "Wachtwoord moet minimaal één speciaal teken bevatten."

    return True, "Wachtwoord is geldig."



    


