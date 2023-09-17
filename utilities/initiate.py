import sys

from utilities.constants import chi_sq_limits_1, chi_sq_limits_2
from utilities.validate import ready_to_initiate
from utilities.parse import parse
from utilities.colour import prCyan, prRed
from calculate import home

chi_sq_limits = chi_sq_limits_2


def initiate_with_files(card: str, vals: str, output_yes: str, output_no: str):
    """
    Initiate procedure if non-interactive input is given

    :param card: File path to the .card file for non-interactive input
    :param vals: File path to the .vals file(values file) for non-interactive input
    :param output_yes: File path of the output file (allowed values)
    :param output_no: File path of the output file (disallowed values)
    """
    global chi_sq_limits
    try:
        with open(card) as c:
            c_lines = c.readlines()
    except OSError:
        sys.exit(f"Card file {card} does not exist. Exiting.")
    try:
        with open(vals) as v:
            v_lines = v.readlines()
    except OSError:
        sys.exit(f"Values file {vals} does not exist. Exiting.")
    if len(c_lines) < 5:
        sys.exit(f"Number of lines in file: {len(c_lines)}, expected 5. Exiting.")

    # extract data
    leptoquark_model = c_lines[0].split("#")[0].strip()
    mass_f = c_lines[1].split("#")[0].strip()
    lambdas_f = c_lines[2].split("#")[0].strip()
    ignore_f = c_lines[3].split("#")[0].strip()
    sigma_f = c_lines[4].split("#")[0].strip()
    margin_f = c_lines[5].split("#")[0].strip()

    # validate data
    if sigma_f == "1":
        chi_sq_limits = chi_sq_limits_1
    elif sigma_f == "2":
        chi_sq_limits = chi_sq_limits_2
    else:
        sys.exit(
            "[Sigma Error]: Line 4 of input card must contain either 1 or 2 as the sigma value. Exiting."
        )
    if not (ready_to_initiate(mass_f, lambdas_f, ignore_f, margin_f)):
        sys.exit("[Input Error]: Syntax Error encountered in input card. Exiting.")

    home(
        *parse(mass_f, lambdas_f, ignore_f, margin_f, v_lines, leptoquark_model),
        False,
        chi_sq_limits,
        output_yes,
        output_no,
    )


def initiate_interactive():
    """
    Initiate procedure if interactive
    """
    global chi_sq_limits
    mass_f = ""
    lambdas_f = ""
    ignore_f = "yes"
    sigma_limit = 2
    margin_f = "0.1"
    lam_values_f = []
    leptoquark_model = ""
    print_initiate_message(
        "mass=, couplings=, systematic_error=, ignore_single_pair=(yes/no), significance=(1/2), import_model=, status, initiate, help\n",
        "Default Model loaded: U1",
        "Couplings available: LM11L, LM12L, LM13L, LM21L, LM22L, LM23L, LM31L, LM32L, LM33L, LM11R, LM12R, LM13R, LM21R, LM22R, LM23R, LM31R, LM32R, LM33R",
    )
    while True:
        prCyan("icalq > ")
        s = input().split("=")
        slen = len(s)
        if s[0].strip() == "mass" and slen == 2:
            mass_f = s[1].strip()
        elif s[0].strip() == "":
            continue
        elif s[0].strip() == "couplings" and slen > 1:
            lambdas_f = s[1].strip()
        elif s[0].strip() == "ignore_single_pair" and slen == 2:
            ignore_f = s[1].strip()
        elif s[0].strip() == "systematic_error" and slen == 2:
            margin_f = s[1].strip()
        elif s[0].strip() == "import_model" and slen == 2:
            # print("Currently only U1 model is available.")
            leptoquark_model = s[1].strip()
        elif s[0].strip() == "significance" and slen == 2:
            if s[1].strip() == "1":
                sigma_limit = 1
                chi_sq_limits = chi_sq_limits_1
            elif s[1].strip() == "2":
                sigma_limit = 2
                chi_sq_limits = chi_sq_limits_2
            else:
                prRed("Allowed values of 'significance': 1 or 2\n")
        elif s[0].strip() == "status":
            print(
                f"\nMass: {mass_f}\nCouplings: {lambdas_f}\nIgnore Single & Pair = {ignore_f}\nSignificance = {sigma_limit}\nSystematic-Error = {margin_f}"
            )
        elif s[0].strip() == "help":
            print_initiate_message(
                "mass=, couplings=, systematic-error=, ignore_single_pair=(yes/no), significance=(1/2), import_model=, status, initiate, help\n",
                "Couplings available: LM11L, LM12L, LM13L, LM21L, LM22L, LM23L, LM31L, LM32L, LM33L, LM11R, LM12R, LM13R, LM21R, LM22R, LM23R, LM31R, LM32R, LM33R",
                "commands with '=' expect appropriate value. Read README.md for more info on individual commands.\n",
            )
        elif s[0].strip() == "initiate":
            if not ready_to_initiate(mass_f, lambdas_f, ignore_f, margin_f):
                prRed(
                    "[Lambda Error]: Example of a valid input - 'LM23L LM33R LM12R'\n"
                )
                continue
            num_lam = len(lambdas_f.split())
            lam_values_f = [" ".join(["0"] * num_lam)]
            home(
                *parse(
                    mass_f,
                    lambdas_f,
                    ignore_f,
                    margin_f,
                    lam_values_f,
                    leptoquark_model,
                ),
                True,
                chi_sq_limits,
            )
        elif s[0].strip() in ["exit", "q", "exit()", ".exit"]:
            return
        else:
            prRed(
                f"Command {s[0]} not recognised. Please retry or enter 'q' to exit.\n"
            )


def print_initiate_message(arg0, arg1, arg2):
    print("Commands available: ", end="")
    prCyan(arg0)
    print(arg1)
    print(arg2)
