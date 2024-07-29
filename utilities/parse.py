import sys
from typing import Any
from functools import cmp_to_key

from utilities.constants import scalar_leptoquark_models, vector_leptoquark_models
from utilities.data_classes import LeptoquarkParameters


def compareCouplings(item1: Any, item2: Any) -> int:
    """
    Use this function as the comparator function while sorting lambdas
    """
    a1 = list(item1[0])
    a2 = list(item2[0])
    if a1[8] != a2[8]:
        return ord(a1[8]) - ord(a2[8])
    if a1[4] == a2[4]:
        return ord(a1[6]) - ord(a2[6])
    return -1 if a1[4] == "L" else 1


def sortCouplingsAndValues(
    leptoquark_parameters: LeptoquarkParameters
):
    """
    Sort coupling and values so that the correct efficiency files can be read
    """
    for coupling_value, line_number in leptoquark_parameters.couplings_values:
        if len(coupling_value) != len(leptoquark_parameters.couplings):
            sys.exit(f"[Query Error]: Coupling values length in line {line_number} is {coupling_value} which does not match the length of input couplings {leptoquark_parameters.couplings}")
        combined_couplings_and_values = zip(leptoquark_parameters.couplings, coupling_value)
        sorted_combined_couplings_and_values = sorted(combined_couplings_and_values, key=cmp_to_key(compareCouplings))
        sorted_combined_couplings_and_values = list(zip(*sorted_combined_couplings_and_values))
        leptoquark_parameters.sorted_couplings = list(sorted_combined_couplings_and_values[0])
        leptoquark_parameters.sorted_couplings_values.append(list(sorted_combined_couplings_and_values[1]))