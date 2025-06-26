from utils.commands_ui import clear_console
from models.models import UserRole
from services.user_service import update_password

HIGHLIGHT = '\033[7m'  # Inverse (white-on-black or black-on-white)
COMMENT = '\033[90m' # Grey
SUCCES = '\033[32m' # Green
BUTTON = '\033[34m'  # Blue
WARNING = '\033[31m' # Red
RESET = '\033[0m' # Return to normal (Always use this after coloring data)

def print_profile(password, show_password, prompt, logged_in_user):
    clear_console()
    password = '*' * len(password) if not show_password else password

    # Placeholders:
    password_ph = f'{COMMENT}password{RESET}'

    # print('\033[?25l', end='')
    print(f'{prompt}\n')
    print(f'Username: {logged_in_user.username}')
    print(f'Email: {logged_in_user.email}')
    print(f'Password: {password or password_ph} {COMMENT}- Press: P - Toggle Password: T{RESET}')
    print(f'User Role: {logged_in_user.role.value}')
    print(f'\n{BUTTON}[CONFIRM NEW PASSWORD]{RESET} {COMMENT}Press: 1{RESET}')
    print(f'{BUTTON}[RETURN TO MAIN MENU]{RESET} {COMMENT}Press: 2{RESET}')

def manage_profile(logged_in_user):
    password = ''
    show_password = False
    prompt = f"{COMMENT}Can only change password.{RESET}"

    while True:
        print_profile(password, show_password, prompt, logged_in_user)

        choice = input('\nSelect an option: ').strip().lower()

        if choice == 'p': password = input("Enter password (min 12 chars, max 30 chars): ")
        elif choice == 't': show_password = not show_password
        elif choice == '1':
            valid, message = update_password(logged_in_user.username, password)
            if valid: prompt = f"{SUCCES}{message}{RESET}"
            else: prompt = f"{WARNING}{message}{RESET}"
        elif choice == '2': return