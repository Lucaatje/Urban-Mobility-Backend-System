from utils.commands_ui import clear_console
from utils.input_validation import validate_credentials


HIGHLIGHT = '\033[7m'  # Inverse (white-on-black or black-on-white)
COMMENT = '\033[90m' # Grey
BUTTON = '\033[32m' # Green
WARNING = '\033[31m' # Red
RESET = '\033[0m' # Return to normal (Always use this after coloring data)

def print_login_page(prompt, username, password, show_password):
    clear_console()
    password = '*' * len(password) if not show_password else password

    #print('\033[?25l', end='')
    print(f'{prompt} {COMMENT}input allowed: letters, numbers and space{RESET}\n')
    print(f'Username: {username} {COMMENT}Press: U{RESET}')
    print(f'Password: {password} {COMMENT}Press: P, Toggle Password: T{RESET}')
    print(f'\n{BUTTON}[LOGIN]{RESET} {COMMENT}Press: 1{RESET}')
    print(f'{BUTTON}[CLOSE PROGRAM]{RESET} {COMMENT}Press: 2{RESET}')

def login_page_ui(prompt):
    username = ''
    password = ''
    show_password = False

    while True:
        print_login_page(prompt, username, password, show_password)

        choice = input("\nSelect an option: ").strip().lower()

        if choice == 'u':
            username = input("Enter username (min 8 chars, max 10 chars): ")
            # if len(input_username) > 7 and len(input_username) < 11: username = input_username
            # else: prompt = f"{WARNING}Username: (min 8 chars, max 10 chars){RESET}"
            # if username_checker(input_username): username = input_username
        elif choice == 'p':
            password = input("Enter password (min 12 chars, max 30 chars): ")
            # if len(input_password) > 11 and len(input_password) < 31: password = input_password
            # else: prompt = f"{WARNING}Password: (min 12 chars, max 30 chars){RESET}"
            # if password_checker(input_password): password = input_password
        elif choice == 't':
            show_password = not show_password
        elif choice == '1':
            logged_in_user = validate_credentials(username, password)
            if logged_in_user:
                return logged_in_user
            else:
                prompt = f"{WARNING}Invalid credentials. Try again.{RESET}"
        elif choice == '2':
            return None
        else:
            prompt = f"{WARNING}Invalid option. Please try again.{RESET}"