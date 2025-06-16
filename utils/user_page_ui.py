from services.user_service import retrieve_users, register, update, delete
from utils.commands_ui import clear_console
from models.models import UserRole


HIGHLIGHT = '\033[7m'  # Inverse (white-on-black or black-on-white)
COMMENT = '\033[90m' # Grey
SUCCES = '\033[32m' # Green
BUTTON = '\033[34m'  # Blue
WARNING = '\033[31m' # Red
RESET = '\033[0m' # Return to normal (Always use this after coloring data)

    ######################################################################################################
    # SHOWCASES LIST OF ALL USERS:                                                                       #
    ######################################################################################################

    # User list layout print:

def print_visible_users(logged_in_user, user_list, response, page_number, user_count):
    clear_console()

    print('╔' + '═' * 120 + '╗')
    print(f'║ {logged_in_user.role.value} - id: {logged_in_user.user_id} - username: {logged_in_user.username}'.ljust(61) + f'total users: {user_count} ║'.rjust(61))
    print('╠' + '═' * 120 + '╣')

    for user in user_list:
        if user.user_id != logged_in_user.user_id:
            id = str(user.user_id).ljust(42)
            username = user.username.ljust(16)
            # password = user.password_hash.ljust(30)
            email = user.email.ljust(39) if len(user.email) < 39 else user.email[:36] + '...'
            role = user.role.value.ljust(20)

            identification = f'id: {id} │ username: {username} │'.ljust(118)
            additionals = f'email: {email} │ role: {role} │'.ljust(118)
            separator = '-' * 118

            print(f'║ {identification} ║\n║ {additionals} ║\n║ {separator} ║')
    
    if '\033[31m' in response or '\033[32m' in response:
        print('║' + f' {response}'.ljust(60) + f'page: {page_number} '.rjust(69) + '║')
    else:
        print('║' + f' {response}'.ljust(60) + f'page: {page_number} '.rjust(60) + '║')
    print('╚' + '═' * 120 + '╝')
    print(f'{COMMENT}Enter id: Select user - Press R: Register user - Press (+ or -): Navigate pages{RESET}')
    print(f'{BUTTON}[RETURN TO MAIN MENU]{RESET} {COMMENT}Press: B{RESET}')

    # User list layout options:

def manage_user_accounts(logged_in_user):
    response = ''
    page_number = 1
    current_user_list, user_count = retrieve_users(page_number)

    while True:
        print_visible_users(logged_in_user, current_user_list, response, page_number, user_count)

        choice = input('\nSelect an option: ').strip().lower()

        if is_valid_id(choice, logged_in_user, current_user_list):
            choice_int = int(choice)
            selected_user = logged_in_user if choice_int == logged_in_user.user_id else next(user for user in current_user_list if user.user_id == choice_int)
            response = user_details_page_ui(selected_user, logged_in_user)
            current_user_list, user_count = retrieve_users(page_number)
        elif choice == '+':
            if len(current_user_list) > 9:
                response = ''
                page_number += 1
                current_user_list, user_count = retrieve_users(page_number)
        elif choice == '-':
            if page_number > 1:
                response = ''
                page_number -= 1
                current_user_list, user_count = retrieve_users(page_number)
        elif choice == 'r':
            message = register_user(logged_in_user) # System Admin (can add: Service Engineer ), Super Admin (can add: System Engineer + Service Engineer)
            response = message
            current_user_list, user_count = retrieve_users(page_number)
        elif choice == 'b':
            return
        else: response = f"{WARNING}Invalid option. Please try again.{RESET}"

    # Validate user input on existing id on current visible users:

def is_valid_id(choice, logged_in_user, user_list):
    try:
        choice_int = int(choice)
    except ValueError:
        return False
    return choice_int == logged_in_user.user_id or any(user.user_id == choice_int for user in user_list)

    ######################################################################################################
    # REGISTRING SERVICE_ENGINEERS AND SYSTEM_ADMINISTRATORS:                                            #
    ######################################################################################################

    # Print registration form:

def print_registration_form(username, email, password, role, show_password, prompt, logged_in_user):
    clear_console()
    password = '*' * len(password) if not show_password else password

    # Placeholders:
    username_ph = f'{COMMENT}username{RESET}'
    email_ph = f'{COMMENT}email{RESET}'
    password_ph = f'{COMMENT}password{RESET}'

    # print('\033[?25l', end='')
    print(f'{prompt}\n')
    print(f'Username: {username or username_ph} {COMMENT}- Press: U{RESET}')
    print(f'Email: {email or email_ph} {COMMENT}- Press E{RESET}')
    print(f'Password: {password or password_ph} {COMMENT}- Press: P - Toggle Password: T{RESET}')
    print(f'User Role: {role.value} {COMMENT}Switch Role: R{RESET}' if logged_in_user.role == UserRole.SUPER_ADMIN else f'User Role: {role.value}')
    print(f'\n{BUTTON}[REGISTER USER]{RESET} {COMMENT}Press: 1{RESET}')
    print(f'{BUTTON}[RETURN TO USER MANAGER]{RESET} {COMMENT}Press: 2{RESET}')

    # Fill in new user credentials:

