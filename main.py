from database.db import init_db
from services.user_service import login, register


def main():
    while True:
        print("\n--- Urban Mobility App ---")
        print("1. Registreer")
        print("2. Login")
        print("3. Afsluiten")

        keuze = input("Maak een keuze (1-3): ")

        if keuze == "1":
            username = input("Gebruikersnaam: ")
            email = input("Email: ")
            password = input("Wachtwoord: ")
            role = input("Rol (Super Administrator / System Administrator / Service Engineer): ")
            register(username, email, password, role)

        elif keuze == "2":
            username = input("Gebruikersnaam: ")
            password = input("Wachtwoord: ")
            login(username, password)

        elif keuze == "3":
            print("Programma afgesloten.")
            break
        else:
            print("Ongeldige keuze.")

if __name__ == "__main__":
    main()