from services.traveller_service import *


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
                print(f"Address: {traveller.street_name} {traveller.house_number}, {traveller.zip_code}, {traveller.city}")
                print(f"Email: {traveller.email_address}")
                print(f"Mobile Phone: {traveller.mobile_phone}")
                print(f"Driving License Number: {traveller.driving_license_number}")

        elif choice == '3':
            traveller_id = input("Enter traveller ID to delete: ")
            if DeleteTravellerById(int(traveller_id)):
                print(f"Traveller with ID {traveller_id} has been deleted.")
            else:
                print(f"Traveller with ID {traveller_id} not found.")

        elif choice == '4':
            traveller_id = input("Enter traveller ID to update: ")
            traveller = GetTravellerById(int(traveller_id))
            print("create a new traveller to replace existing one.")
            Create_traveller()
            UpdateTraveller(traveller)

            
def Create_traveller():
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    birthday = input("Enter birthday (DD/MM/YYYY): ")
    Gender = input("Enter your gender 'male' or 'female': ").strip().lower()
    street_name = input("Enter street name: ")
    house_number = input("Enter house number: ")
    zip_code = input("Enter zip code: ")
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
        Create_traveller()
    email_address = input("Enter email address: ")
    mobile_phone = input("Enter mobile phone number: ")
    driving_license_number = input("Enter driving license number: ")
    traveller = Traveller(
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