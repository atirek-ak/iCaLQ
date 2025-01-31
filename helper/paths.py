import os
from typing import List

def get_immediate_sub_directories(directory) -> List[str]:
    sub_directories = []

    for entry in os.listdir(directory):
        full_path = os.path.join(directory, entry)
        if os.path.isdir(full_path):
            sub_directories.append(entry)

    return sub_directories

def get_immediate_sub_directory_files(directory) -> List[str]:
    files = []

    for entry in os.listdir(directory):
        full_path = os.path.join(directory, entry)
        if os.path.isfile(full_path):
            files.append(entry)

    return files