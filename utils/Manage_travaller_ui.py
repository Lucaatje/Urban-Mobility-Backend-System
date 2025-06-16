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
            RegisterTraveller(traveller)

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
            else:
                print("Traveller not found.")

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
                else:
                    print(f"Traveller with ID {traveller_id} not found.")
            else:
                print("Traveller deletion cancelled.")

        elif choice == '4':
            print("Available Travellers:")
            for id in GetAllTravellersId():
                print(f"Traveller ID: {id}")
            traveller_id = input(
                "Enter traveller ID to update enter 0 to cancel: ")
            if traveller_id == '0':
                traveller = GetTravellerById(int(traveller_id))
                if (traveller is None):
                    continue
                else:
                    print("create a new traveller to replace existing one.")
                    # use the create traveller function to create a new traveller
                    traveller = Create_traveller(traveller)
                    # if the traveller is None, it means the user cancelled the creation
                    if traveller is None:
                        print("Traveller creation/update cancelled.")
                    else:
                        UpdateTraveller(traveller)
            else:
                print("Traveller deletion cancelled.")

        elif choice == '5':
            print("Exiting traveller management.")
            break
