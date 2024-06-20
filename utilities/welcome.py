from datetime import datetime

def welcome_message():
    try:
        with open("banner.txt", encoding="utf8") as f:
            contents = f.read()
            print(f"\n{contents}")
            print(f"{datetime.now().strftime('%B %Y')}")
    except OSError:
        print(
            "\nCaLQ: Calculator for LHC limits on leptoquarks"
        )
