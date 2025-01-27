# Specific use-case output functions
import json
from utilities.constants import file_paths_config_file_path

def print_welcome_banner():
    try:
        with open(file_paths_config_file_path, 'r') as config_file:
            config = json.load(config_file)
            with open(config.get("banner", ""), encoding="utf8") as f:
                contents = f.read()
                print(contents)
    except OSError:
        print("CaLQ: Calculator for LHC limits on leptoquarks")
        print("Version 1.0.0")
