from enum import Enum


class Traveller:
    def __init__(self, traveller_id, first_name, last_name, birthday, gender, street_name, house_number,
                 zip_code, city, email_address, mobile_phone, driving_license_number, registration_date=None):
        self.id = traveller_id  # uniek ID
        self.first_name = first_name.strip().title()
        self.last_name = last_name.strip().title()
        # verwacht als YYYY-MM-DD (string of datetime.date)
        self.birthday = birthday
        self.gender = gender.lower()  # 'male' of 'female'

        self.street_name = street_name.strip().title()
        self.house_number = house_number
        self.zip_code = zip_code.upper()  # Formaat: DDDDXX
        self.city = city.strip().title()

        self.email_address = email_address.lower()
        self.mobile_phone = mobile_phone  # Alleen DDDDDDDD invoeren, +31-6-DDDDDDDD tonen
        # Validatie: XXDDDDDDD of XDDDDDDDD
        self.driving_license_number = driving_license_number.upper()
        # Wordt automatisch ingesteld bij registratie
        self.registration_date = registration_date

    def __repr__(self):
        return f"<Traveller {self.first_name} {self.last_name}>"


class Scooter:
    def __init__(self, scooter_id, brand, model, serial_number, top_speed, battery_capacity,
                 state_of_charge, target_soc_range, location_lat, location_long,
                 out_of_service, mileage, last_maintenance_date):
        self.scooter_id = scooter_id  # intern ID
        self.brand = brand.strip().title()
        self.model = model.strip()
        self.serial_number = serial_number.upper()  # 10–17 alphanumeric

        self.top_speed = float(top_speed)  # in km/h
        self.battery_capacity = int(battery_capacity)  # in Wh
        self.state_of_charge = float(state_of_charge)  # in %, 0–100

        # tuple: (min%, max%), e.g., (20.0, 80.0)
        self.target_soc_range = target_soc_range

        self.location_lat = round(float(location_lat), 5)
        self.location_long = round(float(location_long), 5)

        # True if in maintenance or low battery
        self.out_of_service = bool(out_of_service)
        self.mileage = float(mileage)  # in km
        # string of ISO 8601: YYYY-MM-DD
        self.last_maintenance_date = last_maintenance_date

    def __repr__(self):
        return f"<Scooter {self.brand} {self.model}, Serial: {self.serial_number}>"


class UserRole(Enum):
    SUPER_ADMIN = "Super Administrator"
    SYSTEM_ADMIN = "System Administrator"
    SERVICE_ENGINEER = "Service Engineer"


class User:
    def __init__(self, user_id, username, password_hash, email, role: UserRole):
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash  # Wachtwoord wordt gehashed opgeslagen
        self.email = email.lower()
        self.role = role

    def __repr__(self):
        return f"<User {self.username} ({self.role.value})>"
