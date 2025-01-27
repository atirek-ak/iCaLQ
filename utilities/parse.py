import sys
from functools import cmp_to_key
from typing import Any

from utilities.constants import chirality_index, lepton_index, quark_index
from utilities.data_classes import LeptoquarkParameters



def sortCouplingsAndValuesInteractive(leptoquark_parameters: LeptoquarkParameters):
    """
    Sort coupling and values so that the correct efficiency files can be read for interactive mode
    """
    for _, coupling_value in enumerate(leptoquark_parameters.couplings_values):
        combined_couplings_and_values = zip(
            leptoquark_parameters.couplings, coupling_value
        )
        sorted_combined_couplings_and_values = sorted(
            combined_couplings_and_values, key=cmp_to_key(compareCouplings)
        )
        sorted_combined_couplings_and_values = list(
            zip(*sorted_combined_couplings_and_values)
        )
        leptoquark_parameters.sorted_couplings = list(
            sorted_combined_couplings_and_values[0]
        )
        leptoquark_parameters.sorted_couplings_values.append(
            list(sorted_combined_couplings_and_values[1])
        )
