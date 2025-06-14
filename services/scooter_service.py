from models.models import Scooter



def add_scooter(scooter: Scooter, db_connection):
    
    conn = db_connection
    cursor = conn.cursor()

    validation_error = validate_scooter_data(scooter)
    if validation_error:
        print(f"Validatiefout: {validation_error}")
        return False

    try:
        cursor.execute("""
            INSERT INTO scooters (
                brand, model, serial_number, top_speed, battery_capacity,
                state_of_charge, target_soc_min, target_soc_max,
                latitude, longitude, out_of_service, mileage, last_maintenance
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            scooter.brand,
            scooter.model,
            scooter.serial_number,
            scooter.top_speed,
            scooter.battery_capacity,
            scooter.state_of_charge,
            scooter.target_soc_range[0],
            scooter.target_soc_range[1],
            scooter.location_lat,
            scooter.location_long,
            int(scooter.out_of_service),
            scooter.mileage,
            scooter.last_maintenance_date
        ))
        db_connection.commit()
        return True

    except Exception as e:
        print(f"Databasefout bij toevoegen scooter: {e}")
        return False



def update_scooter(scooter_id, updated_scooter, db_connection):
    
    conn = db_connection
    cursor = conn.cursor()

    existing_scooter = get_scooter_by_id(scooter_id, db_connection)
    if not existing_scooter:
        print(f"Scooter met ID {scooter_id} bestaat niet.")
        return False
    

    validation_error = validate_scooter_data(updated_scooter)
    if validation_error:
        print(f"Validatiefout: {validation_error}")
        return False

    try:
        cursor.execute("""
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
        """, (
            updated_scooter.brand,
            updated_scooter.model,
            updated_scooter.serial_number,
            updated_scooter.top_speed,
            updated_scooter.battery_capacity,
            updated_scooter.state_of_charge,
            updated_scooter.target_soc_range[0],
            updated_scooter.target_soc_range[1],
            updated_scooter.location_lat,
            updated_scooter.location_long,
            int(updated_scooter.out_of_service),
            updated_scooter.mileage,
            updated_scooter.last_maintenance_date,
            scooter_id
        ))

        db_connection.commit()
        return True

    except Exception as e:
        print(f"❌ Databasefout bij updaten scooter: {e}")
        db_connection.rollback()
        return False




def delete_scooter(scooter_id, db_connection):
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
        print(f"Fout bij verwijderen van scooter: {e}")
        return False



def search_scooters(keyword, db_connection):
    conn = db_connection
    cursor = conn.cursor()
    searchterm = f"%{keyword}%"

    try:
        cursor.execute("""
            SELECT id, brand, model, serial_number, state_of_charge
            FROM scooters
            WHERE brand LIKE ? OR model LIKE ? OR serial_number LIKE ?
        """, (searchterm, searchterm, searchterm))

        resultaten = cursor.fetchall()

        if not resultaten:
            return []

        return resultaten

    except Exception as e:
        print(f"❌ Fout bij zoeken naar scooters: {e}")
        return []



def list_all_scooters(db_connection):
    cursor = db_connection.cursor()
    try:
        cursor.execute("SELECT * FROM scooters")
        scooters = cursor.fetchall()

        if not scooters:
            print("⚠️  Er zijn geen scooters gevonden.")
            return

        return scooters
    
    except Exception as e:
        print(f"❌ Fout bij ophalen van scooters: {e}")



def get_scooter_by_id(scooter_id, db_connection) -> Scooter:
    conn = db_connection
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM scooters WHERE id = ?", (scooter_id,))
    scooter = cursor.fetchone()

    if not scooter:
        print(f"Scooter met ID {scooter_id} bestaat niet.")
        return False

    return scooter




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



