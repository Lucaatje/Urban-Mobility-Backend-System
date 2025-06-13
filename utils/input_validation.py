from database.db import get_db_connection
import re
from models.models import User, UserRole


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

def validate_credentials(username, password):
    # Verander dit zodat dit de username en password valideerd en bij success een class user terug stuurd vanuit database.
    # Voorbeeld: return User(1, 'super_admin', 'Admin_123?', 'admin@gmail.com', UserRole.SUPER_ADMIN)
    # Anders None
    return User(1, 'super_admin', 'Admin_123?', 'admin@gmail.com', UserRole.SUPER_ADMIN)

def ZIP_code_checker(zip_code):
    # Check if zip code had 4 digits and 2 letters
    if not re.match(r'^\d{4}[A-Z]{2}$', zip_code):
        return False, "Postcode moet bestaan uit 4 cijfers en 2 hoofdletters (bijv. 1234AB)."

def Mobile_phone_checker(mobile_phone):
    # Check if mobile phone starts has format +31600000000
    if not re.match(r'^\+316\d{8}$', mobile_phone):
        return False, "Mobiel telefoonnummer moet beginnen met +316 en gevolgd worden door 8 cijfers (bijv. +31612345678)."
    
def Driving_license_number_checker(driving_license_number):
    # check if driving license number has either format XX0000000 or X00000000
    if not re.match(r'^[A-Z]{2}\d{7}$', driving_license_number) and not re.match(r'^[A-Z]\d{8}$', driving_license_number):
        return False, "Rijbewijsnummer moet beginnen met 2 hoofdletters en gevolgd worden door 7 cijfers (bijv. AB1234567) of beginnen met 1 hoofdletter en gevolgd worden door 8 cijfers (bijv. A12345678)."