from datetime import datetime
import os
from utils.data_encryption import encrypt, decrypt
from models.models import UserRole


def write_log(username, description, additional_info="", suspicious=False):
    log_file = "logs/system_log.txt"
    suspicious_str = "Yes" if suspicious else "No"
    now = datetime.now()
    date_str = now.strftime("%d-%m-%Y")
    time_str = now.strftime("%H:%M:%S")

    if not os.path.exists(log_file):
        log_number = 1
    else:
        with open(log_file, "r", encoding="utf-8") as f:
            lines = [line for line in f if line.strip()]
            log_number = len(lines) + 1

    if log_number == 1:
        header = "No.  | Date       | Time     | Username         | Description                              | Additional Info                  | Suspicious"
        encrypted_header = encrypt(header)
        separator = "-----|------------|----------|------------------|------------------------------------------|----------------------------------|-----------"
        encrypted_separator = encrypt(separator)

        with open(log_file, "w", encoding="utf-8") as f:
            f.write(encrypted_header + "\n")
            f.write(encrypted_separator + "\n")

    log_line = f"{log_number:<5}| {date_str} | {time_str} | {username:<18} | {description:<42} | {additional_info:<34} | {suspicious_str}"
    encrypted_line = encrypt(log_line)

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(encrypted_line + "\n")


def read_logs(logged_in_user):
    if logged_in_user.role not in [UserRole.SUPER_ADMIN, UserRole.SYSTEM_ADMIN]:
        print("❌ Access denied. Only system administrators may view the logs.")
        return

    log_file = "logs/system_log.txt"
    try:
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        print("\nlogs:\n")
        for line in lines:
            try:
                print(decrypt(line.strip()))
            except Exception:
                print("[⚠️ Unreadable log entry]")

    except FileNotFoundError:
        print("📂 Log file not found.")
