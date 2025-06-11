from database.db import get_db_connection
from utils.input_validation import username_checker, password_checker


def login(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    valid, message = username_checker(username)
    if not valid:
        print(message)
        return None
    
    cursor.execute("SELECT password, role FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if (user and user[0] == password):
        print(f"Ingelogd als {username}, rol: {user[1]}")
    else:
        print("Gebruikersnaam en of wachtwoord verkeerd.")
        return None



def register(username, email, password, role):
    conn = get_db_connection()
    cursor = conn.cursor()

    valid, message = password_checker(password)
    if not valid:
        print(message)
        return None

    try:
        cursor.execute("""
        INSERT INTO users (username, email, password, role)
        VALUES (?, ?, ?, ?)
        """, (username, email, password, role))
        conn.commit()
        print(f"Gebruiker '{username}' succesvol geregistreerd.")
    except Exception as e:
        print("Registratiefout:", e)
    finally:
        conn.close()




