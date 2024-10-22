from utilities.constants import scalar_leptoquark_models, vector_leptoquark_models
from utilities.colour import prRed

def validateInteractiveInputData(
    leptoquark_model: str,
    leptoquark_mass: str, 
    couplings: str, 
    ignore_single_pair_processes: str, 
    significance: str, 
    systematic_error: str,
    extra_width: str,
):
    """
    Validate the data from interactive mode and print corresponding errors for the user to understand the issue
    """
    # validate leptoquark model
    if leptoquark_model not in scalar_leptoquark_models and leptoquark_model not in vector_leptoquark_models:
        prRed(f"Not a valid lepqtoquark model. Allowed models: {scalar_leptoquark_models + vector_leptoquark_models}")
        return

    # validate leptoquark mass
    try:
        leptoquark_mass = float(leptoquark_mass)
    except:
        prRed("Leptoquark mass should be a valid number")
        return


    # validate couplings
    couplings_list = couplings.strip().split(' ')
    if not len(couplings_list):
        prRed("Couplings cannot be empty. For valid format, refer to README")
        return
    for i in range(len(couplings_list)):
        if len(couplings_list[i]) != 10:
            prRed(f"The couplings input {couplings_list[i]} is not 10 characters. For valid format, refer to README")
            return
        if not (
            (couplings_list[i][0] == 'Y' and leptoquark_model in scalar_leptoquark_models)
            or (couplings_list[i][0] == 'X' and leptoquark_model in vector_leptoquark_models)
        ):
            prRed("For scalar leptoquarks, the first letter should be Y & for vector leptoquarks it should be X. For valid format, refer to README")
            return
        if couplings_list[i][1:3] != "10":
            prRed(f"The second and third characters of {couplings_list[i]} should be '10'. For valid format, refer to README")
            return
        if couplings_list[i][3] not in ["L", "R"]:
            prRed("The 4th character of {couplings_list[i]} should be either L or R for left-handed & right-handed couplings respectively. For valid format, refer to README")
            return
        if couplings_list[i][4] not in ["L", "R"]:
            prRed("The 5th character of {couplings_list[i]} should be either L or R for left-handed & right-handed couplings respectively. For valid format, refer to README")
            return
        if couplings_list[i][5] != '[':
            prRed("The 6th character of {couplings_list[i]} should be '['. For valid format, refer to README")
            return
        if (leptoquark_model in scalar_leptoquark_models and couplings_list[i][6] not in ["1", "2"]) or (leptoquark_model in vector_leptoquark_models and couplings_list[i][6] not in ["1", "2", "3"]):
            prRed("The 7th character of {couplings_list[i]} should be a valid lepton generation. For valid format, refer to README")
            return
        if couplings_list[i][7] != ',':
            prRed("The 8th character of {couplings_list[i]} should be ','. For valid format, refer to README")
            return
        if couplings_list[i][8] not in ["1", "2", "3"]:
            prRed("The 9th character of {couplings_list[i]} should be a valid quark generation. For valid format, refer to README")
            return
        if couplings_list[i][9] != ']':
            prRed("The 10th character of {couplings_list[i]} should be ']'. For valid format, refer to README")
            return
    couplings = couplings_list

    # validate Ignore single and pair production
    if ignore_single_pair_processes.lower() in {"yes", "y"}:
        ignore_single_pair_processes = True
    elif ignore_single_pair_processes.lower() in {"no", "n"}:
        ignore_single_pair_processes = False
    else:
        prRed("ignore_single_pair takes input either 'yes'/'y' or 'no'/'n'")
        return

    # validate significance
    try:
        significance = int(significance)
        if significance != 1 and significance != 2:
            prRed("Significance should be a valid number: either 1 or 2")
            return
    except:
        prRed("Significance should be a valid number: either 1 or 2")
        return

    # validate Systematic error
    try:
        systematic_error = float(systematic_error)
        if systematic_error < 0 or systematic_error > 1:
            prRed("[Systematic error should be a valid number from 0 to 1.")
            return
    except:
        prRed("[Systematic error should be a valid number from 0 to 1.")
        return
    
    # validate extra width
    try:
        extra_width = float(extra_width)
    except:
        prRed("Extra Width constant should be a valid number")
        return