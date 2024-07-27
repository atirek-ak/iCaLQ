import sys
import random
from typing import Tuple, List

from utilities.constants import (
    min_lambda_limit,
    max_lambda_limit,
    input_card_number_of_lines,
    InputMode
)
from utilities.data_classes import NonInteractiveInputParameters, LeptoquarkParameters
from utilities.validate import validate_input_data
from utilities.parse import sort_couplings_and_values
from utilities.colour import prCyan, prRed, prCyanNoNewLine
from utilities.initiate.non_interactive.validate import validateNonInteractiveInput
from calculate import calculate

def initiateNonInteractive(non_interactive_input_parameters: NonInteractiveInputParameters):
    """
    Initiate procedure if non-interactive input is given
    """
    global chi_sq_limits
    # validate non-interactive input parameters
    validateNonInteractiveInput(non_interactive_input_parameters)
    
    # read & validate the card data. Then parse it into LeptoquarkParameters object
    leptoquark_parameters, random_points = readCardData(non_interactive_input_parameters)
    # update random points in input vals file if required
    updateRandomPoints(random_points, leptoquark_parameters, leptoquark_parameters)
    # read input coupling values
    readInputCouplingValues(non_interactive_input_parameters, leptoquark_parameters)
    
    calculate(leptoquark_parameters, non_interactive_input_parameters, InputMode.NONINTERACTIVE)


def readCardData(non_interactive_input_parameters: NonInteractiveInputParameters) -> Tuple[LeptoquarkParameters, int]:
    """
    read and parse into object input card data
    """
    # read the cards file
    with open(non_interactive_input_parameters.input_card_path, encoding="utf8") as c:
        input_card_lines = c.readlines()
    if len(input_card_lines) != input_card_number_of_lines:
        sys.exit(f"Number of lines in file: {len(input_card_lines)}, expected {input_card_number_of_lines}. Please refer to README to check if all the data is present.")

    # extract card data
    # validating that each parameter is as said in the README
    leptoquark_model = input_card_lines[0].split("#")[0].strip()
    leptoquark_mass = input_card_lines[1].split("#")[0].strip()
    couplings = input_card_lines[2].split("#")[0].strip()
    ignore_single_pair_processes = input_card_lines[3].split("#")[0].strip()
    significance = input_card_lines[4].split("#")[0].strip()
    systematic_error = input_card_lines[5].split("#")[0].strip()
    decay_width_constant = input_card_lines[6].split("#")[0].strip()
    luminosity = input_card_lines[7].split("#")[0].strip()
    random_points = input_card_lines[8].split("#")[0].strip()

    # Create the leptoquarkParameters class instance
    # From here on, this will be used for referencing to any input data and has all information
    return validate_input_data(leptoquark_model, leptoquark_mass, couplings, ignore_single_pair_processes, significance, systematic_error, decay_width_constant, luminosity, random_points)

def updateRandomPoints(random_points: int, non_interactive_input_parameters: NonInteractiveInputParameters, leptoquark_parameters: LeptoquarkParameters):
    """
    update vals file value with random points if random points > 0
    """
    if random_points > 0:
        f = open(non_interactive_input_parameters.input_values_path, "w")
        for _ in range(random_points): 
            coupling_values_list = [str(random.uniform(min_lambda_limit, max_lambda_limit)) for _ in range(len(leptoquark_parameters.couplings))]
            coupling_values_string = " ".join(coupling_values_list)
            f.write(f"{coupling_values_string}\n")
        f.close()

def readInputCouplingValues(non_interactive_input_parameters: NonInteractiveInputParameters, leptoquark_parameters: LeptoquarkParameters):
    """
    read, parse & validate input coupling values file
    """
    with open(non_interactive_input_parameters.input_values_path) as v:
        leptoquark_parameters.couplings_values = v.readlines()

        # parse the coupling values data
        coupling_values = []
        for coupling_value in leptoquark_parameters.couplings_values:
            coupling_value = coupling_value.strip('\n').strip().split(' ')
            coupling_values.append(coupling_value)
        leptoquark_parameters.couplings_values = coupling_values

    sort_couplings_and_values(leptoquark_parameters)