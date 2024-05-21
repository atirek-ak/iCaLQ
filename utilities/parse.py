import sys
from typing import Any, List
from functools import cmp_to_key

from utilities.constants import scalar_leptoquark_models, vector_leptoquark_models
from utilities.data_classes import LeptoquarkParameters


def compare_coupling(item1: Any, item2: Any) -> int:
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


def sort_couplings_and_values(
    leptoquark_parameters: LeptoquarkParameters
):
    """
    Sort coupling and values so that the correct efficiency files can be read
    """
    for coupling_value, line_number in leptoquark_parameters.couplings_values:
        if len(coupling_value) != len(leptoquark_parameters.couplings):
            sys.exit(f"[Query Error]: Coupling values length in line {line_number} is {coupling_value} which does not match the length of input couplings {leptoquark_parameters.couplings}")
    for coupling_value in leptoquark_parameters.couplings_values:

        combined_couplings_and_values = zip(leptoquark_parameters.couplings, coupling_value)
        sorted_combined_couplings_and_values = sorted(combined_couplings_and_values, key=cmp_to_key(compare_coupling))
        sorted_combined_couplings_and_values = list(zip(*sorted_combined_couplings_and_values))
        leptoquark_parameters.sorted_couplings = list(sorted_combined_couplings_and_values[0])
        leptoquark_parameters.sorted_couplings_values.append(list(sorted_combined_couplings_and_values[1]))


def parse_lam(original_lambdastring, lam_val_f):
    """
    Parsing queries while in interactive mode
    """
    lam_val_f = lam_val_f.replace(",", " ")
    original_lam_vals = [lam_val_f.strip().split()]
    combined_lambda = zip(original_lambdastring, original_lam_vals[0])
    combined_lambda = sorted(combined_lambda, key=cmp_to_key(compare_coupling))
    combined_lambda = list(zip(*combined_lambda))
    temp_lam_vals = [list(combined_lambda[1])]
    return temp_lam_vals, original_lam_vals


def get_lam_separate(lam):
    """
    Separate sympy lambda symbols and lambda strings
    """
    ee_lam = []
    mumu_lam = []
    tautau_lam = []
    ee_ls = []
    mumu_ls = []
    tautau_ls = []

    for lamda in lam:
        temp_str_sym = str(lamda)
        if temp_str_sym[8] == "1":
            ee_lam.append(lamda)
            ee_ls.append(temp_str_sym)
        elif temp_str_sym[8] == "2":
            mumu_lam.append(lamda)
            mumu_ls.append(temp_str_sym)
        elif temp_str_sym[8] == "3":
            tautau_lam.append(lamda)
            tautau_ls.append(temp_str_sym)
    return [ee_lam, mumu_lam, tautau_lam], [ee_ls, mumu_ls, tautau_ls]
