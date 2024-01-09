import sys
from typing import Any
from functools import cmp_to_key

from utilities.constants import scalar_leptoquark_models, vector_leptoquark_models


def compare_lambda(item1: Any, item2: Any) -> int:
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


def parse(
    mass_f: str,
    lambdas_f: str,
    ignore_f: str,
    margin_f: str,
    lam_values_f: list[str],
    leptoquark_model: str,
):
    """
    Parsing string input to their appropriate format. Outputs to be used by home function.

    :param mass_f: Leptoquark mass
    :param lambdas_f: Lambda couplings
    :param ignore_f: Ignore single and pair production
    :param margin_f: Systematic error
    :param lambdas_f: Lambda couplings values
    """
    # convert to correct data types
    mass = float(mass_f)
    margin = float(margin_f)
    original_lambdastring = lambdas_f.strip().split()
    ignorePairSingle = ignore_f.strip().lower() in {"yes", "y"}
    original_lam_vals = []
    temp_lam_vals = []
    lambdastring = []
    for val in lam_values_f:
        val = val.replace(",", " ")
        try:
            if len(val.strip().split()) != len(original_lambdastring):
                raise ValueError()
            for x in val.strip().split():
                float(x)
        except ValueError:
            print(original_lambdastring)
            sys.exit(
                f"[Query Error]: Query values for lambdas are either not {len(original_lambdastring)} (number of lambdas) in count or not convertible to float."
            )
        original_lam_vals.append(val.strip().split())
    for lam_val in original_lam_vals:
        combined_lambda = zip(original_lambdastring, lam_val)
        combined_lambda = sorted(combined_lambda, key=cmp_to_key(compare_lambda))
        combined_lambda = list(zip(*combined_lambda))
        lambdastring = list(combined_lambda[0])
        temp_lam_vals.append(list(combined_lambda[1]))
    lam_vals = temp_lam_vals
    if leptoquark_model not in scalar_leptoquark_models + vector_leptoquark_models:
        raise ValueError(
            f"Model inputted should belong to {scalar_leptoquark_models + vector_leptoquark_models}"
        )
    return (
        mass,
        lambdastring,
        original_lambdastring,
        ignorePairSingle,
        lam_vals,
        original_lam_vals,
        margin,
        leptoquark_model,
    )


def parse_lam(original_lambdastring, lam_val_f):
    """
    Parsing queries while in interactive mode
    """
    lam_val_f = lam_val_f.replace(",", " ")
    original_lam_vals = [lam_val_f.strip().split()]
    combined_lambda = zip(original_lambdastring, original_lam_vals[0])
    combined_lambda = sorted(combined_lambda, key=cmp_to_key(compare_lambda))
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
