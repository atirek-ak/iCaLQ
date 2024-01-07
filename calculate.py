import sympy as sym
from sympy.utilities.lambdify import lambdify
from sympy.utilities.iterables import flatten
import scipy.optimize as optimize
import numpy as np


from utilities.branching_fraction import branching_fraction
from utilities.parse import get_lam_separate, parse_lam
from utilities.validate import lam_val_ok
from utilities.colour import prRed
from calculations.cross_section import get_cs
from calculations.mass import get_closest_mass, make_mass_dict
from calculations.efficiencies import get_efficiencies
from calculations.chi_square import get_chi_square_symb, get_delta_chisq


def home(
    mass,
    lambdastring,
    original_lambdastring,
    ignorePairSingle,
    lam_vals,
    original_lam_vals,
    margin,
    leptoquark_model,
    interactive,
    chi_sq_limits,
    output_yes="icalq_yes.csv",
    output_no="icalq_no.csv",
):
    num_lam = len(lambdastring)
    lam = sym.symbols(lambdastring)
    cs_list = get_cs(mass, lambdastring, num_lam, leptoquark_model)
    closest_mass = get_closest_mass(mass)
    eff_list = get_efficiencies(
        closest_mass, lambdastring, num_lam, cs_list, leptoquark_model
    )
    mass_dict = make_mass_dict(lambdastring, num_lam)
    all_lam, all_ls = get_lam_separate(lam)
    br_frac = branching_fraction(all_ls, all_lam, mass_dict, mass, 0)
    chisq_symb = get_chi_square_symb(
        mass, all_lam, cs_list, eff_list, br_frac, ignorePairSingle, margin
    )
    # print("Lambdifying...")
    numpy_chisq = lambdify(flatten(lam), chisq_symb, modules="numpy")
    startLambda = 0.5
    startLambdas = np.array([startLambda for x in range(num_lam)])
    print("Minimizing...")
    minima = optimize.minimize(
        lambda x: numpy_chisq(*flatten(x)),
        startLambdas,
        method="Nelder-Mead",
        options={"fatol": 0.0001},
    )
    minima_list_1 = [
        optimize.minimize(
            lambda x: numpy_chisq(*flatten(x)),
            randarr,
            method="Nelder-Mead",
            options={"fatol": 0.0001},
        )
        for randarr in np.random.rand(6, num_lam)
    ]
    # minima_list_2 = [
    #     optimize.minimize(lambda x: numpy_chisq(*flatten(x)), randarr)
    #     for randarr in np.random.rand(3, num_lam)
    # ]
    # for m in minima_list_1 + minima_list_2:
    for m in minima_list_1:
        if m.fun < minima.fun:
            print(f"New Minimum Found: {m.fun}")
            print(f"Lambda: {m.x}")
            minima = m
    chisq_min = minima.fun
    opt_lambda_list = minima.x
    print("Minimum Chi Square at values:", end="")
    print(*[f"\n{lambdastring[i]} : {opt_lambda_list[i]}" for i in range(num_lam)])
    if interactive:
        print("Input query values in the following order: ", end="\t")
        for x in original_lambdastring:
            print(x, end="\t")
        while True:
            print("\n > ", end="")
            lam_val_f = input()
            if lam_val_f == "done":
                return
            if not lam_val_ok(lam_val_f, num_lam):
                prRed(f"[Query Error]: Please input {num_lam} float input/s.\n")
                # prRed(f"[Query Error]: Query values for lambdas are either not {num_lam} (number of lambdas) in count or not convertible to float.\n")
                print("Type 'done' to continue to icalq prompt.")
                continue
            lam_vals, original_lam_vals = parse_lam(original_lambdastring, lam_val_f)
            delta_chisq, validity_list = get_delta_chisq(
                lam_vals,
                original_lam_vals,
                chisq_min,
                numpy_chisq,
                num_lam,
                chi_sq_limits,
            )
            print(f"Delta Chi Square: {delta_chisq[0]}\nAllowed: {validity_list[0]}")
            if delta_chisq[0] < 0:
                print(
                    "A negative value should imply precision less than 1e-4 while calculating minima and can be considered equal to 0. Try initiating again to randomize minimization."
                )
    delta_chisq, validity_list = get_delta_chisq(
        lam_vals, original_lam_vals, chisq_min, numpy_chisq, num_lam, chi_sq_limits
    )
    yes_list = [i for i in range(len(validity_list)) if validity_list[i] == "Yes"]
    no_list = [i for i in range(len(validity_list)) if validity_list[i] == "No"]
    print("\nYes List:\n")
    with open(output_yes, "w") as f:
        for x in original_lambdastring:
            print(x, end="\t\t")
            print(x, end=",", file=f)
        print("Delta_chisquare")
        print("Delta_chisquare", file=f)
        for i in yes_list:
            for x in original_lam_vals[i]:
                print(x, end="\t\t")
                print(x, end=",", file=f)
            print(delta_chisq[i])
            print(delta_chisq[i], file=f)
    print("\nNo List:\n")
    with open(output_no, "w") as f:
        for x in original_lambdastring:
            print(x, end="\t\t")
            print(x, end=",", file=f)
        print("Delta_chisquare")
        print("Delta_chisquare", file=f)
        for i in no_list:
            for x in original_lam_vals[i]:
                print(x, end="\t\t")
                print(x, end=",", file=f)
            print(delta_chisq[i])
            print(delta_chisq[i], file=f)
    print(f"Output files {output_yes} and {output_no} written")
