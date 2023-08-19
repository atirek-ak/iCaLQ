import sys

from utilities.constants import CHI_SQ_LIMITS_1, CHI_SQ_LIMITS_2
from utilities.validate import ready_to_initiate
from utilities.parse import parse

chi_sq_limits: list


def initiate_with_files(card: str, vals: str, output_yes: str, output_no: str):
    """
    Initiate procedure if non-interactive input is given

    :param card: File path to the .card file for non-interactive input
    :param vals: File path to the .vals file(values file) for non-interactive input
    :param output_yes: File path of the output file (allowed values)
    :param output_no: File path of the output file (disallowed values)
    """
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
    mass_f = c_lines[0].split("#")[0].strip()
    lambdas_f = c_lines[1].split("#")[0].strip()
    ignore_f = c_lines[2].split("#")[0].strip()
    sigma_f = c_lines[3].split("#")[0].strip()
    margin_f = c_lines[4].split("#")[0].strip()

    # validate data
    if sigma_f == "1":
        chi_sq_limits = CHI_SQ_LIMITS_1
    elif sigma_f == "2":
        chi_sq_limits = CHI_SQ_LIMITS_2
    else:
        sys.exit(
            "[Sigma Error]: Line 4 of input card must contain either 1 or 2 as the sigma value. Exiting."
        )
    if not (ready_to_initiate(mass_f, lambdas_f, ignore_f, margin_f)):
        sys.exit("[Input Error]: Syntax Error encountered in input card. Exiting.")

    # home(
    #     *parse(mass_f, lambdas_f, ignore_f, margin_f, v_lines),
    #     False,
    #     output_yes,
    #     output_no,
    # )

    _, _, _, _, _, _, _ = parse(mass_f, lambdas_f, ignore_f, margin_f, v_lines)
    return
