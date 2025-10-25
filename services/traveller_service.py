from database.db import get_db_connection
from models.models import Traveller
from utils.input_validation import *
import datetime
import os
import re

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


# Whitelist patterns (adjust as needed)
NAME_REGEX = re.compile(r"^[A-Za-zÀ-ÖØ-öø-ÿ' \-]{1,50}$")
STREET_REGEX = re.compile(r"^[A-Za-z0-9À-ÖØ-öø-ÿ' \-]{1,80}$")
HOUSE_REGEX = re.compile(r"^[A-Za-z0-9\/\-]{1,10}$")
EMAIL_MAX_LEN = 254
PHONE_MAX_LEN = 20
DL_MAX_LEN = 20

def _valid_name(value: str) -> bool:
    return bool(value) and len(value) <= 50 and NAME_REGEX.match(value)

def _valid_street(value: str) -> bool:
    return bool(value) and len(value) <= 80 and STREET_REGEX.match(value)

def _valid_house(value: str) -> bool:
    return bool(value) and len(value) <= 10 and HOUSE_REGEX.match(value)

def _valid_email(value: str) -> bool:
    return bool(value) and len(value) <= EMAIL_MAX_LEN  # assume input_validation.email checker used elsewhere


def Create_traveller(existing_traveller=None):
    # Use existing values if provided, otherwise None
    first_name = getattr(existing_traveller, "first_name", None)
    last_name = getattr(existing_traveller, "last_name", None)
    birthday = getattr(existing_traveller, "birthday", None)
    Gender = getattr(existing_traveller, "gender", None)
    street_name = getattr(existing_traveller, "street_name", None)
    house_number = getattr(existing_traveller, "house_number", None)
    zip_code = getattr(existing_traveller, "zip_code", None)
    city = getattr(existing_traveller, "city", None)
    email_address = getattr(existing_traveller, "email_address", None)
    mobile_phone = getattr(existing_traveller, "mobile_phone", None)
    driving_license_number = getattr(existing_traveller, "driving_license_number", None)
    traveller_id = getattr(existing_traveller, "id", None)

    while True:  # outer loop: keeps returning to the form instead of recursion
        loop = True
        while loop:
            print(f"\nCurrent values:\n"
                  f"First name: {first_name if first_name else 'Not set'}\n"
                  f"Last name: {last_name if last_name else 'Not set'}\n"
                  f"Birthday: {birthday if birthday else 'Not set'}\n"
                  f"Gender: {Gender if Gender else 'Not set'}\n"
                  f"Street name: {street_name if street_name else 'Not set'}\n"
                  f"House number: {house_number if house_number else 'Not set'}\n"
                  f"Zip code: {zip_code if zip_code else 'Not set'}\n"
                  f"City: {city if city else 'Not set'}\n"
                  f"Email address: {email_address if email_address else 'Not set'}\n"
                  f"Mobile phone: {mobile_phone if mobile_phone else 'Not set'}\n"
                  f"Driving license number: {driving_license_number if driving_license_number else 'Not set'}\n"
                  )
            match = input(
                "Enter what you would like to fill in:\n"
                "1: First name,\n2: Last name,\n3: Birthday,\n"
                "4: Gender,\n5: Street name,\n6: House number,\n"
                "7: Zip code,\n8: City,\n9: Email address,\n10: Mobile phone,\n"
                "11: Driving license number,\n12: Continue\n13: Exit\n"
            ).strip()

            if match == '1':
                val = input("Enter first name (or 'q' to cancel): ")
                if val.lower() == 'q': return None
                first_name = val
            elif match == '2':
                val = input("Enter last name (or 'q' to cancel): ")
                if val.lower() == 'q': return None
                last_name = val
            elif match == '3':
                val = Date_verification()
                if val is None: return None
                birthday = val
            elif match == '4':
                val = Gender_verification()
                if val is None: return None
                Gender = val
            elif match == '5':
                val = input("Enter street name (or 'q' to cancel): ")
                if val.lower() == 'q': return None
                street_name = val
            elif match == '6':
                val = input("Enter house number (or 'q' to cancel): ")
                if val.lower() == 'q': return None
                house_number = val
            elif match == '7':
                val = Enter_zipcode()
                if val is None: return None
                zip_code = val
            elif match == '8':
                val = Enter_city()
                if val is None: return None
                city = val
            elif match == '9':
                val = input("Enter email address (or 'q' to cancel): ")
                if val.lower() == 'q': return None
                email_address = val
            elif match == '10':
                val = Enter_phonenumber()
                if val is None: return None
                mobile_phone = val
            elif match == '11':
                val = Enter_drivinglicense()
                if val is None: return None
                driving_license_number = val
            elif match == '12':
                print("Continuing to create/update traveller...")
                loop = False
                os.system('cls' if os.name == 'nt' else 'clear')  # Clear console
            elif match == '13':
                print("Exiting traveller creation/update.")
                os.system('cls' if os.name == 'nt' else 'clear')  # Clear console
                return None
            else:
                print("Invalid option. Please try again.")

        # Whitelist / sanity checks (deny-by-default)
        if not _valid_name(first_name):
            print("Invalid first name. Allowed: letters, spaces, hyphen, max 50 chars.")
            continue  # go back to the form
        if not _valid_name(last_name):
            print("Invalid last name. Allowed: letters, spaces, hyphen, max 50 chars.")
            continue
        if not isinstance(birthday, str) or len(birthday) == 0:
            print("Invalid birthday.")
            continue
        if Gender not in ('male', 'female'):
            print("Invalid gender.")
            continue
        if street_name and not _valid_street(street_name):
            print("Invalid street name.")
            continue
        if house_number and not _valid_house(house_number):
            print("Invalid house number.")
            continue
        if email_address and len(email_address) > EMAIL_MAX_LEN:
            print("Email too long.")
            continue
        # phone and driving license are validated in Enter_* helpers

        # All checks passed: build traveller
        traveller = Traveller(
            traveller_id=traveller_id,  # Use existing ID if updating
            first_name=first_name,
            last_name=last_name,
            birthday=birthday,
            gender=Gender,
            street_name=street_name,
            house_number=house_number,
            zip_code=zip_code,
            city=city,
            email_address=email_address,
            mobile_phone=mobile_phone,
            driving_license_number=driving_license_number
        )
        return traveller


