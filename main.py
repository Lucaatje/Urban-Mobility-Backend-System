from database.db import init_db
from services.user_service import login, register
from utils.main_menu_ui import main_menu_ui
from utils.login_page_ui import login_page_ui
from models.models import User, UserRole
from utils.Manage_travaller_ui import manage_traveller_accounts


def main():
    init_db()  # Initialize the database
    # while True:
    #     print("\n--- Urban Mobility App ---")
    #     print("1. Registreer")
    #     print("2. Login")
    #     print("3. Afsluiten")

    #     keuze = input("Maak een keuze (1-3): ")

    #     if keuze == "1":
    #         username = input("Gebruikersnaam: ")
    #         email = input("Email: ")
    #         password = input("Wachtwoord: ")
    #         role = input("Rol (Super Administrator / System Administrator / Service Engineer): ")
    #         register(username, email, password, role)

    #     elif keuze == "2":
    #         username = input("Gebruikersnaam: ")
    #         password = input("Wachtwoord: ")
    #         login(username, password)

    #     elif keuze == "3":
    #         print("Programma afgesloten.")
    #         break
    #     else:
    #         print("Ongeldige keuze.")
    while (True):
        logged_in_user = login_page_ui(
            'welcome, login with username and password.')
        if not logged_in_user:
            break

        # MAIN_MENU NOT FINAL YET, DIFFERENT MENU FOR 3 DIFFERENT USER TYPES

        while (True):
            selected_option = main_menu_ui(logged_in_user)

            match selected_option:
                case '1':
                    manage_user_accounts(logged_in_user)  # TO-DO (Melvern)
                case '2':
                    if (logged_in_user.role == UserRole.SUPER_ADMIN or
                       logged_in_user.role == UserRole.SYSTEM_ADMIN):
                        manage_traveller_accounts(logged_in_user)
                    else:
                        print(
                            "You do not have permission to manage traveller accounts.")
                        continue

                case '3':
                    manage_scooter_information(logged_in_user)  # TO-DO (Luca)
                case '4':
                    break  # Logout and return to login page


if __name__ == "__main__":
    main()
