from database.db import init_db
from utils.user_page_ui import manage_user_accounts
from utils.main_menu_ui import main_menu_ui
from utils.login_page_ui import login_page_ui
from models.models import User, UserRole
from utils.manage_scooter_info_ui import manage_scooter_information
from utils.Manage_travaller_ui import manage_traveller_accounts
from database.Backup import *
from utils.manage_profile import manage_profile
from logs.logger import read_logs
HIGHLIGHT = '\033[7m'  # Inverse (white-on-black or black-on-white)
COMMENT = '\033[90m' # Grey
SUCCES = '\033[32m' # Green
BUTTON = '\033[34m'  # Blue
WARNING = '\033[31m' # Red
RESET = '\033[0m' # Return to normal (Always use this after coloring data)


def main():
    init_db()  # Initialize the database, you can keep this on for now since it also checks if it already exists.
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
        logged_in_user, message = login_page_ui(
            'welcome, login with username and password.')
        if not logged_in_user:
            print(message)
            break

        # MAIN_MENU NOT FINAL YET, DIFFERENT MENU FOR 3 DIFFERENT USER TYPES

        while (True):
            selected_option = main_menu_ui(logged_in_user, message)

            if logged_in_user.role == UserRole.SERVICE_ENGINEER:
                # FOR SERVICE ENGINEER
                match selected_option:
                    case '1':
                        manage_profile(logged_in_user)  # TO-DO (Melvern)
                    case '2':
                        manage_scooter_information(logged_in_user)  # TO-DO (Luca)
                    case '3':
                        break # Logout and return to login page
                    case _:
                        message = f"{WARNING}Invalid option. Please try again.{RESET}"
            else:
                # FOR SUPER/SYSTEM ADMINS
                match selected_option:
                    case '1':
                        response = manage_user_accounts(logged_in_user)  # TO-DO (Melvern)
                        if response == "REDIRECT_LOGIN": break
                    case '2':
                        manage_traveller_accounts(logged_in_user)
                    case '3':
                        manage_scooter_information(logged_in_user)  # TO-DO (Luca)
                    case '4':
                        UI_backup_database(logged_in_user)
                    case '5':
                        response = read_logs(logged_in_user)
                    case '6':
                        break # Logout and return to login page
                    case _:
                        message = f"{WARNING}Invalid option. Please try again.{RESET}"

if __name__ == "__main__":
    main()
