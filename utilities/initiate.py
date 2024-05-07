import sys
import random

from utilities.constants import (
    chi_sq_limits_1,
    chi_sq_limits_2,
    luminosity_tau
)
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
        with open(card, encoding="utf8") as c:
            c_lines = c.readlines()
    except OSError:
        sys.exit(f"Card file {card} does not exist. Exiting.")
    if len(c_lines) < 9:
        sys.exit(f"Number of lines in file: {len(c_lines)}, expected 8. Exiting.")

    # extract data
    leptoquark_model = c_lines[0].split("#")[0].strip()
    mass_f = c_lines[1].split("#")[0].strip()
    lambdas_f = c_lines[2].split("#")[0].strip()
    ignore_f = c_lines[3].split("#")[0].strip()
    sigma_f = c_lines[4].split("#")[0].strip()
    margin_f = c_lines[5].split("#")[0].strip()
    width_constant = c_lines[6].split("#")[0].strip()
    luminosity = c_lines[7].split("#")[0].strip()
    random_points = int(c_lines[8].split("#")[0].strip())
    # validate data
    if sigma_f == "1":
        chi_sq_limits = chi_sq_limits_1
    elif sigma_f == "2":
        chi_sq_limits = chi_sq_limits_2
    else:
        sys.exit(
            "[Sigma Error]: Line 4 of input card must contain either 1 or 2 as the sigma value. Exiting."
        )
    if not (ready_to_initiate(mass_f, lambdas_f, ignore_f, margin_f, leptoquark_model)):
        sys.exit("[Input Error]: Syntax Error encountered in input card. Exiting.")

    width_constant = float(width_constant)

    # update vals file value with random points if needed
    if random_points > 0:
        f = open(vals, "w")
        for _ in range(random_points): 
            vals_list = [str(random.uniform(-3.5, 3.5)) for _ in range(len(lambdas_f.split(' ')))]
            vals_string = " ".join(vals_list)
            f.write(f"{vals_string}\n")
        f.close()

    try:
        with open(vals, encoding="utf8") as v:
            v_lines = v.readlines()
    except OSError:
        sys.exit(f"Values file {vals} does not exist. Exiting.")
    home(
        *parse(
            mass_f,
            lambdas_f,
            ignore_f,
            margin_f,
            v_lines,
            leptoquark_model,
            luminosity,
        ),
        False,
        chi_sq_limits,
        width_constant,
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
    ignore_f = "no"
    sigma_limit = 2
    margin_f = "0.1"
    lam_values_f = []
    leptoquark_model = ""
    width_constant = 0
    luminosity = luminosity_tau
    print_initiate_message(
        "mass=, couplings=, systematic_error=, ignore_single_pair=(yes/no), significance=(1/2), import_model=, width_constant=, status, initiate, help\n",
        "",
        "Couplings available: \n S1 Leptoquark examples: Y10LL[1,1],Y10LL[2,2],Y10RR[3,1]\n U1 Leptoquark examples: :X10LL[1,1],X10LL[3,2],X10RR[1,1]",
    )
    print("Default values set:")
    print(f"ignore_single_pair = {ignore_f}")
    print(f"significance = {sigma_limit}")
    print(f"systematic_error = {margin_f}")
    print(f"width_constant = {width_constant}")
    print(f"luminosity = {luminosity}")

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
            leptoquark_model = s[1].strip()
        elif s[0].strip() == "width_constant" and slen == 2:
            width_constant = float(s[1].strip())
        elif s[0].strip() == "luminosity" and slen == 2:
            luminosity = float(s[1].strip())
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
                f"Mass: {mass_f}\nCouplings: {lambdas_f}\nIgnore Single & Pair = {ignore_f}\nSignificance = {sigma_limit}\nSystematic-Error = {margin_f}\nModel = {leptoquark_model}\nWidth constant = {width_constant}"
            )
        elif s[0].strip() == "help":
            print_initiate_message(
                "mass=, couplings=, systematic_error=, ignore_single_pair=(yes/no), significance=(1/2), import_model=, width_constant=, luminosity=, status, initiate, help\n",
                "Couplings available: \n S1 Leptoquark examples: Y10LL[1,1],Y10LL[2,2],Y10RR[3,1]\n U1 Leptoquark examples: :X10LL[1,1],X10LL[3,2],X10RR[1,1]",
                "commands with '=' expect appropriate value. Read README.md for more info on individual commands.\n",
            )
        elif s[0].strip() == "initiate":
            if not ready_to_initiate(
                mass_f, lambdas_f, ignore_f, margin_f, leptoquark_model
            ):
                prRed(
                    "[Lambda Error]: Example of a valid input - 'Y10LL[2,1] Y10LL[3,1] Y10RR[1,1]'\n"
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
                    luminosity,
                ),
                True,
                chi_sq_limits,
                width_constant,
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
