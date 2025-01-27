import json
from typing import Tuple

from helper.output import pr_red
from utilities.constants import (maximum_leptoquark_mass,
                                 minimum_leptoquark_mass,
                                 scalar_leptoquark_models,
                                 vector_leptoquark_models,
                                 code_infra_config_file_path)
from utilities.data_classes import LeptoquarkParameters


def validateInteractiveInputCouplingValues(
    coupling_values_input_interactive: str, couplings_length: int
) -> bool:
    """
    Check if queries are in correct form
    """
    coupling_values = coupling_values_input_interactive.split()
    if len(coupling_values) != couplings_length:
        pr_red(
            f"[Query error]: Please input {couplings_length} couplings values input.")
        return False
    try:
        for i in range(couplings_length):
            _ = float(coupling_values[i])
    except ValueError:
        pr_red(f"[Query error]: Please enter numerical values as input")
        return False
    return True
