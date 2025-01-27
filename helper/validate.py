import os
from typing import List

def create_files_if_not_present(files: List[str]):
    for file in files:
        if file != "" and not os.path.isfile(file):
            with open(file, "w") as file:
                pass
