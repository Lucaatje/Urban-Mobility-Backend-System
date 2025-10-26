import re
from database.db import get_db_connection


def is_username_unique(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT 1 FROM users WHERE LOWER(username) = LOWER(?)", (username,))
    username_exists = cursor.fetchone() is not None
    conn.close()
    return not username_exists


def username_checker(username):
    # if not (8 <= len(username) <= 10):
    #     return False, "Username moet tussen 8 en 10 karakters lang zijn."

    # # Start met letter of underscore
    # if not re.match(r'^[A-Za-z_]', username):
    #     return False, "Username moet beginnen met een letter of underscore (_)."

    # # Toegestane karakters: letters, cijfers, underscore, apostrof, punt
    # if not re.match(r"^[A-Za-z0-9_.'']+$", username):
    #     return False, "Username mag alleen letters, cijfers, _, ', en . bevatten."

    # # Check uniciteit (case-insensitive)
    # if not is_username_unique(username):
    #     return False, "Username bestaat al."

    # return True, "Username is geldig."
    check_1 = (8 <= len(username) <= 10)
    check_2 = re.match(r'^[A-Za-z_]', username)
    check_3 = re.match(r"^[A-Za-z0-9_.'']+$", username)
    check_4 = is_username_unique(username)

    # generate response message based on first expression that returns False.
    response_message = ""
    if not check_1: response_message = "Username moet tussen 8 en 10 karakters lang zijn."
    elif not check_2: response_message = "Username moet beginnen met een letter of underscore (_)."
    elif not check_3: response_message = "Username mag alleen letters, cijfers, _, ', en . bevatten."
    elif not check_4: response_message = "Username bestaat al."
    else: response_message = "Username is geldig."
    
    if check_1 and check_2 and check_3 and check_4:
        return True, response_message
    else:
        return False, response_message


def password_checker(password):
    # # Lengte check
    # if not (12 <= len(password) <= 30):
    #     return False, "Wachtwoord moet tussen 12 en 30 karakters lang zijn."

    # # Minimaal één kleine letter
    # if not re.search(r'[a-z]', password):
    #     return False, "Wachtwoord moet minimaal één kleine letter bevatten."

    # # Minimaal één hoofdletter
    # if not re.search(r'[A-Z]', password):
    #     return False, "Wachtwoord moet minimaal één hoofdletter bevatten."

    # # Minimaal één cijfer
    # if not re.search(r'\d', password):
    #     return False, "Wachtwoord moet minimaal één cijfer bevatten."

    # # Minimaal één speciaal teken (zoals aangegeven)
    # if not re.search(r'[~!@#$%&_\-\+=`|\\()\{\}\[\]:;\'<>,\.?\/]', password):
    #     return False, "Wachtwoord moet minimaal één speciaal teken bevatten."

    # return True, "Wachtwoord is geldig."
    check_1 = (12 <= len(password) <= 30)
    check_2 = re.search(r'[a-z]', password)
    check_3 = re.search(r'[A-Z]', password)
    check_4 = re.search(r'\d', password)
    check_5 = re.search(r'[~!@#$%&_\-\+=`|\\()\{\}\[\]:;\'<>,\.?\/]', password)
    
    # generate response message based on first expression that returns False.
    response_message = ""
    if not check_1: response_message = "Wachtwoord moet tussen 12 en 30 karakters lang zijn."
    elif not check_2: response_message = "Wachtwoord moet minimaal één kleine letter bevatten."
    elif not check_3: response_message = "Wachtwoord moet minimaal één hoofdletter bevatten."
    elif not check_4: response_message = "Wachtwoord moet minimaal één cijfer bevatten."
    elif not check_5: response_message = "Wachtwoord moet minimaal één speciaal teken bevatten."
    else: response_message = "Wachtwoord is geldig."
    
    if check_1 and check_2 and check_3 and check_4 and check_5:
        return True, response_message
    else:
        return False, response_message


def ZIP_code_checker(zip_code):
    # Check if zip code had 4 digits and 2 letters
    if not re.match(r'^\d{4}[A-Z]{2}$', zip_code):
        return False, "Postcode moet bestaan uit 4 cijfers en 2 hoofdletters (bijv. 1234AB)."
    return True, "Postcode is geldig."


def Mobile_phone_checker(mobile_phone):
    # Check if mobile phone starts has format +31600000000
    if not re.match(r'^\+316\d{8}$', mobile_phone):
        return False, "Mobiel telefoonnummer moet beginnen met +316 en gevolgd worden door 8 cijfers (bijv. +31612345678)."
    return True, "Mobiel telefoonnummer is geldig."


def Driving_license_number_checker(driving_license_number):
    # check if driving license number has either format XX0000000 or X00000000
    if not re.match(r'^[A-Z]{2}\d{7}$', driving_license_number) and not re.match(r'^[A-Z]\d{8}$', driving_license_number):
        return False, "Rijbewijsnummer moet beginnen met 2 hoofdletters en gevolgd worden door 7 cijfers (bijv. AB1234567) of beginnen met 1 hoofdletter en gevolgd worden door 8 cijfers (bijv. A12345678)."
    return True, "Rijbewijsnummer is geldig."