def register_user(logged_in_user):
    # System Admin (can add: Service Engineer ), Super Admin (can add: System Engineer + Service Engineer)
    username = ''
    email = ''
    password = ''
    role = UserRole.SERVICE_ENGINEER
    show_password = False
    prompt = "Register a new Service Engineer."
    if logged_in_user.role == UserRole.SUPER_ADMIN: prompt = "Register a new Service Engineer or System Administrator."

    while True:
        print_registration_form(username, email, password, role, show_password, prompt, logged_in_user)

        choice = input('\nSelect an option: ').strip().lower()

        if choice == 'u': username = input("Enter username (min 8 chars, max 10 chars): ")
        elif choice == 'e': email = input("Enter email (example: username@domain.nl): ")
        elif choice == 'p': password = input("Enter password (min 12 chars, max 30 chars): ")
        elif choice == 'r' and logged_in_user.role == UserRole.SUPER_ADMIN:
            role = UserRole.SYSTEM_ADMIN if role == UserRole.SERVICE_ENGINEER else UserRole.SERVICE_ENGINEER
        elif choice == 't': show_password = not show_password
        elif choice == '1': 
            valid, message = register(username, email, password, role)
            if valid: return f"{SUCCES}{message}{RESET}"
            else: prompt = f"{WARNING}{message}{RESET}"
        elif choice == '2': return ''
        else: prompt = f"{WARNING}Invalid option. Please try again.{RESET}"

    ######################################################################################################
    # REGISTRING SERVICE_ENGINEERS AND SYSTEM_ADMINISTRATORS:                                            #
    ######################################################################################################

    # Print user details for updating:

def print_user_details(username, email, password, role, show_password, can_change_password, prompt, selected_user):
    clear_console()
    password = '*' * len(password) if not show_password else password

    # Placeholders:
    username_ph = f'{COMMENT}{selected_user.username}{RESET}'
    email_ph = f'{COMMENT}{selected_user.email}{RESET}'
    password_ph = f'{COMMENT}password{RESET}'
    role_comment = f'{COMMENT}Switch Role: R{RESET}' if selected_user.role != UserRole.SYSTEM_ADMIN else ''

    # print('\033[?25l', end='')
    print(f'{prompt}\n')
    print(f'Username: {username or username_ph} {COMMENT}- Press: U{RESET}')
    print(f'Email: {email or email_ph} {COMMENT}- Press E{RESET}')
    if can_change_password: print(f'Password: {password or password_ph} {COMMENT}- Press: P - Toggle Password: T{RESET}')
    print(f'User Role: {role.value} {role_comment}')
    print(f'\n{BUTTON}[UPDATE USER]{RESET} {COMMENT}Press: 1{RESET}')
    print(f'{WARNING}[DELETE USER]{RESET} {COMMENT}Press: 2{RESET}')
    print(f'{BUTTON}[RETURN TO USER MANAGER]{RESET} {COMMENT}Press: 3{RESET}')

    # Fill in new user details for updating:

def user_details_page_ui(selected_user, logged_in_user):
    can_change_password = True

    if selected_user.role == UserRole.SUPER_ADMIN: return f'{WARNING}cannot update super_admin{RESET}'
    if selected_user.user_id == logged_in_user.user_id: can_change_password = False
    elif selected_user.role == logged_in_user.role: return f'{WARNING}cannot update another System Administrator{RESET}'

    username = ''
    email = ''
    password = ''
    role = selected_user.role
    show_password = False
    prompt = f"Update user account for {selected_user.role.value}."

    while True:
        print_user_details(username, email, password, role, show_password, can_change_password, prompt, selected_user)

        choice = input('\nSelect an option: ').strip().lower()

        if choice == 'u': username = input("Change username (min 8 chars, max 10 chars): ")
        elif choice == 'e': email = input("Change email (example: username@domain.nl): ")
        elif choice == 'p' and can_change_password:
            # CHANGE THIS SO THAT IT GENERATES A PASSWORD AUTOMATICALY!
            password = input("Enter temporary new password (min 12 chars, max 30 chars): ")
        elif choice == 'r' and selected_user.role == UserRole.SERVICE_ENGINEER:
            role = UserRole.SYSTEM_ADMIN if role == UserRole.SERVICE_ENGINEER else UserRole.SERVICE_ENGINEER
            # ASK TEACHER IF THIS NEEDS TO BE IN THE ASSIGNMENT!
        elif choice == 't': show_password = not show_password
        elif choice == '1':
            valid, message = update(selected_user.user_id, username, email, password, role, selected_user)
            if valid: prompt = f"{SUCCES}{message}{RESET}"
            else: prompt = f"{WARNING}{message}{RESET}"
        elif choice == '2':
            valid, message = delete(selected_user)
            if valid: return message
            else: prompt = message
        elif choice == '3': return ''
        else: prompt = f"{WARNING}Invalid option. Please try again.{RESET}"
