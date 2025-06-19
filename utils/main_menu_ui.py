from utils.commands_ui import clear_console
from models.models import UserRole


HIGHLIGHT = '\033[7m'  # Inverse (white-on-black or black-on-white)
COMMENT = '\033[90m' # Grey
SUCCES = '\033[32m' # Green
BUTTON = '\033[34m'  # Blue
WARNING = '\033[31m' # Red
RESET = '\033[0m' # Return to normal (Always use this after coloring data)


def print_main_menu(logged_in_user, prompt):
    clear_console()
    # OPTIONS FOR EACH USER WILL BE CHANGED LATER

    # IF SUPER ADMIN
    if logged_in_user.role == UserRole.SUPER_ADMIN:
        print(f'Main Menu (SUPER_ADMIN: {logged_in_user.username}) {COMMENT}input allowed: numbers{RESET}\n')
        print(f'{SUCCES}{prompt}{RESET}\n')
        print(f'Manage user accounts: {COMMENT}- Press: 1{RESET}')
        print(f'Manage traveller accounts: {COMMENT}- Press: 2{RESET}')
        print(f'Manage scooter information: {COMMENT}- Press: 3{RESET}')
        print(f'{BUTTON}[LOG OUT]{RESET} {COMMENT}Press: 4{RESET}')
        print(f'{BUTTON}[MANAGE DATABASE]{RESET} {COMMENT}Press: 5{RESET}')
    
    # IF SYSTEM ADMIN
    if logged_in_user.role == UserRole.SYSTEM_ADMIN:
        print(f'Main Menu (SYSTEM_ADMIN: {logged_in_user.username}) {COMMENT}input allowed: numbers{RESET}\n')
        print(f'{SUCCES}{prompt}{RESET}\n')
        print(f'Manage user accounts: {COMMENT}- Press: 1{RESET}')
        print(f'Manage traveller accounts: {COMMENT}- Press: 2{RESET}')
        print(f'Manage scooter information: {COMMENT}- Press: 3{RESET}')
        print(f'{BUTTON}[LOG OUT]{RESET} {COMMENT}Press: 4{RESET}')
        print(f'MANAGE DATABASE {COMMENT}Press: 5{RESET}')
    
    #IF SERVICE ENGINEER
    if logged_in_user.role == UserRole.SERVICE_ENGINEER:
        print(f'Main Menu (SERVICE_ENGINEER: {logged_in_user.username}) {COMMENT}input allowed: numbers{RESET}\n')
        print(f'{SUCCES}{prompt}{RESET}\n')
        print(f'Manage user accounts: {COMMENT}- Press: 1{RESET}')
        print(f'Manage traveller accounts: {COMMENT}- Press: 2{RESET}')
        print(f'Manage scooter information: {COMMENT}- Press: 3{RESET}')
        print(f'{BUTTON}[LOG OUT]{RESET} {COMMENT}Press: 4{RESET}')

def main_menu_ui(logged_in_user, prompt):
    while(True):
        print_main_menu(logged_in_user, prompt)

        index = input("\nSelect an option: ").strip().lower()

        if index in ['1', '2', '3', '4', '5']:
            return index
        else:
            prompt = f"{WARNING}Invalid option. Please try again.{RESET}"
