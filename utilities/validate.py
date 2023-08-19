from utilities.colour import prRed


def ready_to_initiate(mass_f: str, lambdas_f: str, ignore_f: str, margin_f: str):
    """
    Checking if the inputs are in the correct format

    :param mass_f: Leptoquark mass
    :param lambdas_f: Lambda couplings
    :param ignore_f: Ignore single and pair production
    :param margin_f: Systematic error
    """
    # validate mass
    try:
        mass = int(mass_f)
        if mass < 1000 or mass > 3000:
            prRed(
                "[Mass Error]: Acceptable mass values in GeV: integers between 1000 and 3000.\n"
            )
            return False
    except ValueError:
        prRed(
            "[Mass Error]: Mass value should be an integer (between 1000 and 3000).\n"
        )
        return False

    # validate lambda couplings
    lambdas = lambdas_f.split()
    if not lambdas:
        return False
    for i in range(len(lambdas)):
        if lambdas[i][:2] != "LM":
            return False
        if lambdas[i][2] not in ["1", "2", "3"]:
            return False
        if lambdas[i][3] not in ["1", "2", "3"]:
            return False
        if lambdas[i][4] not in ["L", "R", "3"]:
            return False

    # validate Ignore single and pair production
    if ignore_f.lower() not in {"yes", "no", "n", "y"}:
        prRed("ignore_single_pair takes input either 'yes'/'y' or 'no'/'n'\n")
        return False

    # validate Systematic error
    try:
        margin = float(margin_f)
        if margin < 0 or margin > 1:
            prRed(
                "[Systematic-Error Error]: Acceptable systematic error values: float values between 0 and 1.\n"
            )
            return False
    except ValueError:
        prRed(
            "[Systematic-Error Error]: Systematic error value should be a float (between 0 and 1).\n"
        )
        return False
    return True


def lam_val_ok(lam_val_f, num_lam):
    """
    Check if queries are in correct form
    """
    lam_vals = lam_val_f.replace(",", " ").split()
    if len(lam_vals) != num_lam:
        return False
    try:
        for i in range(num_lam):
            a = float(lam_vals[i])
    except ValueError:
        return False
    return True