def Enter_city():
    city_dict = {
        '1': 'Amsterdam',
        '2': 'Rotterdam',
        '3': 'The Hague',
        '4': 'Utrecht',
        '5': 'Eindhoven',
        '6': 'Breda',
        '7': 'Groningen',
        '8': 'Leeuwarden',
        '9': 'Papendrecht',
        '10': 'Dordrecht'
    }
    while True:
        print("\nSelect a city (or 'q' to cancel):")
        for key, name in city_dict.items():
            print(f"  {key}: {name}")
        city = input("Please select your city by number: ").strip()
        if city.lower() == 'q':
            return None
        city_name = city_dict.get(city)
        if city_name:
            print(f"Selected city: {city_name}")
            return city_name
        print("Invalid city selection. Please try again.")


def Enter_phonenumber():
    while True:
        PN = input("Please enter your phone number in the format +31612345678 (or 'q' to cancel): ")
        if PN.lower() == 'q':
            return None
        valid, msg = Mobile_phone_checker(PN)
        if valid:
            return PN
        print(msg)


def Enter_drivinglicense():
    while True:
        DL = input("Please enter your driving license number (or 'q' to cancel): for example AB1234567 or A12345678")
        if DL.lower() == 'q':
            return None
        valid, msg = Driving_license_number_checker(DL)
        if valid:
            return DL
        print(msg)


def Enter_zipcode():
    while True:
        zip_code = input("Please enter your zip code in the format 1234AB (or 'q' to cancel): ")
        if zip_code.lower() == 'q':
            return None
        valid, msg = ZIP_code_checker(zip_code)
        if valid:
            return zip_code
        print(msg)


def Date_verification():
    while True:
        date_str = input("Enter date in DD/MM/YYYY format (or 'q' to cancel): ")
        if date_str.lower() == 'q':
            return None
        try:
            date = datetime.datetime.strptime(date_str, '%d/%m/%Y')
            return date.strftime('%d/%m/%Y')
        except ValueError:
            print("Invalid date format. Please use DD/MM/YYYY.")


def Gender_verification():
    while True:
        gender = input("Enter gender (M/F) (or 'q' to cancel): ").strip().upper()
        if gender.lower() == 'Q':
            return None
        if gender in ['M', 'F']:
            return 'male' if gender == 'M' else 'female'
        print("Invalid gender. Please enter M for male or F for female.")


def GetAllTravellersId() -> list[dict]:
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, first_name, last_name FROM travellers")
    rows = cursor.fetchall()
    conn.close()

    # Return a list of dicts with id and name
    return [{"id": row[0], "name": f"{row[1]} {row[2]}"} for row in rows] if rows else []
