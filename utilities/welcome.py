def welcome_message():
    try:
        with open("banner.txt", encoding="utf8") as f:
            contents = f.read()
            print(f"\n{contents}")
    except OSError:
        print(
            "\niCaLQ: Indirect LHC-Limits Calculator for Leptoquark models\nAlpha version\n"
        )
