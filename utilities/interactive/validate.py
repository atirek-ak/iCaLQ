from helper.output import pr_red
from utilities.constants import (maximum_leptoquark_mass,
                                 minimum_leptoquark_mass,
                                 scalar_leptoquark_models,
                                 vector_leptoquark_models)


def validateLeptoQuarkModel(
    model: str,
) -> bool:
    if (
        model not in scalar_leptoquark_models
        and model not in vector_leptoquark_models
    ):
        pr_red(
            f"[Model error]: Not a valid lepqtoquark model. Allowed models: {scalar_leptoquark_models + vector_leptoquark_models}"
        )
        return False
    return True


def validateLeptoQuarkMass(
    mass: str,
) -> bool:
    try:
        mass = float(mass)
        if (
            mass < minimum_leptoquark_mass
            or mass > maximum_leptoquark_mass
        ):
            pr_red(
                f"[Mass error]: Leptoquark mass should be between {minimum_leptoquark_mass} GeV and {maximum_leptoquark_mass} GeV"
            )
            return False
    except:
        pr_red("[Mass error]: Leptoquark mass should be a valid number")
        return False
    return True


def validateLeptoQuarkCouplings(
    couplings: str,
    model: str,
) -> bool:
    couplings_list = couplings.strip().split(" ")

    # Count frequency of each element
    frequency = {}
    for item in couplings_list:
        if item in frequency:
            pr_red(
                f"[Couplings error]: Coupling {item} is repeated. A coupling can only be inputted once"
            )
            return False
        else:
            frequency[item] = 1

    if not len(couplings_list):
        pr_red(
            "[Couplings error]: Couplings cannot be empty. Refer to README.md for valid format"
        )
        return False
    for i in range(len(couplings_list)):
        if len(couplings_list[i]) != 10:
            pr_red(
                f"[Couplings error]: The couplings input {couplings_list[i]} is not 10 characters. Refer to README.md for valid format"
            )
            return False
        if not (
            (
                couplings_list[i][0] == "Y"
                and model in scalar_leptoquark_models
            )
            or (
                couplings_list[i][0] == "X"
                and model in vector_leptoquark_models
            )
        ):
            pr_red(
                "[Couplings error]: For scalar leptoquarks, the first letter should be Y & for vector leptoquarks, it should be X. Refer to README.md for valid format"
            )
            return False
        if couplings_list[i][1:3] != "10":
            pr_red(
                f"[Couplings error]: The second and third characters of {couplings_list[i]} should be '10'. Refer to README.md for valid format"
            )
            return False
        if couplings_list[i][3] not in ["L", "R"]:
            pr_red(
                f"[Couplings error]: The 4th character of {couplings_list[i]} should be either L or R for left-handed & right-handed couplings respectively. Refer to README.md for valid format"
            )
            return False
        if couplings_list[i][4] not in ["L", "R"]:
            pr_red(
                f"[Couplings error]: The 5th character of {couplings_list[i]} should be either L or R for left-handed & right-handed couplings respectively. Refer to README.md for valid format"
            )
            return False
        if couplings_list[i][5] != "[":
            pr_red(
                f"[Couplings error]: The 6th character of {couplings_list[i]} should be '['. Refer to README.md for valid format"
            )
            return False
        if (
            model in scalar_leptoquark_models
            and couplings_list[i][6] not in ["1", "2"]
        ) or (
            model in vector_leptoquark_models
            and couplings_list[i][6] not in ["1", "2", "3"]
        ):
            pr_red(
                f"[Couplings error]: The 7th character of {couplings_list[i]} should be a valid quark generation. Refer to README.md for valid format"
            )
            return False
        if couplings_list[i][7] != ",":
            pr_red(
                f"[Couplings error]: The 8th character of {couplings_list[i]} should be ','. Refer to README.md for valid format"
            )
            return False
        if couplings_list[i][8] not in ["1", "2", "3"]:
            pr_red(
                f"[Couplings error]: The 9th character of {couplings_list[i]} should be a valid lepton generation. Refer to README.md for valid format"
            )
            return False
        if couplings_list[i][9] != "]":
            pr_red(
                f"[Couplings error]: The 10th character of {couplings_list[i]} should be ']'. Refer to README.md for valid format"
            )
            return False
    return True


def validateIgnoreSinglePairProduction(
    ignore_single_pair_processes: str,
) -> bool:
    if ignore_single_pair_processes.lower() in {
        "yes",
        "y",
        "true",
        "t",
        "1",
        "no",
        "n",
        "false",
        "f",
        "0",
    }:
        return True
    pr_red(
        "[Ignore single pair production error]: ignore_single_pair takes input 'yes'/'y' or 'no'/'n'"
    )
    return False


def validateSignificance(
    significance: str,
) -> bool:
    try:
        significance = int(significance)
        if significance != 1 and significance != 2:
            pr_red("[Significance error]: Significance should be a valid number, 1 or 2")
            return False
    except:
        pr_red("[Significance error]: Significance should be a valid number, 1 or 2")
        return False
    return True


def validateSystematicError(
    systematic_error: str,
) -> bool:
    try:
        systematic_error = float(systematic_error)
        if systematic_error < 0 or systematic_error > 1:
            pr_red(
                "[Systematic error]: Systematic error should be a valid number between 0 and 1."
            )
            return False
    except:
        pr_red(
            "[Systematic error]: Systematic error should be a valid number between 0 and 1."
        )
        return False
    return True


def validateExtraWidth(
    extra_width: str,
):
    # validate extra width
    
