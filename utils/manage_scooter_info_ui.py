from database.db import get_db_connection
from utils.commands_ui import clear_console
from models.models import Scooter, UserRole
import os
from logs.logger import write_log
from services.scooter_service import get_editable_attributes_by_role
from services.scooter_service import get_scooter_by_id, search_scooters, create_scooter
from services.scooter_service import (
    add_scooter,
    update_scooter,
    delete_scooter,
    list_all_scooters
)
from utils.data_encryption import decrypt

def Print_Scooter_Menu():
    clear_console()
    print("Scooter Management\n")
    print("1. Add Scooter")
    print("2. View all scooters")
    print("3. Delete Scooter")
    print("4. Update Scooter")
    print("5. Search scooters by keyword")
    print("6. Exit")


def Print_Scooter_In_List(scooter):
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


def manage_scooter_information(logged_in_user):

    while True:

        Print_Scooter_Menu()
        choice = input("Select an option: ").strip()

        if choice == "1":
            if logged_in_user.role == UserRole.SERVICE_ENGINEER:
                print("\nYou don't have permission to add a scooter.")
                write_log(logged_in_user.username, f"Attempted to add scooter with no permission", suspicious=True)
                input("Press Enter to return to the menu...")
                os.system('cls' if os.name == 'nt' else 'clear')
                continue
            
            scooter = create_scooter()

            if scooter is None:
                continue

            result = add_scooter(scooter)
            success, message = result

            if success:
                print(message)
                write_log(logged_in_user.username, "Added new scooter", f"Serial: {scooter.serial_number}", suspicious=False)
            else:
                print(message)
                write_log(logged_in_user.username, "Failed to add scooter", suspicious=True)
            input("Press enter to return to scooter menu.")
            os.system('cls' if os.name == 'nt' else 'clear')

        if choice == "2":
            scooters = list_all_scooters()
            if len(scooters) > 0:
                write_log(logged_in_user.username, "Listed all scooters", "", suspicious=False)
                print("\nList of all scooters:\n")
                for scooter in scooters:
                    Print_Scooter_In_List(scooter)
            else:
                print("No scooters found.")
                write_log(logged_in_user.username, "Tried listing all scooters", "", suspicious=True)
            input("\nPress Enter to return...")
            return

        if choice == "3":
            if logged_in_user.role == UserRole.SERVICE_ENGINEER:
                print("You don't have permission to delete a scooter.")
                write_log(logged_in_user.username, f"Attempted to delete scooter with no permission", suspicious=True)
                input("Press Enter to return to the menu...")
                os.system('cls' if os.name == 'nt' else 'clear')
                continue
            
            try:
                scooter_id = int(input("Enter the ID of the scooter you want to delete: "))
            except ValueError:
                print("Invalid ID format.")
                input("Press Enter to return...")
                return

            if delete_scooter(scooter_id):
                print("\nScooter deleted.")
                write_log(logged_in_user.username, "Deleted scooter", f"ID: {scooter_id}", suspicious=False)
            else:
                print("\nFailed to delete scooter.")
                write_log(logged_in_user.username, f"Attempted to delete non-existent scooter", f"ID: {scooter_id}", suspicious=True)
            input("\nPress Enter to return...")
            return

        elif choice == "6":
            print("Exiting scooter management.")
            break

    # elif choice == "2":
    #     try:
    #         scooter_id = int(input("Enter the ID of the scooter you want to update: "))
    #     except ValueError:
    #         print("❌ Invalid ID format.")
    #         input("Press Enter to return...")
    #         return

    #     existing_scooter = get_scooter_by_id(scooter_id, db)
    #     if not existing_scooter:
    #         write_log(logged_in_user.username, "Attempted to update non-existent scooter", f"ID: {scooter_id}", suspicious=True)
    #         print(f"❌ Scooter ID {scooter_id} bestaat niet.")
    #         input("Press Enter to return...")
    #         return

    #     editable_fields = get_editable_attributes_by_role(logged_in_user.role)

    #     print("\n📋 Kies welk attribuut je wilt bewerken:")
    #     for i, attr in enumerate(editable_fields, 1):
    #         print(f"{i}. {attr.replace('_', ' ').title()}")

    #     try:
    #         field_choice = int(input("\nNummer van veld: "))
    #         if field_choice < 1 or field_choice > len(editable_fields):
    #             raise ValueError
    #     except ValueError:
    #         print("❌ Ongeldige keuze.")
    #         input("Press Enter to return...")
    #         return

    #     selected_field = editable_fields[field_choice - 1]
    #     updates = {}

    #     if selected_field == "target_soc":
    #         try:
    #             min_val = float(input("Nieuwe minimum SoC (%): "))
    #             max_val = float(input("Nieuwe maximum SoC (%): "))
    #             updates[selected_field] = (min_val, max_val)
    #         except ValueError:
    #             print("❌ Ongeldige invoer voor SoC-range.")
    #             input("Press Enter to return...")
    #             return
    #     elif selected_field == "location":
    #         lat = input("Latitude: ")
    #         lon = input("Longitude: ")
    #         updates[selected_field] = (lat, lon)
    #     elif selected_field == "out_of_service":
    #         updates[selected_field] = input("Out of service? (yes/no): ").lower() in ['yes', 'ja', 'true']
    #     elif selected_field in ["state_of_charge", "range_km", "mileage"]:
    #         try:
    #             updates[selected_field] = float(input(f"Nieuwe waarde voor '{selected_field}': "))
    #         except ValueError:
    #             print("❌ Ongeldige numerieke invoer.")
    #             input("Press Enter to return...")
    #             return
    #     else:
    #         updates[selected_field] = input(f"Nieuwe waarde voor '{selected_field}': ")
        
        
    #     if selected_field == "target_soc":
    #         existing_scooter.target_soc_range = updates[selected_field]
    #     elif selected_field == "location":
    #         existing_scooter.location_lat = float(updates[selected_field][0])
    #         existing_scooter.location_long = float(updates[selected_field][1])
    #     else:
    #         setattr(existing_scooter, selected_field, updates[selected_field])


    #     # En valideer + sla op
    #     success = update_scooter(scooter_id, existing_scooter, db, username=logged_in_user.username, updated_field=selected_field)

    #     if success:
    #         print("\n✅ Scooter succesvol bijgewerkt.")
    #         write_log(logged_in_user.username, f"Updated scooter field '{selected_field}'", f"Scooter ID: {scooter_id}", suspicious=False)
    #     else:
    #         print("\n❌ Fout bij updaten van scooter.")
    #         write_log(logged_in_user.username, f"Tried updating scooter field '{selected_field}'", f"Scooter ID: {scooter_id}", suspicious=True)

    #     input("\nPress Enter to return...")
    #     return
    
    # elif choice == "4":
    #     scooters = list_all_scooters(db)
    #     if not scooters:
    #         print("⚠️  No scooters found.")
    #         write_log(logged_in_user.username, "Tried listing all scooters", "", suspicious=True)
    #     else:
    #         write_log(logged_in_user.username, "Listed all scooters", "", suspicious=False)
    #         print("\n📋 List of all scooters:\n")
    #         for scooter in scooters:
    #             print(f"ID: {scooter.scooter_id}")
    #             print(f"  Brand: {scooter.brand}")
    #             print(f"  Model: {scooter.model}")
    #             print(f"  Serial Number: {scooter.serial_number}")
    #             print(f"  Top Speed: {scooter.top_speed} km/h")
    #             print(f"  Battery Capacity: {scooter.battery_capacity} Wh")
    #             print(f"  State of Charge: {scooter.state_of_charge}%")
    #             print(f"  Target SoC Range: {scooter.target_soc_range[0]}% - {scooter.target_soc_range[1]}%")
    #             print(f"  Location: ({scooter.location_lat}, {scooter.location_long})")
    #             print(f"  Out of Service: {'Yes' if scooter.out_of_service else 'No'}")
    #             print(f"  Mileage: {scooter.mileage} km")
    #             print(f"  Last Maintenance Date: {scooter.last_maintenance_date}")
    #             print("-" * 40)
    #     input("\nPress Enter to return...")
    #     return
    
    # elif choice == "5":
    #     keyword = input("🔍 Voer zoekterm in (merk, model of serienummer): ")
    #     resultaten = search_scooters(keyword, db)

    #     if not resultaten:
    #         print("\n⚠️  Geen scooters gevonden met die zoekterm.")
    #         write_log(logged_in_user.username, "Tried performing scooter search", f"Search keyword: {keyword}", suspicious=True)
    #     else:
    #         print("\n📋 Zoekresultaten:\n")
    #         write_log(logged_in_user.username, "Performed scooter search", f"Search keyword: {keyword}", suspicious=False)
    #         for row in resultaten:
    #             print(f"ID: {row[0]}")
    #             print(f"  Brand: {row[1]}")
    #             print(f"  Model: {row[2]}")
    #             print(f"  Serial Number: {row[3]}")
    #             print(f"  State of Charge: {row[4]}%")
    #             print("-" * 40)

    #     input("\nDruk op Enter om terug te keren...")
    #     return

    # else:
    #     print("❌ Invalid choice.")
    #     input("Press Enter to return...")
    #     return

   
