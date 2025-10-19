from models.models import Scooter, UserRole
from logs.logger import write_log
from utils.data_encryption import encrypt, decrypt
from datetime import datetime
import os
from database.db import get_db_connection

def add_scooter(scooter: Scooter):
    
    conn = get_db_connection()
    cursor = conn.cursor()

    validation_error = validate_scooter_data(scooter)
    if validation_error:
        return [False, validation_error]

    try:
        cursor.execute("""
            INSERT INTO scooters (
                brand, model, serial_number, top_speed, battery_capacity,
                state_of_charge, target_soc_min, target_soc_max,
                latitude, longitude, out_of_service, mileage, last_maintenance
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            encrypt(scooter.brand),
            encrypt(scooter.model),
            encrypt(scooter.serial_number),
            encrypt(str(scooter.top_speed)),
            encrypt(str(scooter.battery_capacity)),
            encrypt(str(scooter.state_of_charge)),
            encrypt(str(scooter.target_soc_range[0])),
            encrypt(str(scooter.target_soc_range[1])),
            encrypt(str(scooter.location_lat)),
            encrypt(str(scooter.location_long)),
            int(scooter.out_of_service),  # Booleans en integers hoef je niet te encrypten tenzij gevoelig
            encrypt(str(scooter.mileage)),
            encrypt(scooter.last_maintenance_date)
        ))
        conn.commit()
        return [True, "Scooter successfully added."]

    except Exception as e:
        print(f"Databasefout bij toevoegen scooter: {e}")
        return False
    

def create_scooter(existing_scooter=None):
    scooter_id = getattr(existing_scooter, "scooter_id", None)
    brand = getattr(existing_scooter, "brand", None)
    model = getattr(existing_scooter, "model", None)
    serial_number = getattr(existing_scooter, "serial_number", None)
    top_speed = getattr(existing_scooter, "top_speed", None)
    battery_capacity = getattr(existing_scooter, "battery_capacity", None)
    state_of_charge = getattr(existing_scooter, "state_of_charge", None)
    target_soc_range = getattr(existing_scooter, "target_soc_range", None)
    location_lat = getattr(existing_scooter, "location_lat", None)
    location_long = getattr(existing_scooter, "location_long", None)
    out_of_service = getattr(existing_scooter, "out_of_service", None)
    mileage = getattr(existing_scooter, "mileage", None)
    last_maintenance_date = getattr(existing_scooter, "last_maintenance_date", None)

    while True:
        print(f"\nCurrent values:\n"
              f"Brand: {brand if brand else 'Not set'}\n"
              f"Model: {model if model else 'Not set'}\n"
              f"Serial number: {serial_number if serial_number else 'Not set'}\n"
              f"Top speed: {top_speed if top_speed else 'Not set'}\n"
              f"Battery capacity: {battery_capacity if battery_capacity else 'Not set'}\n"
              f"State of charge: {state_of_charge if state_of_charge else 'Not set'}\n"
              f"Target SoC range: {target_soc_range if target_soc_range else 'Not set'}\n"
              f"Latitude: {location_lat if location_lat else 'Not set'}\n"
              f"Longitude: {location_long if location_long else 'Not set'}\n"
              f"Out of service: {out_of_service if out_of_service is not None else 'Not set'}\n"
              f"Mileage: {mileage if mileage else 'Not set'}\n"
              f"Last maintenance date: {last_maintenance_date if last_maintenance_date else 'Not set'}\n"
              )

        match = input(
            "Enter what you would like to fill in:\n"
            "1: Brand,\n2: Model,\n3: Serial number,\n"
            "4: Top speed (km/h),\n5: Battery capacity (Wh),\n"
            "6: State of charge (%),\n7: Target SoC range (min,max),\n"
            "8: Latitude,\n9: Longitude,\n10: Out of service (True/False),\n"
            "11: Mileage (km),\n12: Last maintenance date (YYYY-MM-DD),\n"
            "13: Continue,\n14: Exit\n"
        ).strip()

        if match == '1':
            brand = input("Enter brand: ").strip().title()
            os.system('cls' if os.name == 'nt' else 'clear')
        elif match == '2':
            model = input("Enter model: ").strip()
            os.system('cls' if os.name == 'nt' else 'clear')
        elif match == '3':
            serial_number = input("Enter serial number (10–17 alphanumeric): ").strip().upper()
            os.system('cls' if os.name == 'nt' else 'clear')
        elif match == '4':
            top_speed = float(input("Enter top speed (km/h): "))
            os.system('cls' if os.name == 'nt' else 'clear')
        elif match == '5':
            battery_capacity = int(input("Enter battery capacity (Wh): "))
            os.system('cls' if os.name == 'nt' else 'clear')
        elif match == '6':
            state_of_charge = float(input("Enter state of charge (%): "))
            os.system('cls' if os.name == 'nt' else 'clear')
        elif match == '7':
            try:
                min_soc = float(input("Enter min SoC (%): "))
                max_soc = float(input("Enter max SoC (%): "))
                target_soc_range = (min_soc, max_soc)
            except ValueError:
                print("Invalid input. Please enter numeric values.")
            os.system('cls' if os.name == 'nt' else 'clear')
        elif match == '8':
            location_lat = float(input("Enter latitude: "))
            os.system('cls' if os.name == 'nt' else 'clear')
        elif match == '9':
            location_long = float(input("Enter longitude: "))
            os.system('cls' if os.name == 'nt' else 'clear')
        elif match == '10':
            val = input("Out of service? (y/n): ").lower()
            out_of_service = val in ("y", "yes", "true", "1")
            os.system('cls' if os.name == 'nt' else 'clear')
        elif match == '11':
            mileage = float(input("Enter mileage (km): "))
            os.system('cls' if os.name == 'nt' else 'clear')
        elif match == '12':
            last_maintenance_date = input("Enter last maintenance date (YYYY-MM-DD): ").strip()
            try:
                datetime.strptime(last_maintenance_date, "%Y-%m-%d")
            except ValueError:
                print("Invalid date format.")
                last_maintenance_date = None
            os.system('cls' if os.name == 'nt' else 'clear')
        elif match == '13':
            print("Continuing to create/update scooter...")
            os.system('cls' if os.name == 'nt' else 'clear')
            break
        elif match == '14':
            print("Exiting scooter creation/update.")
            os.system('cls' if os.name == 'nt' else 'clear')
            return None
        else:
            print("Invalid option. Please try again.")
            os.system('cls' if os.name == 'nt' else 'clear')

    required_fields = [brand, model, serial_number, battery_capacity, state_of_charge]
    if not all(required_fields):
        print("Not all required fields are filled. Scooter not created/updated.")
        print("Returning to creation menu.")
        return create_scooter(existing_scooter)

    scooter = Scooter(
        scooter_id=scooter_id,
        brand=brand,
        model=model,
        serial_number=serial_number,
        top_speed=top_speed,
        battery_capacity=battery_capacity,
        state_of_charge=state_of_charge,
        target_soc_range=target_soc_range,
        location_lat=location_lat,
        location_long=location_long,
        out_of_service=out_of_service,
        mileage=mileage,
        last_maintenance_date=last_maintenance_date
    )
    return scooter


def update_scooter(scooter_id, updated_scooter: Scooter, db, username=None, updated_field=None):
    validation_error = validate_scooter_data(updated_scooter)
    if validation_error:
        print(f"❌ Validatiefout voor veld '{updated_field}': {validation_error}")
        return False
    
    conn = db
    cursor = conn.cursor()

    try:
        query = """
            UPDATE scooters SET
                brand = ?,
                model = ?,
                serial_number = ?,
                top_speed = ?,
                battery_capacity = ?,
                state_of_charge = ?,
                target_soc_min = ?,
                target_soc_max = ?,
                latitude = ?,
                longitude = ?,
                out_of_service = ?,
                mileage = ?,
                last_maintenance = ?
            WHERE id = ?
        """
        cursor.execute(query, (
            encrypt(updated_scooter.brand),
            encrypt(updated_scooter.model),
            encrypt(updated_scooter.serial_number),
            encrypt(str(updated_scooter.top_speed)),
            encrypt(str(updated_scooter.battery_capacity)),
            encrypt(str(updated_scooter.state_of_charge)),
            encrypt(str(updated_scooter.target_soc_range[0])),
            encrypt(str(updated_scooter.target_soc_range[1])),
            encrypt(str(updated_scooter.location_lat)),
            encrypt(str(updated_scooter.location_long)),
            int(updated_scooter.out_of_service),
            encrypt(str(updated_scooter.mileage)),
            encrypt(updated_scooter.last_maintenance_date),
            scooter_id
        ))
        conn.commit()
        return True

    except Exception as e:
        print(f"❌ Databasefout tijdens update van veld '{updated_field}': {e}")
        return False




def delete_scooter(scooter_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    scooter = get_scooter_by_id(scooter_id)
    if not scooter:
        return False

    try:
        cursor.execute("DELETE FROM scooters WHERE id = ?", (scooter_id,))
        conn.commit()
        return True
    
    except Exception as e:
        print(f"Fout bij verwijderen van scooter: {e}")
        return False



def search_scooters(keyword, db_connection):
    conn = db_connection
    cursor = conn.cursor()
    keyword = keyword.lower()

    try:
        cursor.execute("""
            SELECT id, brand, model, serial_number, state_of_charge
            FROM scooters
        """)
        rows = cursor.fetchall()

        resultaten = []
        for row in rows:
            try:
                decrypted_brand = decrypt(row[1])
                decrypted_model = decrypt(row[2])
                decrypted_serial = decrypt(row[3])
                decrypted_soc = int(float(decrypt(row[4])))

                if (keyword in decrypted_brand.lower()
                    or keyword in decrypted_model.lower()
                    or keyword in decrypted_serial.lower()):
                    resultaten.append((
                        row[0], decrypted_brand, decrypted_model, decrypted_serial, decrypted_soc
                    ))
            except Exception as e:
                print(f"❌ Fout bij decryptie tijdens zoeken: {e}")
                continue

        return resultaten

    except Exception as e:
        print(f"❌ Fout bij zoeken naar scooters: {e}")
        return []



def list_all_scooters():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM scooters")
        rows = cursor.fetchall()

        if not rows:
            return []

        scooters = []
        for row in rows:
            try:
                scooter = Scooter(
                    scooter_id=row[0],
                    brand=decrypt(row[1]),
                    model=decrypt(row[2]),
                    serial_number=decrypt(row[3]),
                    top_speed=float(decrypt(row[4])),
                    battery_capacity=float(decrypt(row[5])),
                    state_of_charge=int(float(decrypt(row[6]))),
                    target_soc_range=(
                        int(float(decrypt(row[7]))),
                        int(float(decrypt(row[8])))
                    ),
                    location_lat=float(decrypt(row[9])),
                    location_long=float(decrypt(row[10])),
                    out_of_service=bool(row[11]),
                    mileage=float(decrypt(row[12])),
                    last_maintenance_date=decrypt(row[13])
                )
                scooters.append(scooter)
            except Exception as e:
                print(f"Fout bij decryptie scooter in lijst: {e}")
                continue

        return scooters

    except Exception as e:
        print(f"Fout bij ophalen van scooters: {e}")
        return []



def get_scooter_by_id(scooter_id, db):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM scooters WHERE id = ?", (scooter_id,))
    row = cursor.fetchone()

    if row:
        return Scooter(
            scooter_id=row[0],
            brand=decrypt(row[1]),
            model=decrypt(row[2]),
            serial_number=decrypt(row[3]),
            top_speed=float(decrypt(row[4])),
            battery_capacity=float(decrypt(row[5])),
            state_of_charge=int(float(decrypt(row[6]))),
            target_soc_range=(
                int(float(decrypt(row[7]))),
                int(float(decrypt(row[8])))
            ),
            location_lat=float(decrypt(row[9])),
            location_long=float(decrypt(row[10])),
            out_of_service=bool(row[11]),
            mileage=float(decrypt(row[12])),
            last_maintenance_date=decrypt(row[13])
        )
    return None



def get_editable_attributes_by_role(role):
    if role == UserRole.SERVICE_ENGINEER:
        return [
            "state_of_charge",
            "target_soc",
            "range_km",
            "location",
            "out_of_service",
            "mileage",
            "last_maintenance_date"
        ]
    else:
        return [
            "brand",
            "model",
            "serial_number",
            "top_speed",
            "battery_capacity",
            "state_of_charge",
            "target_soc",
            "range_km",
            "location",
            "out_of_service",
            "mileage",
            "last_maintenance_date"
        ]



def validate_scooter_data(scooter: Scooter) -> str | None:

    if not (10 <= len(scooter.serial_number) <= 17) or not scooter.serial_number.isalnum():
        return "Serienummer moet 10–17 alfanumerieke tekens bevatten."
    

    if not (0 <= scooter.state_of_charge <= 100):
        return "State of Charge (SoC) moet tussen 0 en 100% liggen."

    if not isinstance(scooter.target_soc_range, tuple) or len(scooter.target_soc_range) != 2:
        return "Target SoC Range moet een tuple zijn van (min, max)."

    min_soc, max_soc = scooter.target_soc_range
    if not (0 <= min_soc < max_soc <= 100):
        return "Target SoC Range moet geldig zijn en tussen 0 en 100% liggen."

    if not (51.85 <= scooter.location_lat <= 52.00 and 4.25 <= scooter.location_long <= 4.60):
        return "Locatie moet binnen regio Rotterdam liggen."

    from datetime import datetime
    try:
        datetime.strptime(scooter.last_maintenance_date, "%Y-%m-%d")
    except (ValueError, TypeError):
        return "Datum laatste onderhoud moet in formaat YYYY-MM-DD zijn."

    return None



