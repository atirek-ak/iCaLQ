def welcome_message():
    try:
        with open("banner.txt", encoding="utf8") as f:
            contents = f.read()
            print(f"{contents}")
    except OSError:
        print("iCaLQ: Indirect LHC-Limits Calculator for Leptoquark models")
        print("Alpha version")
