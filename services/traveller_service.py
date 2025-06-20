from database.db import get_db_connection
from models.models import Traveller
from utils.input_validation import *
import datetime
import os
from utils.data_encryption import encrypt, decrypt


def RegisterTraveller(traveller: Traveller):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO travellers (
            first_name, last_name, birthday, gender,
            street_name, house_number, zip_code, city,
            email_address, mobile_phone, driving_license_number
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            encrypt(traveller.first_name),
            encrypt(traveller.last_name),
            encrypt(traveller.birthday),
            traveller.gender,
            encrypt(traveller.street_name),
            encrypt(traveller.house_number),
            encrypt(traveller.zip_code),
            encrypt(traveller.city),
            encrypt(traveller.email_address),
            encrypt(traveller.mobile_phone),
            encrypt(traveller.driving_license_number),
        ))
        conn.commit()
        print(f"Traveller: '{traveller.first_name} {traveller.last_name}' succesvol geregistreerd.")
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
        return Traveller(
            traveller_id=row[0],
            first_name=decrypt(row[1]),
            last_name=decrypt(row[2]),
            birthday=decrypt(row[3]),
            gender=row[4],
            street_name=decrypt(row[5]),
            house_number=decrypt(row[6]),
            zip_code=decrypt(row[7]),
            city=decrypt(row[8]),
            email_address=decrypt(row[9]),
            mobile_phone=decrypt(row[10]),
            driving_license_number=decrypt(row[11])
        )
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

    try:
        cursor.execute("""
        UPDATE travellers
        SET first_name = ?, last_name = ?, birthday = ?, gender = ?, 
            street_name = ?, house_number = ?, zip_code = ?, city = ?, 
            email_address = ?, mobile_phone = ?, driving_license_number = ?
        WHERE id = ?
        """, (
            encrypt(traveller.first_name),
            encrypt(traveller.last_name),
            encrypt(traveller.birthday),
            traveller.gender,
            encrypt(traveller.street_name),
            encrypt(traveller.house_number),
            encrypt(traveller.zip_code),
            encrypt(traveller.city),
            encrypt(traveller.email_address),
            encrypt(traveller.mobile_phone),
            encrypt(traveller.driving_license_number),
            traveller.id
        ))
        conn.commit()
        print(f"Traveller: '{traveller.first_name} {traveller.last_name}' successfully updated.")
        return True
    except Exception as e:
        print("Update error:", e)
        return False
    finally:
        conn.close()


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
    driving_license_number = getattr(
        existing_traveller, "driving_license_number", None)
    traveller_id = getattr(existing_traveller, "id", None)

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
            first_name = input("Enter first name: ")
        elif match == '2':
            last_name = input("Enter last name: ")
        elif match == '3':
            birthday = Date_verification()
        elif match == '4':
            Gender = Gender_verification()
        elif match == '5':
            street_name = input("Enter street name: ")
        elif match == '6':
            house_number = input("Enter house number: ")
        elif match == '7':
            zip_code = Enter_zipcode()
        elif match == '8':
            city = Enter_city()
        elif match == '9':
            email_address = input("Enter email address: ")
        elif match == '10':
            mobile_phone = Enter_phonenumber()
        elif match == '11':
            driving_license_number = Enter_drivinglicense()
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

    # Check if all required fields are filled
    required_fields = [first_name, last_name, birthday,
                       Gender, email_address, driving_license_number]
    if not all(required_fields):
        print("Not all required fields are filled. Traveller not created/updated.")
        print("Returning to creation menu.")
        return Create_traveller(existing_traveller)

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
    # choose city from 1 to 10
    city = input("Please select your city by number: 1: Amsterdam, 2: Rotterdam, 3: The Hague, 4: Utrecht, 5: Eindhoven 6: Breda, 7: Groningen, 8: Leeuwarden, 9: Papendrecht, 10: Dordrecht \n")
    # change input to city name
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
    city = city_dict.get(city, 'Unknown City')
    if city == 'Unknown City':
        print("Invalid city selection. Please try again.")
        Enter_city()
    return city


def Enter_phonenumber():
    PN = input("Please enter your phone number in the format +31612345678: ")
    if Mobile_phone_checker(PN)[0]:
        return PN
    else:
        print(Mobile_phone_checker(PN)[1])
        return Enter_phonenumber()


def Enter_drivinglicense():
    DL = input(
        "Please enter your driving license number: for example AB1234567 or A12345678: ")
    if Driving_license_number_checker(DL)[0]:
        return DL
    else:
        print(Driving_license_number_checker(DL)[1])
        return Enter_drivinglicense()


def Enter_zipcode():
    zip_code = input("Please enter your zip code in the format 1234AB: ")
    if ZIP_code_checker(zip_code)[0]:
        return zip_code
    else:
        print(ZIP_code_checker(zip_code)[1])
        return Enter_zipcode()


def Date_verification():
    date_str = input("Enter date in DD/MM/YYYY format: ")
    try:
        # Try to parse the date string
        date = datetime.datetime.strptime(date_str, '%d/%m/%Y')
        return date.strftime('%d/%m/%Y')  # Return in DD/MM/YYYY format
    except ValueError:
        print("Invalid date format. Please use DD/MM/YYYY.")
        return Date_verification()


def Gender_verification():
    while True:
        gender = input("Enter gender (M/F): ").strip().upper()
        if gender in ['M', 'F']:
            return 'male' if gender == 'M' else 'female'
        print("Invalid gender. Please enter M for male or F for female.")


def GetAllTravellersId() -> list[dict]:
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, first_name, last_name FROM travellers")
    rows = cursor.fetchall()
    conn.close()

    return [{"id": row[0], "name": f"{decrypt(row[1])} {decrypt(row[2])}"} for row in rows] if rows else []
