from services.traveller_service import *
from utils.input_validation import *
import os
import datetime


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
            if traveller is None:
                print("Traveller creation cancelled.")
                continue
            RegisterTraveller(traveller)

        elif choice == '2':
            print("Available Travellers:")
            for t in GetAllTravellersId():
                print(f"Traveller ID: {t['id']}, Name: {t['name']}")
            # Loop until user provides a valid numeric ID or cancels with '0'
            while True:
                traveller_id = input("Enter traveller ID to view or 0 to cancel: ").strip()
                if traveller_id == '0':
                    print("View cancelled.")
                    break
                if traveller_id == '':
                    print("No input entered. Please enter a numeric ID or 0 to cancel.")
                    continue
                try:
                    tid = int(traveller_id)
                except ValueError:
                    print("Invalid ID format. Please enter a numeric ID or 0 to cancel.")
                    continue
                traveller = GetTravellerById(tid)
                if traveller:
                    print(f"Traveller ID: {traveller.id}")
                    print(f"Name: {traveller.first_name} {traveller.last_name}")
                    print(f"Birthday: {traveller.birthday}")
                    print(f"Gender: {traveller.gender}")
                    print(f"Address: {traveller.street_name} {traveller.house_number}, {traveller.zip_code}, {traveller.city}")
                    print(f"Email: {traveller.email_address}")
                    print(f"Mobile Phone: {traveller.mobile_phone}")
                    print(f"Driving License Number: {traveller.driving_license_number}")
                else:
                    print("Traveller not found.")
                break

        elif choice == '3':
            print("Available Travellers:")
            for t in GetAllTravellersId():
                print(f"Traveller ID: {t['id']}, Name: {t['name']}")
            # Loop until user provides a valid numeric ID to delete or cancels with '0'
            while True:
                traveller_id = input("Enter traveller ID to delete or 0 to cancel: ").strip()
                if traveller_id == '0':
                    print("Traveller deletion cancelled.")
                    break
                if traveller_id == '':
                    print("No input entered. Please enter a numeric ID or 0 to cancel.")
                    continue
                try:
                    tid = int(traveller_id)
                except ValueError:
                    print("Invalid ID format. Please enter a numeric ID or 0 to cancel.")
                    continue
                if DeleteTravellerById(tid):
                    print(f"Traveller with ID {traveller_id} has been deleted.")
                else:
                    print(f"Traveller with ID {traveller_id} not found.")
                break

        elif choice == '4':
            print("Available Travellers:")
            for t in GetAllTravellersId():
                print(f"Traveller ID: {t['id']}, Name: {t['name']}")
            # Loop until user provides a valid numeric ID to update or cancels with '0'
            while True:
                traveller_id = input("Enter traveller ID to update or 0 to cancel: ").strip()
                if traveller_id == '0':
                    print("Traveller update cancelled.")
                    break
                if traveller_id == '':
                    print("No input entered. Please enter a numeric ID or 0 to cancel.")
                    continue
                try:
                    tid = int(traveller_id)
                except ValueError:
                    print("Invalid ID format. Please enter a numeric ID or 0 to cancel.")
                    continue

                traveller = GetTravellerById(tid)

                if traveller is None:
                    print("Traveller not found.")
                    break

                print("Create a new traveller to replace existing one (press 'q' in prompts to cancel).")
                updated = Create_traveller(traveller)
                if updated is None:
                    print("Traveller creation/update cancelled.")
                else:
                    # preserve the original id if Create_traveller didn't set it
                    updated.id = getattr(updated, 'id', getattr(traveller, 'id', None))
                    UpdateTraveller(updated)
                break

        elif choice == '5':
            print("Exiting traveller management.")
            break
