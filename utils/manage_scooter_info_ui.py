from database.db import get_db_connection
from utils.commands_ui import clear_console
from models.models import Scooter, UserRole
import os
from logs.logger import write_log
from services.scooter_service import get_editable_attributes_by_role
from services.scooter_service import get_scooter_by_id, search_scooters, create_scooter, get_all_scooters
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
        
        if choice == "4":
            print("Availabe Scooters:")
            for scooter in get_all_scooters():
                print(f"Scooter ID: {scooter['id']}, Name: {scooter['name']}")
            
            scooter_id_input = input("Enter Scooter ID to update or 0 to cancel: ").strip()
            
            if scooter_id_input == '0':
                print("Scooter update cancelled.")
                continue

            scooters = get_all_scooters()
            if not any(str(s.get("id")) == scooter_id_input for s in scooters):
                print("Scooter not found.")
                input("Press Enter to return...")
                continue

            try:
                scooter_id = int(scooter_id_input)
            except ValueError:
                print("Invalid ID format. Please enter a number.")
                write_log(logged_in_user.username, "Update scooter failed", f"Invalid ID: {scooter_id_input}", suspicious=True)
                continue
            
            scooter = get_scooter_by_id(scooter_id)
            if scooter is None:
                print("Scooter is not found.")
                write_log(logged_in_user.username, "Update scooter failed", f"ID not found: {scooter_id}", suspicious=True)
                continue
            
            print("Update the scooter's information. Press Enter to keep existing values.")
            updated_scooter = create_scooter(scooter)

            if updated_scooter is None:
                print("Scooter update is cancelled.")
                continue
            
            updated_scooter.id = scooter_id
            if update_scooter(scooter_id, updated_scooter):
                print("Scooter succesfully updated.")
                input("Press Enter to return...")
                write_log(logged_in_user.username, "Updated scooter", f"ID: {scooter_id}")
            else:
                print("Traveller update failed.")
                write_log(logged_in_user.username, "Update scooter failed", f"ID: {scooter_id}", suspicious=True)   

        elif choice == "5":
            keyword = input("Type in keyword (brand, model or serialnumber): ")
            results = search_scooters(keyword)

            if not results :
                print("\nNo scooters found with that keyword.")
                write_log(logged_in_user.username, "Tried performing scooter search", f"Search keyword: {keyword}", suspicious=True)
            else:
                print("\nSearch results: \n")
                write_log(logged_in_user.username, "Performed scooter search", f"Search keyword: {keyword}", suspicious=False)
                for row in results:
                    print(f"ID: {row[0]}")
                    print(f"  Brand: {row[1]}")
                    print(f"  Model: {row[2]}")
                    print(f"  Serial Number: {row[3]}")
                    print(f"  State of Charge: {row[4]}%")
                    print("-" * 40)

            input("\nPress Enter to return...")
            return         

        elif choice == "6":
            print("Exiting scooter management.")
            break
