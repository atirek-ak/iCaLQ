import sympy as sym
from sympy.utilities.lambdify import lambdify
from sympy.utilities.iterables import flatten
import scipy.optimize as optimize
import numpy as np


from utilities.branching_fraction import branching_fraction
from utilities.data_classes import NonInteractiveInputParameters, LeptoquarkParameters
from utilities.parse import get_lam_separate, parse_lam
from utilities.validate import lam_val_ok
from utilities.colour import prRed
from calculations.cross_section import get_cross_sections
from calculations.mass import get_closest_leptoquark_mass, make_leptoquark_mass_dict
from calculations.efficiencies import get_efficiencies
from calculations.chi_square import get_chi_square_symb, get_delta_chisq


def calculate(
    leptoquark_parameters: LeptoquarkParameters,
    non_interactive_input_parameters: NonInteractiveInputParameters | None = None,
):
    couplings_length = len(leptoquark_parameters.couplings)
    couplings_symbolic = [sym.Symbol(coupling) for coupling in leptoquark_parameters.couplings]
    electron_electron_cross_section, muon_muon_cross_section, tau_tau_cross_section = get_cross_sections(leptoquark_parameters)
    closest_leptoquark_mass = get_closest_leptoquark_mass(leptoquark_parameters.leptoquark_mass)
    eff_list = get_efficiencies(
        closest_leptoquark_mass, leptoquark_parameters, electron_electron_cross_section, muon_muon_cross_section, tau_tau_cross_section
    )
    mass_dict = make_leptoquark_mass_dict(lambdastring, couplings_length)
    all_lam, all_ls = get_lam_separate(couplings_symbolic)
    br_frac = branching_fraction(leptoquark_model, all_ls, all_lam, mass_dict, mass, width_constant)
    chisq_symb = get_chi_square_symb(
        mass, all_lam, cs_list, eff_list, br_frac, ignorePairSingle, margin, leptoquark_model, luminosity
    )
    # print("Lambdifying...")
    numpy_chisq = lambdify(flatten(couplings_symbolic), chisq_symb, modules="numpy")
    startLambda = 0.5
    startLambdas = np.array([startLambda for _ in range(couplings_length)])
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
        for randarr in np.random.rand(6, couplings_length)
    ]
    # minima_list_2 = [
    #     optimize.minimize(lambda x: numpy_chisq(*flatten(x)), randarr)
    #     for randarr in np.random.rand(3, couplings_length)
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
    print(*[f"\n{lambdastring[i]} : {opt_lambda_list[i]}" for i in range(couplings_length)])
    if interactive:
        print("Input query values in the following order: ", end="\t")
        for x in original_lambdastring:
            print(x, end="\t")
        while True:
            print("\n > ", end="")
            lam_val_f = input()
            if lam_val_f.lower() in ["done", "exit"]:
                return
            if not lam_val_ok(lam_val_f, couplings_length):
                prRed(f"[Query Error]: Please input {couplings_length} float input/s.")
                # prRed(f"[Query Error]: Query values for lambdas are either not {couplings_length} (number of lambdas) in count or not convertible to float.\n")
                print("Type 'done' or 'exit' to continue to calq prompt.")
                continue
            lam_vals, original_lam_vals = parse_lam(original_lambdastring, lam_val_f)
            delta_chisq, validity_list = get_delta_chisq(
                lam_vals,
                original_lam_vals,
                chisq_min,
                numpy_chisq,
                couplings_length,
                chi_sq_limits,
            )
            print(f"Delta Chi Square: {delta_chisq[0]}\nAllowed: {validity_list[0]}")
            if delta_chisq[0] < 0:
                print(
                    "A negative value should imply precision less than 1e-4 while calculating minima and can be considered equal to 0. Try initiating again to randomize minimization."
                )
    delta_chisq, validity_list = get_delta_chisq(
        lam_vals, original_lam_vals, chisq_min, numpy_chisq, couplings_length, chi_sq_limits
    )
    yes_list = [i for i in range(len(validity_list)) if validity_list[i] == "Yes"]
    no_list = [i for i in range(len(validity_list)) if validity_list[i] == "No"]
    print("\nYes List:\n")
    with open(output_yes, "w", encoding="utf8") as f:
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
    with open(output_no, "w", encoding="utf8") as f:
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
