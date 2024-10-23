from utilities.constants import scalar_leptoquark_models, vector_leptoquark_models, minimum_leptoquark_mass, maximum_leptoquark_mass
from utilities.colour import prRed


def validateLeptoQuarkModel(
    leptoquark_model: str,
) -> bool:
    if leptoquark_model not in scalar_leptoquark_models and leptoquark_model not in vector_leptoquark_models:
        prRed(f"Not a valid lepqtoquark model. Allowed models: {scalar_leptoquark_models + vector_leptoquark_models}")
        return False
    return True


def validateLeptoQuarkMass(
    leptoquark_mass: str, 
) -> bool:
    try:
        leptoquark_mass = float(leptoquark_mass)
        if leptoquark_mass < minimum_leptoquark_mass or leptoquark_mass > maximum_leptoquark_mass:
            prRed(f"Leptoquark mass should be from {minimum_leptoquark_mass} to {maximum_leptoquark_mass} GeV")
            return False
    except:
        prRed("Leptoquark mass should be a valid number")
        return False
    return True

def validateLeptoQuarkCouplings(
    couplings: str, 
    leptoquark_model: str,
) -> bool:
    couplings_list = couplings.strip().split(' ')
    if not len(couplings_list):
        prRed("Couplings cannot be empty. For valid format, refer to README")
        return False
    for i in range(len(couplings_list)):
        if len(couplings_list[i]) != 10:
            prRed(f"The couplings input {couplings_list[i]} is not 10 characters. For valid format, refer to README")
            return False
        if not (
            (couplings_list[i][0] == 'Y' and leptoquark_model in scalar_leptoquark_models)
            or (couplings_list[i][0] == 'X' and leptoquark_model in vector_leptoquark_models)
        ):
            prRed("For scalar leptoquarks, the first letter should be Y & for vector leptoquarks it should be X. For valid format, refer to README")
            return False
        if couplings_list[i][1:3] != "10":
            prRed(f"The second and third characters of {couplings_list[i]} should be '10'. For valid format, refer to README")
            return False
        if couplings_list[i][3] not in ["L", "R"]:
            prRed(f"The 4th character of {couplings_list[i]} should be either L or R for left-handed & right-handed couplings respectively. For valid format, refer to README")
            return False
        if couplings_list[i][4] not in ["L", "R"]:
            prRed(f"The 5th character of {couplings_list[i]} should be either L or R for left-handed & right-handed couplings respectively. For valid format, refer to README")
            return False
        if couplings_list[i][5] != '[':
            prRed(f"The 6th character of {couplings_list[i]} should be '['. For valid format, refer to README")
            return False
        if (leptoquark_model in scalar_leptoquark_models and couplings_list[i][6] not in ["1", "2"]) or (leptoquark_model in vector_leptoquark_models and couplings_list[i][6] not in ["1", "2", "3"]):
            prRed(f"The 7th character of {couplings_list[i]} should be a valid quark generation. For valid format, refer to README")
            return False
        if couplings_list[i][7] != ',':
            prRed(f"The 8th character of {couplings_list[i]} should be ','. For valid format, refer to README")
            return False
        if couplings_list[i][8] not in ["1", "2", "3"]:
            prRed(f"The 9th character of {couplings_list[i]} should be a valid lepton generation. For valid format, refer to README")
            return False
        if couplings_list[i][9] != ']':
            prRed(f"The 10th character of {couplings_list[i]} should be ']'. For valid format, refer to README")
            return False
    return True


def validateIgnoreSinglePairProduction(
    ignore_single_pair_processes: str, 
) -> bool:
    if ignore_single_pair_processes.lower() in {"yes", "y", "no", "n"}:
        return True
    prRed("ignore_single_pair takes input either 'yes'/'y' or 'no'/'n'")
    return False

def validateSignificance(
    significance: str, 
) -> bool:
    try:
        significance = int(significance)
        if significance != 1 and significance != 2:
            prRed("Significance should be a valid number: either 1 or 2")
            return False
    except:
        prRed("Significance should be a valid number: either 1 or 2")
        return False
    return True

def validateSystematicError(
    systematic_error: str,
) -> bool:
    try:
        systematic_error = float(systematic_error)
        if systematic_error < 0 or systematic_error > 1:
            prRed("Systematic error should be a valid number from 0 to 1.")
            return False
    except:
        prRed("Systematic error should be a valid number from 0 to 1.")
        return False
    return True

def validateExtraWidth(
    extra_width: str,
):
    # validate extra width
    try:
        extra_width = float(extra_width)
    except:
        prRed("Extra Width constant should be a valid number")
        return False
    return True