from services.traveller_service import *
from utils.input_validation import *
import os
import datetime
from logs.logger import write_log


def Print_Traveller_menu():
    print("1. Add Traveller")
    print("2. View Traveller")
    print("3. Delete Traveller")
    print("4. Update Traveller")
    print("5. Exit")


def manage_traveller_accounts(logged_in_user):
    while True:
        Print_Traveller_menu()
        choice = input("Select an option: ").strip()

        if choice == '1':
            traveller = Create_traveller()
            RegisterTraveller(traveller)
            write_log(logged_in_user.username, "Added traveller", f"{traveller.first_name} {traveller.last_name}")

        elif choice == '2':
            print("Available Travellers:")
            # Display all traveller ID and names
            for id in GetAllTravellersId():
                print(f"Traveller ID: {id}")
            traveller_id = input(
                "Enter traveller ID to view enter 0 to cancel: ")
            if traveller_id != '0':
                traveller = GetTravellerById(int(traveller_id))
                # print format
                if traveller:
                    print(f"Traveller ID: {traveller.id}")
                    print(
                        f"Name: {traveller.first_name} {traveller.last_name}")
                    print(f"Birthday: {traveller.birthday}")
                    print(f"Gender: {traveller.gender}")
                    print(
                        f"Address: {traveller.street_name} {traveller.house_number}, {traveller.zip_code}, {traveller.city}")
                    print(f"Email: {traveller.email_address}")
                    print(f"Mobile Phone: {traveller.mobile_phone}")
                    print(
                        f"Driving License Number: {traveller.driving_license_number}")
                    write_log(logged_in_user.username, "Viewed traveller", f"ID: {traveller.id}")
            else:
                print("Traveller not found.")
                write_log(logged_in_user.username, "View traveller failed", f"ID: {traveller_id}", suspicious=True)


        elif choice == '3':
            print("Available Travellers:")
            for id in GetAllTravellersId():
                print(f"Traveller ID: {id}")
            traveller_id = input(
                "Enter traveller ID to delete enter 0 to cancel: ")
            if traveller_id != '0':
                if DeleteTravellerById(int(traveller_id)):
                    print(
                        f"Traveller with ID {traveller_id} has been deleted.")
                    write_log(logged_in_user.username, "Deleted traveller", f"ID: {traveller_id}")
                else:
                    print(f"Traveller with ID {traveller_id} not found.")
                    write_log(logged_in_user.username, "Delete traveller failed", f"ID: {traveller_id}", suspicious=True)
            else:
                print("Traveller deletion cancelled.")

        elif choice == '4':
            print("Available Travellers:")
            for traveller in GetAllTravellersId():
                print(f"Traveller ID: {traveller['id']}, Name: {traveller['name']}")

            traveller_id_input = input("Enter traveller ID to update or 0 to cancel: ").strip()
            
            if traveller_id_input == '0':
                print("Traveller update cancelled.")
                continue

            try:
                traveller_id = int(traveller_id_input)
            except ValueError:
                print("Invalid ID format. Please enter a number.")
                write_log(logged_in_user.username, "Update traveller failed", f"Invalid ID: {traveller_id_input}", suspicious=True)
                continue

            traveller = GetTravellerById(traveller_id)
            if traveller is None:
                print("Traveller not found.")
                write_log(logged_in_user.username, "Update traveller failed", f"ID not found: {traveller_id}", suspicious=True)
                continue

            print("Update the traveller's information. Press Enter to keep existing values.")
            updated_traveller = Create_traveller(traveller)

            if updated_traveller is None:
                print("Traveller update cancelled.")
                continue

            updated_traveller.id = traveller_id  # Ensure ID is preserved
            if UpdateTraveller(updated_traveller):
                print("Traveller successfully updated.")
                write_log(logged_in_user.username, "Updated traveller", f"ID: {traveller_id}")
            else:
                print("Traveller update failed.")
                write_log(logged_in_user.username, "Update traveller failed", f"ID: {traveller_id}", suspicious=True)

        elif choice == '5':
            print("Exiting traveller management.")
            break
