import os
from typing import List
from helper.output import pr_red

def create_files_if_not_present(files: List[str]):
    for file in files:
        if file != "" and not os.path.isfile(file):
            with open(file, "w") as _:
                pass

def validate_interactive_input_coupling_values(
        coupling_values_input_interactive: str, couplings_length: int
) -> bool:
    coupling_values = coupling_values_input_interactive.strip().split(' ')
    if len(coupling_values) != couplings_length:
        pr_red(
            f"[Query error]: Please input {couplings_length} couplings values input.")
        return False
    try:
        for i in range(couplings_length):
            _ = float(coupling_values[i].strip())
    except ValueError:
        pr_red(f"[Query error]: Please enter numerical values as input")
        return False
    return True