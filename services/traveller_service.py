from database.db import get_db_connection
from models.models import Traveller
from utils.input_validation import *


def RegisterTraveller(traveller: Traveller):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO travellers (first_name, last_name, birthday, gender, street_name, house_number, zip_code, city, email_address, mobile_phone, driving_license_number)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (traveller.first_name, traveller.last_name, traveller.birthday, traveller.gender, traveller.street_name, traveller.house_number, traveller.zip_code, traveller.city, traveller.email_address, traveller.mobile_phone, traveller.driving_license_number))
        conn.commit()
        print(
            f"Traveller: '{traveller.first_name} {traveller.last_name}' succesvol geregistreerd.")
    except Exception as e:
        print("Registratiefout:", e)
    finally:
        conn.close()


def GetTravellerById(traveller_id: int) -> Traveller:
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM travellers WHERE id = ?", (traveller_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return Traveller(*row)
    else:
        print(f"Traveller with ID {traveller_id} not found.")
        return None


def DeleteTravellerById(traveller_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM travellers WHERE id = ?", (traveller_id,))
    conn.commit()
    conn.close()

    if cursor.rowcount > 0:
        return True
    else:
        return False


def UpdateTraveller(traveller: Traveller) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()

    if GetTravellerById(traveller.id) is None:
        print(f"Traveller with ID {traveller.id} not found.")
        return False

    # Update everything except ID
    try:
        cursor.execute("""
        UPDATE travellers
        SET first_name = ?, last_name = ?, birthday = ?, gender = ?, street_name = ?, house_number = ?, zip_code = ?, city = ?, email_address = ?, mobile_phone = ?, driving_license_number = ?
        WHERE id = ?
        """, (traveller.first_name, traveller.last_name, traveller.birthday, traveller.gender, traveller.street_name, traveller.house_number, traveller.zip_code, traveller.city, traveller.email_address, traveller.mobile_phone, traveller.driving_license_number, traveller.id))
        conn.commit()
        print(
            f"Traveller: '{traveller.first_name} {traveller.last_name}' successfully updated.")
        return True
    except Exception as e:
        print("Update error:", e)
        return False
    finally:
        conn.close()
