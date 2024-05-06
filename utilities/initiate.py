import sys
import random

from utilities.constants import (
    chi_sq_limits_1,
    chi_sq_limits_2,
    luminosity_tau
)
from utilities.validate import validate_input_data, check_input_files_exits
from utilities.parse import sort_couplings_and_values
from utilities.colour import prCyan, prRed, prCyanNoNewLine
from calculate import home

chi_sq_limits = chi_sq_limits_2

def initiate_with_files(input_card_file: str, input_couplings_values_file: str, output_yes_file: str, output_no_file: str):
    """
    Initiate procedure if non-interactive input is given

    :param input_card_file: File path to the .card file for non-interactive input
    :param input_couplings_values_file: File path to the .vals file(values file) for non-interactive input
    :param output_yes_file: File path of the output file (allowed values)
    :param output_no_file: File path of the output file (disallowed values)
    """
    global chi_sq_limits
    check_input_files_exits(input_card_file, input_couplings_values_file)
    
    # read the cards file
    with open(input_card_file, encoding="utf8") as c:
        input_card_lines = c.readlines()
    if len(input_card_lines) < 8:
        sys.exit(f"Number of lines in file: {len(input_card_lines)}, expected 8. Please refer to README to check if all the data is present.")

    # extract card data
    leptoquark_model = input_card_lines[0].split("#")[0].strip()
    leptoquark_mass = input_card_lines[1].split("#")[0].strip()
    couplings = input_card_lines[2].split("#")[0].strip()
    ignore_single_pair_processes = input_card_lines[3].split("#")[0].strip()
    significance = input_card_lines[4].split("#")[0].strip()
    systematic_error = input_card_lines[5].split("#")[0].strip()
    decay_width_constant = input_card_lines[6].split("#")[0].strip()
    luminosity = input_card_lines[7].split("#")[0].strip()
    random_points = input_card_lines[8].split("#")[0].strip()

    # validate data
    # since chi_sq_limits is a global variable, it is validated here, instead of the validation function
    # TODO: check if it can be done without global values
    if significance == "1":
        chi_sq_limits = chi_sq_limits_1
    elif significance == "2":
        chi_sq_limits = chi_sq_limits_2
    else:
        sys.exit(
            "[Sigma Error]: Line 4 of input card must contain either 1 or 2 as the sigma value. Exiting."
        )
    leptoquark_paramters, random_points = validate_input_data(leptoquark_model, leptoquark_mass, couplings, ignore_single_pair_processes, significance, systematic_error, decay_width_constant, luminosity, random_points):

    # update vals file value with random points if needed
    if random_points > 0:
        f = open(input_couplings_values_file, "w")
        for _ in range(random_points): 
            coupling_values_list = [str(random.uniform(-3.5, 3.5)) for _ in range(len(couplings))]
            coupling_values_string = " ".join(coupling_values_list)
            f.write(f"{coupling_values_string}\n")
        f.close()


    # read input coupling values file
    with open(input_couplings_values_file, encoding="utf8") as v:
        coupling_values_lines = v.readlines()
    home(
        *sort_couplings_and_values(
            leptoquark_mass,
            couplings,
            ignore_single_pair_processes,
            systematic_error,
            coupling_values_lines,
            leptoquark_model,
            luminosity,
        ),
        False,
        chi_sq_limits,
        decay_width_constant,
        input_couplings_values_file,
        output_yes_file,
        output_no_file,
    )


def initiate_interactive():
    """
    Initiate procedure if interactive
    """
    global chi_sq_limits
    leptoquark_model = ""
    leptoquark_mass = ""
    couplings = ""
    ignore_single_pair_processes = "no"
    significance = 2
    systematic_error = "0.1"
    decay_width_constant = 0
    luminosity = luminosity_tau
    coupling_values = []

    print("Default values:")
    print(f"ignore_single_pair = {ignore_single_pair_processes}")
    print(f"significance = {significance}")
    print(f"systematic_error = {systematic_error}")
    print(f"decay_width_constant = {decay_width_constant}")
    print(f"luminosity = {luminosity}")

    while True:
        prCyanNoNewLine("icalq > ")
        s = input().split("=")
        slen = len(s)
        if s[0].strip() == "import_model" and slen == 2:
            leptoquark_model = s[1].strip()
        elif s[0].strip() == "mass" and slen == 2:
            leptoquark_mass = s[1].strip()
        elif s[0].strip() == "couplings" and slen > 1:
            couplings = s[1].strip()
        elif s[0].strip() == "ignore_single_pair" and slen == 2:
            ignore_single_pair_processes = s[1].strip()
        elif s[0].strip() == "significance" and slen == 2:
            if s[1].strip() == "1":
                significance = 1
                chi_sq_limits = chi_sq_limits_1
            elif s[1].strip() == "2":
                significance = 2
                chi_sq_limits = chi_sq_limits_2
            else:
                prRed("Allowed values of 'significance': 1 or 2")
        elif s[0].strip() == "systematic_error" and slen == 2:
            systematic_error = s[1].strip()
        elif s[0].strip() == "decay_width_constant" and slen == 2:
            decay_width_constant = float(s[1].strip())
        elif s[0].strip() == "luminosity" and slen == 2:
            luminosity = float(s[1].strip())
        elif s[0].strip() == "status":
            print(f"Leptoquark Model = {leptoquark_model}")
            print(f"Leptoquark mass: {leptoquark_mass}")
            print(f"Couplings: {couplings}")
            print(f"Ignore Single & Pair processes= {ignore_single_pair_processes}")
            print(f"Significance = {significance}")
            print(f"Decay Width constant = {decay_width_constant}")
            print(f"Luminosity = {luminosity} MeV")
        elif s[0].strip() == "help":
            prCyan("Commands with '=' expect appropriate value. Read README.md for more info on individual commands.")
            prCyan("Value input commands: ")
            print("import_model= [Leptoquark model]")
            print("mass= [Leptoquark mass]")
            print("couplings= [Couplings. For the format, refer to README]")
            print("ignore_single_pair= [If true, the contribution from single & pair production processes is ignored]")
            print("significance= [Significance determines the limit of the chi-square test. Possible values=1,2]")
            print("systematic_error= [Systematic error to be included in the calculations. Should be from 0 to 1]")
            print("decay_width_constant= [Leptoquark mass]")
            print("luminosity= [Luminosity at which the processes happen]")
            prCyan("Other commands:")
            print("status [To print currently set values]")
            print("initiate [To start the calcualations]")
            print("exit [To exit out of the calculator]")
        elif s[0].strip() == "initiate":
            leptoquark_paramters, random_points = validate_input_data(leptoquark_model, leptoquark_mass, couplings, ignore_single_pair_processes, significance, systematic_error, decay_width_constant, luminosity, random_points):
            coupling_values = [" ".join(["0"] * len(couplings))]
            
            home(
                *sort_couplings_and_values(
                    leptoquark_mass,
                    couplings,
                    ignore_single_pair_processes,
                    systematic_error,
                    coupling_values,
                    leptoquark_model,
                    luminosity,
                ),
                True,
                chi_sq_limits,
                decay_width_constant,
            )
        elif s[0].strip().lower() in ["exit", "q", "exit()", ".exit"]:
            return
        elif s[0].strip() == "":
            continue
        else:
            prRed(
                f"Command {s[0]} not recognised. Please retry or enter 'q' to exit."
            )

