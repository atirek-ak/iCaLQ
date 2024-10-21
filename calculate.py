import sympy as sym
from sympy.utilities.lambdify import lambdify
from sympy.utilities.iterables import flatten
import scipy.optimize as optimize
import numpy as np

from utilities.constants import InputMode
from utilities.branching_fraction import getBranchingFraction
from utilities.data_classes import LeptoquarkParameters, NonInteractiveInputParameters
from utilities.validate import validateInteractiveInputCouplingValues
from calculations.cross_section import getCrossSections
from calculations.mass import makeLeptoquarkMassDictionary
from calculations.efficiencies import getEfficiencies
from calculations.chi_square import getChiSquareSymbolic
from calculations.helper import getDeltaChiSquare


def calculate(
    leptoquark_parameters: LeptoquarkParameters,
    input_mode: InputMode,
    non_interactive_input_parameters: NonInteractiveInputParameters = LeptoquarkParameters()
):
    """
    main function for chi-square testing and asociated calculations 
    """
    # fetch cross-section & efficiency after interpolation
    coupling_to_process_cross_section_map = getCrossSections(leptoquark_parameters)
    coupling_to_process_efficiencies_map = getEfficiencies(leptoquark_parameters, coupling_to_process_cross_section_map)

    # make symbolic couplings 
    symbolic_couplings = [sym.Symbol(coupling) for coupling in leptoquark_parameters.sorted_couplings]

    # get branching fraction
    mass_dictionary = makeLeptoquarkMassDictionary(leptoquark_parameters.sorted_couplings)
    branching_fraction = getBranchingFraction(leptoquark_parameters, symbolic_couplings, mass_dictionary)

    # calcualte chi-square
    chi_square_symbolic = getChiSquareSymbolic(leptoquark_parameters, branching_fraction, coupling_to_process_cross_section_map, coupling_to_process_efficiencies_map, symbolic_couplings)
    # convert chi-square symbolic to numpy as it has faster execution
    numpy_chi_square_symbolic = lambdify(flatten(symbolic_couplings), chi_square_symbolic, modules="numpy")

    # find minimum lambda
    # start coupling value is the initial value we use for minimization
    print("Finding chi-square minima...")
    # we create 5 array with coupling values between 0 to 1 as starting points for minimization
    minima_values_list = [
        optimize.minimize(
            lambda x: numpy_chi_square_symbolic(*flatten(x)),
            random_values_list,
            method="Nelder-Mead",
            options={"fatol": 0.0001},
        )
        for random_values_list in np.random.rand(5, len(leptoquark_parameters.sorted_couplings))
    ]
    # we create 5 array with coupling values between 0 to 5 as starting points for minimization
    minima_values_list.extend([
        optimize.minimize(
            lambda x: numpy_chi_square_symbolic(*flatten(x)),
            random_values_list,
            method="Nelder-Mead",
            options={"fatol": 0.0001},
        )
        for random_values_list in (np.random.rand(5, len(leptoquark_parameters.sorted_couplings)) * 5)
    ])
    minima = minima_values_list[0]
    for minima_value in minima_values_list:
        # comparing function values
        if minima_value.fun < minima.fun:
            minima = minima_value
    chi_square_minima = minima.fun
    chi_square_minima_couplings = minima.x
    print("Minimum Chi Square at values:", end="")
    print(*[f"\n{leptoquark_parameters.sorted_couplings[i]} : {chi_square_minima_couplings[i]}" for i in range(len(leptoquark_parameters.sorted_couplings))])

    # in case of interactive mode, input coupling values
    if input_mode == InputMode.INTERACTIVE:
        print("Input cooupling values in the following order: ", end="\t")
        for coupling in leptoquark_parameters.sorted_couplings:
            print(coupling, end="\t")
        while True:
            print("\n > ", end="")
            coupling_values_input_interactive = input()
            if coupling_values_input_interactive.lower() in ["done", "exit"]:
                return
            if not validateInteractiveInputCouplingValues(coupling_values_input_interactive, len(leptoquark_parameters.sorted_couplings)):
                print("Type 'done' or 'exit' to continue to calq prompt.")
                continue
            coupling_values_interactive = [float(value) for value in coupling_values_input_interactive.strip().split()]
            delta_chi_square, validity_list = getDeltaChiSquare(leptoquark_parameters, [coupling_values_interactive], chi_square_minima, numpy_chi_square_symbolic)
            print(f"Delta Chi Square: {delta_chi_square[0]}\nAllowed: {validity_list[0]}")
            if delta_chi_square[0] < 0:
                print("A negative value should imply precision less than 1e-4 while calculating minima and can be considered equal to 0. Try initiating again to randomize minimization.")

    # Get delta chi-square for non-interactive mode
    delta_chi_square, validity_list = getDeltaChiSquare(leptoquark_parameters, leptoquark_parameters.sorted_couplings_values, chi_square_minima, numpy_chi_square_symbolic)
    yes_list = [i for i in range(len(validity_list)) if validity_list[i] == "Yes"]
    no_list = [i for i in range(len(validity_list)) if validity_list[i] == "No"]

    # printing & outputting yes values
    print("\nYes List:")
    with open(f"values/{leptoquark_parameters.sorted_couplings[0]}.csv", 'a') as temp_file:
        for index in range(len(delta_chi_square)):
            if index in yes_list:
                # for x in original_lam_vals[i]:
                print(f"{leptoquark_parameters.leptoquark_mass}\t{leptoquark_parameters.sorted_couplings_values[index]}\t{chi_square_minima}\t{chi_square_minima+delta_chi_square[index]}\t1", file=temp_file)
            else:
                print(f"{leptoquark_parameters.leptoquark_mass}\t{leptoquark_parameters.sorted_couplings_values[index]}\t{chi_square_minima}\t{chi_square_minima+delta_chi_square[index]}\t2", file=temp_file)
    with open(non_interactive_input_parameters.output_yes_path, "w", encoding="utf8") as yes_file:
        for coupling in leptoquark_parameters.sorted_couplings:
            print(coupling, end="\t")
            print(coupling, end=",", file=yes_file)
        print("Delta_chisquare")
        print("Delta_chisquare", file=yes_file)
        for i in yes_list:
            for value in leptoquark_parameters.sorted_couplings_values[i]:
                print(value, end="\t")
                print(value, end=",", file=yes_file)
            print(delta_chi_square[i])
            print(delta_chi_square[i], file=yes_file)

    # printing & outputting no values
    print("\nNo List:")
    with open(non_interactive_input_parameters.output_no_path, "w", encoding="utf8") as no_file:
        for coupling in leptoquark_parameters.sorted_couplings:
            print(coupling, end="\t")
            print(coupling, end=",", file=no_file)
        print("Delta_chisquare")
        print("Delta_chisquare", file=no_file)
        for i in no_list:
            for value in leptoquark_parameters.sorted_couplings_values[i]:
                print(value, end="\t")
                print(value, end=",", file=no_file)
            print(delta_chi_square[i])
            print(delta_chi_square[i], file=no_file)
    print(f"Output files {non_interactive_input_parameters.output_yes_path} and {non_interactive_input_parameters.output_no_path} written")
