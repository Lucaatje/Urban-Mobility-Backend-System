from utils.commands_ui import clear_console
from services.user_service import login


HIGHLIGHT = '\033[7m'  # Inverse (white-on-black or black-on-white)
COMMENT = '\033[90m' # Grey
BUTTON = '\033[32m' # Green
WARNING = '\033[31m' # Red
RESET = '\033[0m' # Return to normal (Always use this after coloring data)

def print_login_page(prompt, username, password, show_password):
    clear_console()
    password = '*' * len(password) if not show_password else password
    username_ph = f'{COMMENT}username{RESET}'
    password_ph = f'{COMMENT}password{RESET}'

    #print('\033[?25l', end='')
    print(f'{prompt}\n')
    print(f'Username: {username or username_ph} {COMMENT}- Press: U{RESET}')
    print(f'Password: {password or password_ph} {COMMENT}- Press: P - Toggle Password: T{RESET}')
    print(f'\n{BUTTON}[LOGIN]{RESET} {COMMENT}Press: 1{RESET}')
    print(f'{BUTTON}[CLOSE PROGRAM]{RESET} {COMMENT}Press: 2{RESET}')

def login_page_ui(prompt):
    username = ''
    password = ''
    show_password = False

    while True:
        print_login_page(prompt, username, password, show_password)

        choice = input("\nSelect an option: ").strip().lower()

        if choice == 'u': username = input("Enter username (min 8 chars, max 10 chars): ")
        elif choice == 'p': password = input("Enter password (min 12 chars, max 30 chars): ")
        elif choice == 't': show_password = not show_password
        elif choice == '1': 
            logged_in_user, message = login(username, password)
            if logged_in_user: return logged_in_user, message
            else: prompt = f"{WARNING}{message}{RESET}"
        elif choice == '2': return None, f"\n{WARNING}CLOSING PROGRAM...{RESET}"
        else: prompt = f"{WARNING}Invalid option. Please try again.{RESET}"
