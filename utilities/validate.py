import os
from typing import Tuple, List

from utilities.colour import prRed
from utilities.constants import scalar_leptoquark_models, vector_leptoquark_models, minimum_leptoquark_mass_supported, maximum_leptoquark_mass_supported
from utilities.data_classes import LeptoquarkParameters

def checkIfFilesExist(files: List[str]):
    for file in files:
        if not os.path.isfile(file):
            raise Exception(f"File {file} could not be found. Please check if the input path is correct")


def validateInputData(
    leptoquark_model: str,
    leptoquark_mass: str, 
    couplings: str, 
    ignore_single_pair_processes: str, 
    significance: str, 
    systematic_error: str,
    decay_width_constant: str,
    luminosity: str,
    random_points: str = "0",
) -> Tuple[LeptoquarkParameters, int]:
    """
    Validate the data from both interactive and non-interactive modes and raise corresponding errors for the user to understand the issue
    After validating, convert the data to the appropriate type, & return a class that can be used throughout instead of passing multiple variables
    """
    # validate leptoquark model
    if leptoquark_model not in scalar_leptoquark_models and leptoquark_model not in vector_leptoquark_models:
        raise ValueError(f"Not a valid lepqtoquark model. Allowed models: {scalar_leptoquark_models.append(vector_leptoquark_models)}")

    # validate leptoquark mass
    try:
        leptoquark_mass = float(leptoquark_mass)
    except:
        raise ValueError("Leptoquark mass should be a valid number")
    if leptoquark_mass < minimum_leptoquark_mass_supported or leptoquark_mass > maximum_leptoquark_mass_supported:
        raise ValueError(f"Leptoquark mass should range from {minimum_leptoquark_mass_supported} to {maximum_leptoquark_mass_supported} MeV")


    # validate couplings
    couplings_list = couplings.strip().split(' ')
    if not len(couplings_list):
        raise ValueError("Couplings cannot be empty. For valid format, refer to README")
    for i in range(len(couplings_list)):
        if len(couplings_list[i]) != 10:
            raise ValueError(f"The couplings input {couplings_list[i]} is not 10 characters. For valid format, refer to README")
        if not (
            (couplings_list[i][0] == 'Y' and leptoquark_model in scalar_leptoquark_models)
            or (couplings_list[i][0] == 'X' and leptoquark_model in vector_leptoquark_models)
        ):
            raise ValueError("For scalar leptoquarks, the first letter should be Y & for vector leptoquarks it should be X. For valid format, refer to README")
        if couplings_list[i][1:3] != "10":
            raise ValueError(f"The second and third characters of {couplings_list[i]} should be '10'. For valid format, refer to README")
        if couplings_list[i][3] not in ["L", "R"]:
            raise ValueError("The 4th character of {couplings_list[i]} should be either L or R for left-handed & right-handed couplings respectively. For valid format, refer to README")
        if couplings_list[i][4] not in ["L", "R"]:
            raise ValueError("The 5th character of {couplings_list[i]} should be either L or R for left-handed & right-handed couplings respectively. For valid format, refer to README")
        if couplings_list[i][5] != '[':
            raise ValueError("The 6th character of {couplings_list[i]} should be '['. For valid format, refer to README")
        if (leptoquark_model in scalar_leptoquark_models and couplings_list[i][6] not in ["1", "2"]) or (leptoquark_model in vector_leptoquark_models and couplings_list[i][6] not in ["1", "2", "3"]):
            raise ValueError("The 7th character of {couplings_list[i]} should be a valid lepton generation. For valid format, refer to README")
        if couplings_list[i][7] != '[':
            raise ValueError("The 8th character of {couplings_list[i]} should be ','. For valid format, refer to README")
        if couplings_list[i][8] not in ["1", "2", "3"]:
            raise ValueError("The 9th character of {couplings_list[i]} should be a valid quark generation. For valid format, refer to README")
        if couplings_list[i][9] != ']':
            raise ValueError("The 10th character of {couplings_list[i]} should be ']'. For valid format, refer to README")
    couplings = couplings_list

    # validate Ignore single and pair production
    if ignore_single_pair_processes.lower() in {"yes", "y"}:
        ignore_single_pair_processes = True
    elif ignore_single_pair_processes.lower() in {"no", "n"}:
        ignore_single_pair_processes = False
    else:
        raise ValueError("ignore_single_pair takes input either 'yes'/'y' or 'no'/'n'")

    # validate significance
    try:
        significance = int(significance)
        if significance != 1 and significance != 2:
            raise ValueError("Significance should be a valid number: either 1 or 2")
    except:
        raise ValueError("Significance should be a valid number: either 1 or 2")

    # validate Systematic error
    try:
        systematic_error = float(systematic_error)
        if systematic_error < 0 or systematic_error > 1:
            raise ValueError("[Systematic error should be a valid number from 0 to 1.")
    except:
        raise ValueError("[Systematic error should be a valid number from 0 to 1.")
    
    # validate decay with constant
    try:
        decay_width_constant = float(decay_width_constant)
    except:
        raise ValueError("Decay Width constant should be a valid number")

    # validate luminosity
    try:
        luminosity = float(luminosity)
    except:
        raise ValueError("Luminsoity should be a valid number")
    
    # validate random points
    try:
        random_points = int(random_points)
        if random_points < 0:
            raise ValueError("Random points should be a non-negative integer")
    except:
        raise ValueError("Random points should be a valid number")
    
    # create Leptoquark data class
    leptoquark_parameters = LeptoquarkParameters(
        leptoquark_model=leptoquark_model,
        leptoquark_mass=leptoquark_mass,
        couplings=couplings,
        ignore_single_pair_processes=ignore_single_pair_processes,
        significance=significance,
        systematic_error=systematic_error,
        decay_width_constant=decay_width_constant,
        luminosity=luminosity,
    )

    # random points is returned seperately as it is not required during the calculations
    return leptoquark_parameters, random_points

    

def validateInteractiveInputCouplingValues(coupling_values_input_interactive: str, couplings_length: int) -> bool:
    """
    Check if queries are in correct form
    """
    coupling_values = coupling_values_input_interactive.split()
    if len(coupling_values) != couplings_length:
        prRed(f"[Query Error]: Please input {len(couplings_length)} couplings values input.")
        return False
    try:
        for i in range(couplings_length):
            _ = float(coupling_values[i])
    except ValueError:
        prRed(f"[Query Error]: Please input numerical values as input")
        return False
    return True
