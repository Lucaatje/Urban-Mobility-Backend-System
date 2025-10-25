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
    

def create_scooter(existing_scooter=None, user_role=None):
    from models.models import UserRole  
    editable_fields = get_editable_attributes_by_role(user_role)

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

        option_map = {
            "1": ("brand", "Brand"),
            "2": ("model", "Model"),
            "3": ("serial_number", "Serial number"),
            "4": ("top_speed", "Top speed (km/h)"),
            "5": ("battery_capacity", "Battery capacity (Wh)"),
            "6": ("state_of_charge", "State of charge (%)"),
            "7": ("target_soc_range", "Target SoC range (min,max)"),
            "8": ("location_lat", "Latitude"),
            "9": ("location_long", "Longitude"),
            "10": ("out_of_service", "Out of service (True/False)"),
            "11": ("mileage", "Mileage (km)"),
            "12": ("last_maintenance_date", "Last maintenance date (YYYY-MM-DD)")
        }

        available_options = []
        print("Enter what you would like to fill in:")
        for num, (attr, label) in option_map.items():
            
            if any(key in attr for key in editable_fields):
                print(f"{num}: {label}")
                available_options.append(num)

        print("13: Continue")
        print("14: Exit")

        match = input("Select an option: ").strip()

        if match not in available_options + ["13", "14"]:
            print("You do not have permission to edit this field or invalid option.")
            continue

        if match == '1':
            brand = get_valid_input("Enter brand: ").title()
            os.system('cls' if os.name == 'nt' else 'clear')
        elif match == '2':
            model = get_valid_input("Enter model: ")
            os.system('cls' if os.name == 'nt' else 'clear')
        elif match == '3':
            serial_number = get_valid_input("Enter serial number (10–17 alphanumeric): ").upper()
            os.system('cls' if os.name == 'nt' else 'clear')
        elif match == '4':
            top_speed = get_valid_input("Enter top speed (km/h): ", float)
            os.system('cls' if os.name == 'nt' else 'clear')
        elif match == '5':
            battery_capacity = get_valid_input("Enter battery capacity (Wh): ", int)
            os.system('cls' if os.name == 'nt' else 'clear')
        elif match == '6':
            state_of_charge = get_valid_input("Enter state of charge (%): ", float)
            os.system('cls' if os.name == 'nt' else 'clear')
        elif match == '7':
            try:
                min_soc = get_valid_input("Enter min SoC (%): ", float)
                max_soc = get_valid_input("Enter max SoC (%): ", float)
                target_soc_range = (min_soc, max_soc)
            except ValueError:
                print("Invalid input. Please enter numeric values.")
            os.system('cls' if os.name == 'nt' else 'clear')
        elif match == '8':
            location_lat = get_valid_input("Enter latitude: ", float)
            os.system('cls' if os.name == 'nt' else 'clear')
        elif match == '9':
            location_long = get_valid_input("Enter longitude: ", float)
            os.system('cls' if os.name == 'nt' else 'clear')
        elif match == '10':
            val = input("Out of service? (y/n): ").lower()
            out_of_service = val in ("y", "yes", "true", "1")
            os.system('cls' if os.name == 'nt' else 'clear')
        elif match == '11':
            mileage = get_valid_input("Enter mileage (km): ", float)
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
            required_fields = {
                "Brand": brand,
                "Model": model,
                "Serial number": serial_number,
                "Top speed": top_speed,
                "Battery capacity": battery_capacity,
                "State of charge": state_of_charge,
                "Target SoC range": target_soc_range,
                "Latitude": location_lat,
                "Longitude": location_long,
                "Out of service": out_of_service,
                "Mileage": mileage,
                "Last maintenance date": last_maintenance_date
            }

            missing = [field for field, value in required_fields.items() if value in (None, "", [])]

            if missing:
                print("\nYou must fill in all required fields before continuing:")
                for field in missing:
                    print(f" - {field}")
                input("\nPress Enter to return and complete the missing fields...")
                continue 
            else:
                print("\nAll fields complete. Continuing...")
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

def update_scooter(scooter_id, updated_scooter: Scooter, updated_field=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    validation_error = validate_scooter_data(updated_scooter)
    if validation_error:
        print(f"❌ Validatiefout voor veld '{updated_field}': {validation_error}")
        return False
 
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



def search_scooters(keyword):
    conn = get_db_connection()
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



def get_scooter_by_id(scooter_id):
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


def get_all_scooters() -> list[dict]:
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, brand, model, serial_number FROM scooters")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return []

    scooters = []
    for row in rows:
        try:
            scooter_id = row[0]
            brand = decrypt(row[1])
            model = decrypt(row[2])
            serial = decrypt(row[3])
            scooters.append({
                "id": scooter_id,
                "name": f"{brand} {model} ({serial})"
            })
        except Exception as e:
            print(f"Error decrypting scooter data (id={row[0]}): {e}")
            continue

    return scooters


def get_valid_input(prompt, value_type=str, allow_empty=False):
    while True:
        user_input = input(prompt).strip()
        if not user_input:
            if allow_empty:
                return None
            print("This field cannot be empty.")
            continue

        if value_type == str:
            return user_input
        elif value_type == float:
            try:
                return float(user_input)
            except ValueError:
                print("Please enter a valid number.")
        elif value_type == int:
            try:
                return int(user_input)
            except ValueError:
                print("Please enter a valid integer.")
        else:
            return user_input


def validate_scooter_data(scooter: Scooter) -> str | None:

    if not (10 <= len(scooter.serial_number) <= 17) or not scooter.serial_number.isalnum():
        return "Serial number must contain 10–17 alphanumeric characters."
    
    if not (0 <= scooter.state_of_charge <= 100):
        return "State of Charge (SoC) must be between 0 and 100%."

    if not isinstance(scooter.target_soc_range, tuple) or len(scooter.target_soc_range) != 2:
        return "Target SoC range must be a tuple of (min, max)."

    min_soc, max_soc = scooter.target_soc_range
    if not (0 <= min_soc < max_soc <= 100):
        return "Target SoC range must be valid and between 0 and 100%."

    if not (51.85 <= scooter.location_lat <= 52.00 and 4.25 <= scooter.location_long <= 4.60):
        return "Location must be within the Rotterdam region."

    from datetime import datetime
    try:
        datetime.strptime(scooter.last_maintenance_date, "%Y-%m-%d")
    except (ValueError, TypeError):
        return "Last maintenance date must be in the format YYYY-MM-DD."

    return None
