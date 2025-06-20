from database.db import get_db_connection
from utils.commands_ui import clear_console
from models.models import Scooter, UserRole
from logs.logger import write_log
from services.scooter_service import get_editable_attributes_by_role
from services.scooter_service import get_scooter_by_id, search_scooters
from services.scooter_service import (
    add_scooter,
    update_scooter,
    delete_scooter,
    list_all_scooters
)
from utils.data_encryption import decrypt

def manage_scooter_information(logged_in_user):
    clear_console()
    print("Scooter Management\n")
    print("1. Add a new scooter")
    print("2. Update an existing scooter")
    print("3. Delete a scooter")
    print("4. Show all scooters")
    print("5. Search scooters by keyword")
    choice = input("\nChoose an option (1-4): ")

    db = get_db_connection()

    encrypted_username = logged_in_user.username
    username = decrypt(encrypted_username)

    if choice == "1":
        if logged_in_user.role == UserRole.SERVICE_ENGINEER:
            print("You do not have permission to add scooters.")
            input("Press Enter to return...")
            return

        scooter_id = None

        brand = input("Brand: ")
        model = input("Model: ")
        serial_number = input("Serial Number (10–17 alphanumeric): ")
        top_speed = input("Top Speed (km/h): ")
        battery_capacity = input("Battery Capacity (Wh): ")
        state_of_charge = input("Current SoC (%): ")

        try:
            soc_min = float(input("Target SoC Minimum (%): "))
            soc_max = float(input("Target SoC Maximum (%): "))
        except ValueError:
            print("Invalid input for SoC range.")
            input("Press Enter to return...")
            return

        target_soc_range = (soc_min, soc_max)
        latitude = input("Latitude: ")
        longitude = input("Longitude: ")
        out_of_service = input("Out of service? (yes/no): ").lower() in ['yes', 'ja', 'true']
        mileage = input("Mileage (km): ")
        last_maintenance_date = input("Last Maintenance Date (YYYY-MM-DD): ")

        try:
            scooter = Scooter(
                scooter_id,
                brand,
                model,
                serial_number,
                top_speed,
                battery_capacity,
                state_of_charge,
                target_soc_range,
                latitude,
                longitude,
                out_of_service,
                mileage,
                last_maintenance_date
            )
        except Exception as e:
            print(f"\nFailed to create Scooter object: {e}")
            input("Press Enter to return...")
            return

        if add_scooter(scooter, db):
            print("\nScooter added.")
            write_log(username, "Added new scooter", f"Serial: {scooter.serial_number}", suspicious=False)
        else:
            print("\nFailed to add scooter.")
            write_log(username, "Failed to add scooter", str(e), suspicious=True)

        input("\nPress Enter to return...")
        return

    elif choice == "2":
        try:
            scooter_id = int(input("Enter the ID of the scooter you want to update: "))
        except ValueError:
            print("Invalid ID format.")
            input("Press Enter to return...")
            return

        existing_scooter = get_scooter_by_id(scooter_id, db)
        if not existing_scooter:
            write_log(logged_in_user.username, "Attempted to update non-existent scooter", f"ID: {scooter_id}", suspicious=True)
            print(f"Scooter ID {scooter_id} bestaat niet.")
            input("Press Enter to return...")
            return

        editable_fields = get_editable_attributes_by_role(logged_in_user.role)

        print("\n📋 Choose which attribute you want to update:")
        for i, attr in enumerate(editable_fields, 1):
            print(f"{i}. {attr.replace('_', ' ').title()}")

        try:
            field_choice = int(input("\nNummer van veld: "))
            if field_choice < 1 or field_choice > len(editable_fields):
                raise ValueError
        except ValueError:
            print("Invalid choice.")
            input("Press Enter to return...")
            return

        selected_field = editable_fields[field_choice - 1]
        updates = {}

        if selected_field == "target_soc":
            try:
                min_val = float(input("Nieuwe minimum SoC (%): "))
                max_val = float(input("Nieuwe maximum SoC (%): "))
                updates[selected_field] = (min_val, max_val)
            except ValueError:
                print("Invalid input for SoC range.")
                input("Press Enter to return...")
                return
        elif selected_field == "location":
            lat = input("Latitude: ")
            lon = input("Longitude: ")
            updates[selected_field] = (lat, lon)
        elif selected_field == "out_of_service":
            updates[selected_field] = input("Out of service? (yes/no): ").lower() in ['yes', 'ja', 'true']
        elif selected_field in ["state_of_charge", "range_km", "mileage"]:
            try:
                updates[selected_field] = float(input(f"Nieuwe waarde voor '{selected_field}': "))
            except ValueError:
                print("Invalid numeric input.")
                input("Press Enter to return...")
                return
        else:
            updates[selected_field] = input(f"New value for '{selected_field}': ")
        
        
        if selected_field == "target_soc":
            existing_scooter.target_soc_range = updates[selected_field]
        elif selected_field == "location":
            existing_scooter.location_lat = float(updates[selected_field][0])
            existing_scooter.location_long = float(updates[selected_field][1])
        else:
            setattr(existing_scooter, selected_field, updates[selected_field])


        # En valideer + sla op
        success = update_scooter(scooter_id, existing_scooter, db, username=logged_in_user.username, updated_field=selected_field)

        if success:
            print("\nScooter successfully updated.")
            write_log(username, f"Updated scooter field '{selected_field}'", f"Scooter ID: {scooter_id}", suspicious=False)
        else:
            print("\nFailed to update scooter.")
            write_log(username, f"Tried updating scooter field '{selected_field}'", f"Scooter ID: {scooter_id}", suspicious=True)

        input("\nPress Enter to return...")
        return

    elif choice == "3":
        if logged_in_user.role == UserRole.SERVICE_ENGINEER:
            print("You do not have permission to delete scooters.")
            write_log(username, f"Attempted to delete scooter with no permission", f"ID: {scooter_id}", suspicious=True)
            input("Press Enter to return...")
            return

        try:
            scooter_id = int(input("Enter the ID of the scooter you want to delete: "))
        except ValueError:
            print("Invalid ID format.")
            input("Press Enter to return...")
            return

        if delete_scooter(scooter_id, db):
            print("\nScooter deleted.")
            write_log(username, "Deleted scooter", f"ID: {scooter_id}", suspicious=False)
        else:
            print("\nFailed to delete scooter.")
            write_log(username, f"Attempted to delete non-existent scooter", f"ID: {scooter_id}", suspicious=True)
        input("\nPress Enter to return...")
        return

    elif choice == "4":
        scooters = list_all_scooters(db)
        if not scooters:
            print("No scooters found.")
            write_log(username, "Tried listing all scooters", "", suspicious=True)
        else:
            write_log(username, "Listed all scooters", "", suspicious=False)
            print("\nList of all scooters:\n")
            for scooter in scooters:
                print(f"ID: {scooter.scooter_id}")
                print(f"  Brand: {scooter.brand}")
                print(f"  Model: {scooter.model}")
                print(f"  Serial Number: {scooter.serial_number}")
                print(f"  Top Speed: {scooter.top_speed} km/h")
                print(f"  Battery Capacity: {scooter.battery_capacity} Wh")
                print(f"  State of Charge: {scooter.state_of_charge}%")
                print(f"  Target SoC Range: {scooter.target_soc_range[0]}% - {scooter.target_soc_range[1]}%")
                print(f"  Location: ({scooter.location_lat}, {scooter.location_long})")
                print(f"  Out of Service: {'Yes' if scooter.out_of_service else 'No'}")
                print(f"  Mileage: {scooter.mileage} km")
                print(f"  Last Maintenance Date: {scooter.last_maintenance_date}")
                print("-" * 40)
        input("\nPress Enter to return...")
        return
    
    elif choice == "5":
        keyword = input("Enter search keyword (brand, model or serial number): ")
        resultaten = search_scooters(keyword, db)

        if not resultaten:
            print("\nNo scooters found for that keyword.")
            write_log(username, "Tried performing scooter search", f"Search keyword: {keyword}", suspicious=True)
        else:
            print("\n📋 Zoekresultaten:\n")
            write_log(username, "Performed scooter search", f"Search keyword: {keyword}", suspicious=False)
            for row in resultaten:
                print(f"ID: {row[0]}")
                print(f"  Brand: {row[1]}")
                print(f"  Model: {row[2]}")
                print(f"  Serial Number: {row[3]}")
                print(f"  State of Charge: {row[4]}%")
                print("-" * 40)

        input("\nPress Enter to return...")
        return

    else:
        print("Invalid choice.")
        input("Press Enter to return...")
        return

   
