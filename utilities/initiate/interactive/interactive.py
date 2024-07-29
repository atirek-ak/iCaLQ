from utilities.constants import (
    luminosity_tau,
    default_ignore_single_pair_processes,
    default_significane,
    default_systematic_error,
    default_decay_width_constant,
    InputMode
)
from utilities.data_classes import NonInteractiveInputParameters
from utilities.validate import validateInputData, checkIfFilesExist
from utilities.parse import sortCouplingsAndValues
from utilities.colour import prCyan, prRed, prCyanNoNewLine
from calculate import calculate


def initiateInteractive():
    """
    Initiate procedure for interactive mode
    """
    # initialize leptoquark model values
    leptoquark_model = ""
    leptoquark_mass = ""
    couplings = ""
    ignore_single_pair_processes = default_ignore_single_pair_processes
    significance = default_significane
    systematic_error = default_systematic_error
    decay_width_constant = default_decay_width_constant
    luminosity = luminosity_tau

    printDefaultValues(ignore_single_pair_processes, significance, systematic_error, decay_width_constant, luminosity) 

    # loop to input values. we will have to add validations here only
    while True:
        prCyanNoNewLine("calq > ")
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
            elif s[1].strip() == "2":
                significance = 2
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
            printHelp()
        elif s[0].strip() == "initiate":
            leptoquark_parameters, _ = validateInputData(leptoquark_model, leptoquark_mass, couplings, ignore_single_pair_processes, significance, systematic_error, decay_width_constant, luminosity)
            leptoquark_parameters.couplings_values = [" ".join(["0"] * len(couplings))]
            calculate(leptoquark_parameters, InputMode.INTERACTIVE)
        elif s[0].strip().lower() in ["exit", "q", "exit()", ".exit"]:
            return
        elif s[0].strip() == "":
            continue
        else:
            prRed(f"Command {s[0]} not recognised. Please retry or enter 'q' to exit.")


def printDefaultValues(ignore_single_pair_processes: str, significance: int, systematic_error: str, decay_width_constant: int, luminosity: int):
    print("Default values:")
    print(f"ignore_single_pair = {ignore_single_pair_processes}")
    print(f"significance = {significance}")
    print(f"systematic_error = {systematic_error}")
    print(f"decay_width_constant = {decay_width_constant}")
    print(f"luminosity = {luminosity}")

def printHelp():
    """
    Content to be printed when help is inputted
    """
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