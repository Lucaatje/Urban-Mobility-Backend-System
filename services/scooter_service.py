from models.models import Scooter, UserRole
from logs.logger import write_log
from utils.data_encryption import encrypt, decrypt



def add_scooter(scooter: Scooter, db_connection, username="unknown"):
    
    conn = db_connection
    cursor = conn.cursor()

    validation_error = validate_scooter_data(scooter)
    if validation_error:
        print(f"Validation error: {validation_error}")
        return False

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
        db_connection.commit()
        return True

    except Exception as e:
        print(f"Database error while adding scooter: {e}")
        return False



def update_scooter(scooter_id, updated_scooter: Scooter, db, username=None, updated_field=None):
    validation_error = validate_scooter_data(updated_scooter)
    if validation_error:
        print(f"Validation error for field '{updated_field}': {validation_error}")
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
        print(f"Database error while updating field '{updated_field}': {e}")
        return False




def delete_scooter(scooter_id, db_connection, username="unknown"):
    conn = db_connection
    cursor = conn.cursor()
    
    scooter = get_scooter_by_id(scooter_id, db_connection)
    if not scooter:
        return False

    try:
        cursor.execute("DELETE FROM scooters WHERE id = ?", (scooter_id,))
        conn.commit()
        return True
    
    except Exception as e:
        print(f"Error while deleting scooter: {e}")
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
                print(f"Error during decryption while searching: {e}")
                continue

        return resultaten

    except Exception as e:
        print(f"Error while searching for scooters: {e}")
        return []



def list_all_scooters(db_connection, username="unknown"):
    cursor = db_connection.cursor()
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
                print(f"Error during scooter decryption in list: {e}")
                continue

        return scooters

    except Exception as e:
        write_log(username, "Failed to list scooters", str(e), suspicious=True)
        print(f"Error while retrieving scooters: {e}")
        return []



def get_scooter_by_id(scooter_id, db):
    cursor = db.cursor()
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
        return "Serial number must be 10–17 alphanumeric characters."

    if not (0 <= scooter.state_of_charge <= 100):
        return "State of Charge (SoC) must be between 0 and 100%."

    if not isinstance(scooter.target_soc_range, tuple) or len(scooter.target_soc_range) != 2:
        return "Target SoC Range must be a tuple of (min, max)."

    min_soc, max_soc = scooter.target_soc_range
    if not (0 <= min_soc < max_soc <= 100):
        return "Target SoC Range must be valid and between 0 and 100%."

    if not (51.85 <= scooter.location_lat <= 52.00 and 4.25 <= scooter.location_long <= 4.60):
        return "Location must be within the Rotterdam region."

    from datetime import datetime
    try:
        datetime.strptime(scooter.last_maintenance_date, "%Y-%m-%d")
    except (ValueError, TypeError):
        return "Last maintenance date must be in the format YYYY-MM-DD."

    return None



