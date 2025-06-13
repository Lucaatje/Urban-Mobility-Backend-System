from database.db import get_db_connection
from utils.input_validation import username_checker, password_checker
from models.models import Traveller
from utils.input_validation import *


def RegisterTraveller(traveller: Traveller):
    conn = get_db_connection()
    cursor = conn.cursor()

    if (ZIP_code_checker(traveller.zip_code)[0] is False):
        print(ZIP_code_checker(traveller.zip_code)[1])
        return
    
    if (Mobile_phone_checker(traveller.mobile_phone)[0] is False):
        print(Mobile_phone_checker(traveller.mobile_phone)[1])
        return
    


    try:
        cursor.execute("""
        INSERT INTO users (first_name, last_name, birthday, gender, street_name, house_number, zip_code, city, email_address, mobile_phone, driving_license_number)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (traveller.first_name, traveller.last_name, traveller.birthday, traveller.gender, traveller.street_name, traveller.house_number, traveller.zip_code, traveller.city, traveller.email_address, traveller.mobile_phone, traveller.driving_license_number))
        conn.commit()
        print(f"Traveller: '{traveller.first_name} {traveller.last_name}' succesvol geregistreerd.")
    except Exception as e:
        print("Registratiefout:", e)
    finally:
        conn.close()
