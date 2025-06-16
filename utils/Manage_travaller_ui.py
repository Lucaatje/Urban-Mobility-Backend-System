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
            traveller_id = input("Enter traveller ID to view: ")
            traveller = GetTravellerById(int(traveller_id))
            if traveller:
                print(f"Traveller ID: {traveller.id}")
                print(f"Name: {traveller.first_name} {traveller.last_name}")
                print(f"Birthday: {traveller.birthday}")
                print(f"Gender: {traveller.gender}")
                print(
                    f"Address: {traveller.street_name} {traveller.house_number}, {traveller.zip_code}, {traveller.city}")
                print(f"Email: {traveller.email_address}")
                print(f"Mobile Phone: {traveller.mobile_phone}")
                print(
                    f"Driving License Number: {traveller.driving_license_number}")

        elif choice == '3':
            traveller_id = input("Enter traveller ID to delete: ")
            if DeleteTravellerById(int(traveller_id)):
                print(f"Traveller with ID {traveller_id} has been deleted.")
            else:
                print(f"Traveller with ID {traveller_id} not found.")

        elif choice == '4':
            traveller_id = input("Enter traveller ID to update: ")
            traveller = GetTravellerById(int(traveller_id))
            if (traveller is None):
                continue
            else:
                print("create a new traveller to replace existing one.")
                traveller = Create_traveller(traveller)
                if traveller is None:
                    print("Traveller creation/update cancelled.")
                else:
                    UpdateTraveller(traveller)
        elif choice == '5':
            print("Exiting traveller management.")
            break


def Create_traveller(existing_traveller=None):
    # Use existing values if provided, otherwise None
    first_name = getattr(existing_traveller, "first_name", None)
    last_name = getattr(existing_traveller, "last_name", None)
    birthday = getattr(existing_traveller, "birthday", None)
    Gender = getattr(existing_traveller, "gender", None)
    street_name = getattr(existing_traveller, "street_name", None)
    house_number = getattr(existing_traveller, "house_number", None)
    zip_code = getattr(existing_traveller, "zip_code", None)
    city = getattr(existing_traveller, "city", None)
    email_address = getattr(existing_traveller, "email_address", None)
    mobile_phone = getattr(existing_traveller, "mobile_phone", None)
    driving_license_number = getattr(
        existing_traveller, "driving_license_number", None)
    traveller_id = getattr(existing_traveller, "id", None)

    loop = True
    while loop:
        print(f"\nCurrent values:\n"
              f"First name: {first_name if first_name else 'Not set'}\n"
              f"Last name: {last_name if last_name else 'Not set'}\n"
              f"Birthday: {birthday if birthday else 'Not set'}\n"
              f"Gender: {Gender if Gender else 'Not set'}\n"
              f"Street name: {street_name if street_name else 'Not set'}\n"
              f"House number: {house_number if house_number else 'Not set'}\n"
              f"Zip code: {zip_code if zip_code else 'Not set'}\n"
              f"City: {city if city else 'Not set'}\n"
              f"Email address: {email_address if email_address else 'Not set'}\n"
              f"Mobile phone: {mobile_phone if mobile_phone else 'Not set'}\n"
              f"Driving license number: {driving_license_number if driving_license_number else 'Not set'}\n"
              )
        match = input(
            "Enter what you would like to fill in:\n"
            "1: First name,\n2: Last name,\n3: Birthday,\n"
            "4: Gender,\n5: Street name,\n6: House number,\n"
            "7: Zip code,\n8: City,\n9: Email address,\n10: Mobile phone,\n"
            "11: Driving license number,\n12: Continue\n13: Exit\n"
        ).strip()

        if match == '1':
            first_name = input("Enter first name: ")
        elif match == '2':
            last_name = input("Enter last name: ")
        elif match == '3':
            birthday = Date_verification()
        elif match == '4':
            Gender = input(
                "Enter your gender 'male' or 'female': ").strip().lower()
        elif match == '5':
            street_name = input("Enter street name: ")
        elif match == '6':
            house_number = input("Enter house number: ")
        elif match == '7':
            zip_code = Enter_zipcode()
        elif match == '8':
            city = Enter_city()
        elif match == '9':
            email_address = input("Enter email address: ")
        elif match == '10':
            mobile_phone = Enter_phonenumber()
        elif match == '11':
            driving_license_number = Enter_drivinglicense()
        elif match == '12':
            print("Continuing to create/update traveller...")
            loop = False
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear console
        elif match == '13':
            print("Exiting traveller creation/update.")
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear console
            return None
        else:
            print("Invalid option. Please try again.")

    # Check if all required fields are filled
    required_fields = [first_name, last_name, birthday,
                       Gender, email_address, driving_license_number]
    if not all(required_fields):
        print("Not all required fields are filled. Traveller not created/updated.")
        print("Returning to creation menu.")
        return Create_traveller(existing_traveller)

    traveller = Traveller(
        traveller_id=traveller_id,  # Use existing ID if updating
        first_name=first_name,
        last_name=last_name,
        birthday=birthday,
        gender=Gender,
        street_name=street_name,
        house_number=house_number,
        zip_code=zip_code,
        city=city,
        email_address=email_address,
        mobile_phone=mobile_phone,
        driving_license_number=driving_license_number
    )
    return traveller


def Enter_city():
    # choose city from 1 to 10
    city = input("Please select your city by number: 1: Amsterdam, 2: Rotterdam, 3: The Hague, 4: Utrecht, 5: Eindhoven 6: Breda, 7: Groningen, 8: Leeuwarden, 9: Papendrecht, 10: Dordrecht \n")
    # change input to city name
    city_dict = {
        '1': 'Amsterdam',
        '2': 'Rotterdam',
        '3': 'The Hague',
        '4': 'Utrecht',
        '5': 'Eindhoven',
        '6': 'Breda',
        '7': 'Groningen',
        '8': 'Leeuwarden',
        '9': 'Papendrecht',
        '10': 'Dordrecht'
    }
    city = city_dict.get(city, 'Unknown City')
    if city == 'Unknown City':
        print("Invalid city selection. Please try again.")
        Enter_city()
    return city


def Enter_phonenumber():
    PN = input("Please enter your phone number in the format +31612345678: ")
    if Mobile_phone_checker(PN)[0]:
        return PN
    else:
        print(Mobile_phone_checker(PN)[1])
        return Enter_phonenumber()


def Enter_drivinglicense():
    DL = input(
        "Please enter your driving license number: for example AB1234567 or A12345678: ")
    if Driving_license_number_checker(DL)[0]:
        return DL
    else:
        print(Driving_license_number_checker(DL)[1])
        return Enter_drivinglicense()


def Enter_zipcode():
    zip_code = input("Please enter your zip code in the format 1234AB: ")
    if ZIP_code_checker(zip_code)[0]:
        return zip_code
    else:
        print(ZIP_code_checker(zip_code)[1])
        return Enter_zipcode()


def Date_verification():
    date_str = input("Enter date in DD/MM/YYYY format: ")
    try:
        # Try to parse the date string
        date = datetime.datetime.strptime(date_str, '%d/%m/%Y')
        return date.strftime('%d/%m/%Y')  # Return in DD/MM/YYYY format
    except ValueError:
        print("Invalid date format. Please use DD/MM/YYYY.")
        return Date_verification()
