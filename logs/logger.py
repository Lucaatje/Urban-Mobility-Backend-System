def write_log(username, description, additional_info="", suspicious=False):
    from datetime import datetime
    import os

    log_file = "logs/system_log.txt"
    suspicious_str = "Yes" if suspicious else "No"
    now = datetime.now()
    date_str = now.strftime("%d-%m-%Y")
    time_str = now.strftime("%H:%M:%S")

    # Bepaal volgnummer
    if not os.path.exists(log_file):
        log_number = 1
    else:
        with open(log_file, "r", encoding="utf-8") as f:
            lines = [line for line in f if line.strip() and not line.startswith("No.")]
            log_number = len(lines)

    # Als bestand nog niet bestaat, koptekst toevoegen
    if log_number == 1:
        with open(log_file, "w", encoding="utf-8") as f:
            f.write("No.  | Date       | Time     | Username   | Description                        | Additional Info                  | Suspicious\n")
            f.write("-----|------------|----------|------------|------------------------------------|----------------------------------|-----------\n")

    # Schrijf nieuwe logregel
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{log_number:<5}| {date_str} | {time_str} | {username:<10} | {description:<34} | {additional_info:<32} | {suspicious_str}\n")
