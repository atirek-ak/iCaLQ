import math
import sys
import sympy as sym
import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
from sympy.utilities.iterables import flatten
from sympy.utilities.lambdify import lambdify
from sympy import Pow
import scipy.optimize as optimize

from classes.config import code_infra_config, file_paths_config, physics_config
from classes.leptoquark_parameters import LeptoquarkParameters
from classes.non_interactive_input_params import NonInteractiveInputParameters
from classes.custom_datatypes import InputMode, Generation, Tag, KFactor, DecayProcess
from classes.cross_section import CrossSections
from classes.efficiency import Efficiencies
from classes.branching_fraction import BranchingFraction
from classes.cache import PersistentDiskCache
from helper.validate import  validate_interactive_input_coupling_values
from helper.strings import convert_coupling_to_symbolic_coupling_format


class Calculator:
    def __init__(
            self,
            leptoquark_parameters: LeptoquarkParameters,
            input_mode: InputMode,
            non_interactive_input_parameters: NonInteractiveInputParameters = None,
            cross_sections: CrossSections = None,
            efficiencies: Efficiencies = None,
            symbolic_sorted_couplings: List[sym.Symbol] = None,
            branching_fraction: BranchingFraction = BranchingFraction(),
            chi_square: sym.Symbol = None,
            numpy_chi_square = None,
            chi_square_without_leptoquark: sym.Symbol = None,
            numpy_chi_square_without_leptoquark = None,
            minima: float = sys.float_info.max,
            minima_couplings: List[float] = None,
            cache: PersistentDiskCache = PersistentDiskCache(),
        ):
        self.leptoquark_parameters = leptoquark_parameters
        self.input_mode = input_mode
        self.non_interactive_input_parameters = non_interactive_input_parameters
        self.cross_sections = cross_sections
        self.efficiencies = efficiencies
        self.symbolic_sorted_couplings = symbolic_sorted_couplings
        self.branching_fraction = branching_fraction
        self.chi_square = chi_square
        self.numpy_chi_square = numpy_chi_square
        # this parameter is when branching fraction is set to zero
        self.chi_square_without_leptoquark = chi_square_without_leptoquark
        self.numpy_chi_square_without_leptoquark = numpy_chi_square_without_leptoquark
        self.minima = minima
        self.minima_couplings = minima_couplings
        self.cache = cache

    @staticmethod
    def get_standard_model_and_nd_dataframe(tag_value: str):
        dataframe = pd.read_csv(f"{file_paths_config.get('data_prefix')}/HEPdata/{tag_value}.csv", header=[0])
        return dataframe["Standard Model"].to_numpy(), dataframe["ND"].to_numpy()

    def calculate_single_coupling_contribution_tau_tau(self, coupling: str, symbolic_coupling: sym.Symbol):
        total_contribution: sym.Symbol = sym.Float(0)
        for tag in Tag:
            standard_model_contribution, nd_contribution = Calculator.get_standard_model_and_nd_dataframe(tag.value)
            # any decay process here would give the same number of bins. Using t_channel here
            number_of_bins = len(self.efficiencies.coupling_to_efficiency_map[DecayProcess.T_CHANNEL.value][coupling][tag.value])
            leptoquark_processes_contribution: List[Dict[str,sym.Symbol]] = [{} for _ in range(number_of_bins)]
            for bin_number in range(number_of_bins):
                denominator = nd_contribution[bin_number] + math.pow(self.leptoquark_parameters.systematic_error, 2) * math.pow(nd_contribution[bin_number],2)
                for decay_process in DecayProcess:
                    if decay_process in [DecayProcess.T_CHANNEL_DOUBLE_COUPLING, DecayProcess.T_CHANNEL_COMBINED]:
                        continue
                    if decay_process == DecayProcess.PAIR_PRODUCTION:
                        leptoquark_processes_contribution[bin_number][decay_process.value] = KFactor.dictionary[self.leptoquark_parameters.model][decay_process] \
                        * self.cross_sections.coupling_to_cross_section_map[coupling][decay_process.value] \
                        * self.efficiencies.coupling_to_efficiency_map[decay_process.value][coupling][tag.value][bin_number] \
                        * Pow(symbolic_coupling, 4) \
                        * Pow(self.branching_fraction.branching_fraction, 2) \
                        * self.leptoquark_parameters.luminosity * 1000
                    elif decay_process == DecayProcess.SINGLE_PRODUCTION:
                        leptoquark_processes_contribution[bin_number][decay_process.value] = KFactor.dictionary[self.leptoquark_parameters.model][decay_process] \
                                                                                             * self.cross_sections.coupling_to_cross_section_map[coupling][decay_process.value] \
                                                                                             * self.efficiencies.coupling_to_efficiency_map[decay_process.value][coupling][tag.value][bin_number] \
                                                                                             * Pow(symbolic_coupling, 2) \
                                                                                             * self.branching_fraction.branching_fraction \
                                                                                             * self.leptoquark_parameters.luminosity * 1000
                    elif decay_process == DecayProcess.INTERFERENCE:
                        leptoquark_processes_contribution[bin_number][decay_process.value] = KFactor.dictionary[self.leptoquark_parameters.model][decay_process] \
                                                                                             * self.cross_sections.coupling_to_cross_section_map[coupling][decay_process.value] \
                                                                                             * self.efficiencies.coupling_to_efficiency_map[decay_process.value][coupling][tag.value][bin_number] \
                                                                                             * Pow(symbolic_coupling, 2) \
                                                                                             * self.leptoquark_parameters.luminosity * 1000
                    elif decay_process == DecayProcess.T_CHANNEL:
                        leptoquark_processes_contribution[bin_number][decay_process.value] = KFactor.dictionary[self.leptoquark_parameters.model][decay_process] \
                                                                                             * self.cross_sections.coupling_to_cross_section_map[coupling][decay_process.value] \
                                                                                             * self.efficiencies.coupling_to_efficiency_map[decay_process.value][coupling][tag.value][bin_number] \
                                                                                             * Pow(symbolic_coupling, 4) \
                                                                                             * self.leptoquark_parameters.luminosity * 1000
                    elif decay_process == DecayProcess.PUREQCD and self.leptoquark_parameters.mass <= physics_config.get('pureqcd_contribution_mass_limit'):
                        leptoquark_processes_contribution[bin_number][decay_process.value] = KFactor.dictionary[self.leptoquark_parameters.model][decay_process] \
                                                                                             * self.cross_sections.coupling_to_cross_section_map[coupling][decay_process.value] \
                                                                                             * self.efficiencies.coupling_to_efficiency_map[decay_process.value][coupling][tag.value][bin_number] \
                                                                                             * Pow(self.branching_fraction.branching_fraction, 2) \
                                                                                             * self.leptoquark_parameters.luminosity * 1000
                if self.leptoquark_parameters.ignore_single_pair_processes:
                    total_contribution += sym.simplify(Pow((
                        + leptoquark_processes_contribution[bin_number][DecayProcess.T_CHANNEL.value]
                        + leptoquark_processes_contribution[bin_number][DecayProcess.INTERFERENCE.value]
                        + standard_model_contribution[bin_number]
                        - nd_contribution[bin_number]
                    ),2) / denominator)
                else:
                    total_contribution +=  sym.simplify(Pow((
                            leptoquark_processes_contribution[bin_number][DecayProcess.PUREQCD.value]
                            + leptoquark_processes_contribution[bin_number][DecayProcess.PAIR_PRODUCTION.value]
                            + leptoquark_processes_contribution[bin_number][DecayProcess.SINGLE_PRODUCTION.value]
                            + leptoquark_processes_contribution[bin_number][DecayProcess.T_CHANNEL.value]
                            + leptoquark_processes_contribution[bin_number][DecayProcess.INTERFERENCE.value]
                            + standard_model_contribution[bin_number]
                            - nd_contribution[bin_number]
                    ),2) / denominator)
        return sym.simplify(total_contribution)

    def calculate_single_coupling_contribution(self, coupling: str, symbolic_coupling: sym.Symbol):
        total_contribution: sym.Symbol = sym.Float(0)
        standard_model_contribution, nd_contribution = Calculator.get_standard_model_and_nd_dataframe("dielectron")
        if coupling[code_infra_config.get('coupling').get('lepton_index')] == str(Generation.MUON.value):
            standard_model_contribution, nd_contribution = Calculator.get_standard_model_and_nd_dataframe("dimuon")
        # any decay process here would give the same number of bins. Using t_channel here
        number_of_bins = len(self.efficiencies.coupling_to_efficiency_map[DecayProcess.T_CHANNEL.value][coupling])
        leptoquark_processes_contribution: List[Dict[str,sym.Symbol]] = [{} for _ in range(number_of_bins)]
        for bin_number in range(number_of_bins):
            denominator = nd_contribution[bin_number] + math.pow(self.leptoquark_parameters.systematic_error, 2) * math.pow(nd_contribution[bin_number],2)
            for decay_process in DecayProcess:
                if decay_process in [DecayProcess.T_CHANNEL_DOUBLE_COUPLING, DecayProcess.T_CHANNEL_COMBINED]:
                    continue
                if decay_process == DecayProcess.PAIR_PRODUCTION:
                    leptoquark_processes_contribution[bin_number][decay_process.value] = KFactor.dictionary[self.leptoquark_parameters.model][decay_process] \
                                                                                         * self.cross_sections.coupling_to_cross_section_map[coupling][decay_process.value] \
                                                                                         * self.efficiencies.coupling_to_efficiency_map[decay_process.value][coupling][bin_number] \
                                                                                         * Pow(symbolic_coupling, 4) \
                                                                                         * Pow(self.branching_fraction.branching_fraction, 2) \
                                                                                         * self.leptoquark_parameters.luminosity * 1000
                elif decay_process == DecayProcess.SINGLE_PRODUCTION:
                    leptoquark_processes_contribution[bin_number][decay_process.value] = KFactor.dictionary[self.leptoquark_parameters.model][decay_process] \
                                                                                         * self.cross_sections.coupling_to_cross_section_map[coupling][decay_process.value] \
                                                                                         * self.efficiencies.coupling_to_efficiency_map[decay_process.value][coupling][bin_number] \
                                                                                         * Pow(symbolic_coupling, 2) \
                                                                                         * self.branching_fraction.branching_fraction \
                                                                                         * self.leptoquark_parameters.luminosity * 1000
                elif decay_process == DecayProcess.INTERFERENCE:
                    leptoquark_processes_contribution[bin_number][decay_process.value] = KFactor.dictionary[self.leptoquark_parameters.model][decay_process] \
                                                                                         * self.cross_sections.coupling_to_cross_section_map[coupling][decay_process.value] \
                                                                                         * self.efficiencies.coupling_to_efficiency_map[decay_process.value][coupling][bin_number] \
                                                                                         * Pow(symbolic_coupling, 2) \
                                                                                         * self.leptoquark_parameters.luminosity * 1000
                elif decay_process == DecayProcess.T_CHANNEL:
                    leptoquark_processes_contribution[bin_number][decay_process.value] = KFactor.dictionary[self.leptoquark_parameters.model][decay_process] \
                                                                                         * self.cross_sections.coupling_to_cross_section_map[coupling][decay_process.value] \
                                                                                         * self.efficiencies.coupling_to_efficiency_map[decay_process.value][coupling][bin_number] \
                                                                                         * Pow(symbolic_coupling, 4) \
                                                                                         * self.leptoquark_parameters.luminosity * 1000
                elif decay_process == DecayProcess.PUREQCD and self.leptoquark_parameters.mass <= physics_config.get('pureqcd_contribution_mass_limit'):
                    leptoquark_processes_contribution[bin_number][decay_process.value] = KFactor.dictionary[self.leptoquark_parameters.model][decay_process] \
                                                                                         * self.cross_sections.coupling_to_cross_section_map[coupling][decay_process.value] \
                                                                                         * self.efficiencies.coupling_to_efficiency_map[decay_process.value][coupling][bin_number] \
                                                                                         * Pow(self.branching_fraction.branching_fraction, 2) \
                                                                                         * self.leptoquark_parameters.luminosity * 1000
            if self.leptoquark_parameters.ignore_single_pair_processes:
                total_contribution += sym.simplify(Pow((
                        + leptoquark_processes_contribution[bin_number][DecayProcess.T_CHANNEL.value]
                        + leptoquark_processes_contribution[bin_number][DecayProcess.INTERFERENCE.value]
                        + standard_model_contribution[bin_number]
                        - nd_contribution[bin_number]
                ),2) / denominator)
            else:
                total_contribution +=  sym.simplify(Pow((
                        leptoquark_processes_contribution[bin_number][DecayProcess.PUREQCD.value]
                        + leptoquark_processes_contribution[bin_number][DecayProcess.PAIR_PRODUCTION.value]
                        + leptoquark_processes_contribution[bin_number][DecayProcess.SINGLE_PRODUCTION.value]
                        + leptoquark_processes_contribution[bin_number][DecayProcess.T_CHANNEL.value]
                        + leptoquark_processes_contribution[bin_number][DecayProcess.INTERFERENCE.value]
                        + standard_model_contribution[bin_number]
                        - nd_contribution[bin_number]
                ),2) / denominator)
        return sym.simplify(total_contribution)

    def calculate_double_coupling_contribution_tau_tau(self, cross_terms_coupling: str, coupling_1_index: int, coupling_2_index: int):
        total_contribution: sym.Symbol = sym.Float(0)
        for tag in Tag:
            standard_model_contribution, nd_contribution = Calculator.get_standard_model_and_nd_dataframe(tag.value)
            # any decay process here would give the same number of bins. Using t_channel here
            number_of_bins = len(self.efficiencies.coupling_to_efficiency_map[DecayProcess.T_CHANNEL.value][self.leptoquark_parameters.sorted_couplings[coupling_1_index]][tag.value])
            leptoquark_processes_contribution: List[Dict[str,sym.Symbol]] = [{} for _ in range(number_of_bins)]
            for bin_number in range(number_of_bins):
                denominator = nd_contribution[bin_number] + math.pow(self.leptoquark_parameters.systematic_error, 2) * math.pow(nd_contribution[bin_number],2)
                for decay_process in DecayProcess:
                    if decay_process != DecayProcess.T_CHANNEL:
                        continue
                    leptoquark_processes_contribution[bin_number][decay_process.value] = KFactor.dictionary[self.leptoquark_parameters.model][decay_process] \
                                                                                         * self.cross_sections.coupling_to_cross_section_map[cross_terms_coupling][DecayProcess.T_CHANNEL_DOUBLE_COUPLING.value] \
                                                                                         * self.efficiencies.coupling_to_efficiency_map[decay_process.value][cross_terms_coupling][tag.value][bin_number] \
                                                                                         * Pow(self.symbolic_sorted_couplings[coupling_1_index], 2) \
                                                                                         * Pow(self.symbolic_sorted_couplings[coupling_2_index], 2) \
                                                                                         * self.leptoquark_parameters.luminosity * 1000

                total_contribution +=  sym.simplify(Pow((
                        + leptoquark_processes_contribution[bin_number][DecayProcess.T_CHANNEL.value]
                        + standard_model_contribution[bin_number]
                        - nd_contribution[bin_number]
                ),2) / denominator)
        return sym.simplify(total_contribution)

    def calculate_double_coupling_contribution(self, cross_terms_coupling: str, coupling_1_index: int, coupling_2_index: int):
        total_contribution: sym.Symbol = sym.Float(0)
        standard_model_contribution, nd_contribution = Calculator.get_standard_model_and_nd_dataframe("dielectron")
        if self.leptoquark_parameters.sorted_couplings[coupling_1_index][code_infra_config.get('coupling').get('lepton_index')] == str(Generation.MUON.value):
            standard_model_contribution, nd_contribution = Calculator.get_standard_model_and_nd_dataframe("dimuon")
        # any decay process here would give the same number of bins. Using t_channel here
        number_of_bins = len(self.efficiencies.coupling_to_efficiency_map[DecayProcess.T_CHANNEL.value][self.leptoquark_parameters.sorted_couplings[coupling_1_index]])
        leptoquark_processes_contribution: List[Dict[str,sym.Symbol]] = [{} for _ in range(number_of_bins)]
        for bin_number in range(number_of_bins):
            denominator = nd_contribution[bin_number] + math.pow(self.leptoquark_parameters.systematic_error, 2) * math.pow(nd_contribution[bin_number],2)
            for decay_process in DecayProcess:
                if decay_process != DecayProcess.T_CHANNEL:
                    continue
                leptoquark_processes_contribution[bin_number][decay_process.value] = KFactor.dictionary[self.leptoquark_parameters.model][decay_process] \
                                                                                     * self.cross_sections.coupling_to_cross_section_map[cross_terms_coupling][DecayProcess.T_CHANNEL_DOUBLE_COUPLING.value] \
                                                                                     * self.efficiencies.coupling_to_efficiency_map[decay_process.value][cross_terms_coupling][bin_number] \
                                                                                     * Pow(self.symbolic_sorted_couplings[coupling_1_index], 2) \
                                                                                     * Pow(self.symbolic_sorted_couplings[coupling_2_index], 2) \
                                                                                     * self.leptoquark_parameters.luminosity * 1000

            total_contribution +=  sym.simplify(Pow((
                    + leptoquark_processes_contribution[bin_number][DecayProcess.T_CHANNEL.value]
                    + standard_model_contribution[bin_number]
                    - nd_contribution[bin_number]
            ),2) / denominator)
        return sym.simplify(total_contribution)

    def calculate_chi_square(self, print_output: bool = False) -> sym.Symbol:
        chi_square: sym.Symbol = sym.Float(0)
        # single coupling chi-square
        for sorted_coupling, sorted_coupling_symbolic in zip(self.leptoquark_parameters.sorted_couplings, self.symbolic_sorted_couplings):
            if sorted_coupling[code_infra_config.get('coupling').get('lepton_index')] == str(Generation.TAU.value):
                chi_square += self.calculate_single_coupling_contribution_tau_tau(sorted_coupling, sorted_coupling_symbolic)
            else:
                chi_square += self.calculate_single_coupling_contribution(sorted_coupling, sorted_coupling_symbolic)
            if print_output:
                print(f"{sorted_coupling} contributions calculated!!")


        # cross terms chi-square
        for i in range(len(self.leptoquark_parameters.sorted_couplings)):
            for j in range(i + 1, len(self.leptoquark_parameters.sorted_couplings)):
                if (
                        self.leptoquark_parameters.sorted_couplings[i][code_infra_config.get('coupling').get('lepton_index')]
                        == self.leptoquark_parameters.sorted_couplings[j][code_infra_config.get('coupling').get('lepton_index')]
                ):
                    cross_terms_coupling = f"{self.leptoquark_parameters.sorted_couplings[i]}_{self.leptoquark_parameters.sorted_couplings[j]}"
                    if self.leptoquark_parameters.sorted_couplings[i][code_infra_config.get('coupling').get('lepton_index')] == str(Generation.TAU.value):
                        chi_square += self.calculate_double_coupling_contribution_tau_tau(cross_terms_coupling, i, j)
                    else:
                        chi_square += self.calculate_double_coupling_contribution(cross_terms_coupling, i, j)
                    if print_output:
                        print(f"{cross_terms_coupling} contributions calculated!!")

        return chi_square

    def convert_chi_square_to_numpy(self, chi_square: sym.Symbol):
        return lambdify(
            flatten(self.symbolic_sorted_couplings), chi_square, modules="numpy"
        )

    def set_branching_fraction_to_zero_and_return_original_value(self) -> sym.Symbol:
        original_branching_fraction = self.branching_fraction.branching_fraction
        self.branching_fraction.branching_fraction = sym.Float(0.0)
        return original_branching_fraction

    def unset_branching_fraction_from_zero(self, original_branching_fraction: sym.Symbol):
        self.branching_fraction.branching_fraction = original_branching_fraction


    def set_chi_square_without_leptoquark(self):
        if len(self.leptoquark_parameters.sorted_couplings) > 1:
            original_branching_fraction = self.set_branching_fraction_to_zero_and_return_original_value()
            self.chi_square_without_leptoquark = self.calculate_chi_square(False)
            self.unset_branching_fraction_from_zero(original_branching_fraction)
            self.set_chi_square_without_leptoquark_in_cache()
            self.numpy_chi_square_without_leptoquark = self.convert_chi_square_to_numpy(self.chi_square_without_leptoquark)

    def compare_minima_without_leptoquark(self):
        if len(self.leptoquark_parameters.sorted_couplings) > 1:
            all_zeros_couplings = [
                0.0 for _ in self.leptoquark_parameters.sorted_couplings
            ]
            zero_minima = self.numpy_chi_square_without_leptoquark(
                *flatten(all_zeros_couplings)
            )
            if zero_minima < self.minima:
                self.minima = zero_minima
                self.minima_couplings = all_zeros_couplings

    def find_minima(self):
        print("Finding chi-square minima ...")
        minima_points = [
            optimize.minimize(
                lambda x: self.numpy_chi_square(*flatten(x)),
                random_values_list,
                method="Nelder-Mead",
                options={"fatol": 0.0001},
            ) for random_values_list in 5 * np.random.rand(
                7, len(self.leptoquark_parameters.sorted_couplings)
            )
        ]
        for minima_point in minima_points:
            if minima_point.fun < self.minima:
                self.minima = minima_point.fun
                self.minima_couplings = minima_point.x

        self.compare_minima_without_leptoquark()
        self.set_chi_square_minima_in_cache()
        self.set_chi_square_minima_coupling_values_in_cache()
        print(f"Chi-square minima: {self.minima}")
        print("Minimum chi-square at values:", end="")
        print(
            *[
                f"\n{self.leptoquark_parameters.sorted_couplings[i]} : {self.minima_couplings[i]}"
                for i in range(len(self.leptoquark_parameters.sorted_couplings))
            ]
        )

    def get_delta_chi_square(
            self,
            coupling_values_list: List[List[float]],
    ) -> Tuple[List[Tuple[List[float], float]], List[Tuple[List[float], float]]]:
        within_limits: List[Tuple[List[float], float]] = []
        outside_limits: List[Tuple[List[float], float]] = []
        for coupling_values in coupling_values_list:
            try:
                # substitute values in branching fraction to check for zero division error for multiple couplings
                # for single couplings the branching_fraction will be a float
                if len(coupling_values) > 1:
                    flat_values = flatten(coupling_values)
                    _ = self.branching_fraction.branching_fraction.subs(
                        dict(zip(flat_values[::2], flat_values[1::2]))
                    )
                chi_square_value = self.numpy_chi_square(
                    *flatten(coupling_values))
            except ZeroDivisionError:
                chi_square_value = self.numpy_chi_square_without_leptoquark(
                    *flatten(coupling_values)
                )
            delta_chi_square= chi_square_value - self.minima
            if delta_chi_square <= physics_config.get('chi_square_limits')[str(self.leptoquark_parameters.significance)][len(self.leptoquark_parameters.sorted_couplings)-1]:
                within_limits.append((coupling_values, delta_chi_square))
            else:
                outside_limits.append((coupling_values, delta_chi_square))
        return within_limits, outside_limits

    def interactive_input_coupling_values(self):
        if self.input_mode != InputMode.INTERACTIVE:
            return
        print("Input coupling values in the following order: ", end="\t")
        for coupling in self.leptoquark_parameters.sorted_couplings:
            print(coupling, end="\t")
            while True:
                print("\n > ", end="")
                coupling_values_input_interactive = input()
                if coupling_values_input_interactive.lower() in [
                    "done",
                    "d",
                    "q",
                    "quit",
                    "exit",
                ]:
                    return
                if not validate_interactive_input_coupling_values(
                        coupling_values_input_interactive,
                        len(self.leptoquark_parameters.sorted_couplings),
                ):
                    print("Type 'done' or 'exit' to continue to calq prompt.")
                    continue
                coupling_values_interactive = [
                    float(value.strip())
                    for value in coupling_values_input_interactive.strip().split(' ')
                ]
                within_limits_list, outside_limits_list = self.get_delta_chi_square(
                    [coupling_values_interactive],
                )
                if len(within_limits_list) > 0:
                    print(
                        f"Delta chi-square: {within_limits_list[0][1]}\nAllowed: Yes"
                    )
                if len(outside_limits_list) > 0:
                    print(
                        f"Delta chi-square: {outside_limits_list[0][1]}\nAllowed: No"
                    )
                if len(outside_limits_list) > 0 > outside_limits_list[0][1]:
                    print(
                        "A negative value should imply precision less than 1e-4 while calculating minima and can be considered equal to 0. Try initiating again to randomize minimization."
                    )

    def non_interactive_output_validity_lists(self):
        if self.input_mode != InputMode.NONINTERACTIVE:
            return
        within_limits_list, outside_limits_list = self.get_delta_chi_square(
            self.leptoquark_parameters.sorted_couplings_values
        )
        if len(within_limits_list) > 0:
            print("\nYes List:")
            with open(
                    self.non_interactive_input_parameters.output_yes_path, "w", encoding="utf8"
            ) as yes_file:
                for coupling in self.leptoquark_parameters.sorted_couplings:
                    print(coupling, end="\t")
                    print(f'"{coupling}"', end=",", file=yes_file)
                print("Delta chi-square")
                print("Delta chi-square", file=yes_file)
                for within_limits_element in within_limits_list:
                    print('\t'.join(map(str, within_limits_element[0])), end="\t")
                    print(','.join(map(str, within_limits_element[0])), end=",", file=yes_file)
                    print(within_limits_element[1])
                    print(within_limits_element[1], file=yes_file)

        if len(outside_limits_list) > 0:
            print("\nNo List:")
            with open(
                    self.non_interactive_input_parameters.output_no_path, "w", encoding="utf8"
            ) as no_file:
                for coupling in self.leptoquark_parameters.sorted_couplings:
                    print(coupling, end="\t")
                    print(f'"{coupling}"', end=",", file=no_file)
                print("Delta chi-square")
                print("Delta chi-square", file=no_file)
                for outside_limits_element in outside_limits_list:
                    print('\t'.join(map(str, outside_limits_element[0])), end="\t")
                    print(','.join(map(str, outside_limits_element[0])), end=",", file=no_file)
                    print(outside_limits_element[1])
                    print(outside_limits_element[1], file=no_file)

        with open(
                self.non_interactive_input_parameters.output_common_path, "w", encoding="utf8"
        ) as common_file:
            for coupling in self.leptoquark_parameters.sorted_couplings:
                print(f'"{coupling}"', end=",", file=common_file)
            print("Delta chi-square", file=common_file)
            for within_limits_element in outside_limits_list:
                print(','.join(map(str, within_limits_element[0])), end=",", file=common_file)
                print(within_limits_element[1], file=common_file)
            for outside_limits_element in outside_limits_list:
                print(','.join(map(str, outside_limits_element[0])), end=",", file=common_file)
                print(outside_limits_element[1], file=common_file)

    def check_and_assign_cache(self) -> bool:
        chi_square_key = PersistentDiskCache.construct_chi_square_expression_cache_key(self.leptoquark_parameters)
        chi_square_value = self.cache.get_symbolic_expression(chi_square_key)
        if not chi_square_value:
            return False
        self.chi_square = chi_square_value
        self.numpy_chi_square = self.convert_chi_square_to_numpy(self.chi_square)

        chi_square_without_leptoquark_key = PersistentDiskCache.construct_chi_square_without_leptoquark_expression_cache_key(self.leptoquark_parameters)
        chi_square_without_leptoquark_value = self.cache.get_symbolic_expression(chi_square_without_leptoquark_key)
        if not chi_square_without_leptoquark_value:
            return False
        self.chi_square_without_leptoquark = chi_square_without_leptoquark_value
        self.numpy_chi_square_without_leptoquark = self.convert_chi_square_to_numpy(self.chi_square_without_leptoquark)

        minima_key = PersistentDiskCache.construct_chi_square_minima_cache_key(self.leptoquark_parameters)
        minima_value = self.cache.get_float_value(minima_key)
        if not minima_value:
            return False
        self.minima = minima_value

        minima_couplings_key = PersistentDiskCache.construct_chi_square_minima_couplings_cache_key(self.leptoquark_parameters)
        minima_couplings_value = self.cache.get_list_of_floats_value(minima_couplings_key)
        if not minima_couplings_value:
            return False
        self.minima_couplings = minima_couplings_value

        return True

    def set_chi_square_in_cache(self):
        chi_square_key = PersistentDiskCache.construct_chi_square_expression_cache_key(self.leptoquark_parameters)
        self.cache.set(chi_square_key, str(self.chi_square))

    def set_chi_square_without_leptoquark_in_cache(self):
        chi_square_without_leptoquark_key = PersistentDiskCache.construct_chi_square_without_leptoquark_expression_cache_key(self.leptoquark_parameters)
        self.cache.set(chi_square_without_leptoquark_key, str(self.chi_square))

    def set_chi_square_minima_in_cache(self):
        minima_key = PersistentDiskCache.construct_chi_square_minima_cache_key(self.leptoquark_parameters)
        self.cache.set(minima_key, str(self.minima))

    def set_chi_square_minima_coupling_values_in_cache(self):
        minima_couplings_key = PersistentDiskCache.construct_chi_square_minima_couplings_cache_key(self.leptoquark_parameters)
        self.cache.set(minima_couplings_key, ' '.join([str(element) for element in self.minima_couplings]))

    def calculate(self):
        # create symbolic couplings
        self.symbolic_sorted_couplings = [
            sym.Symbol(convert_coupling_to_symbolic_coupling_format(coupling)) for coupling in self.leptoquark_parameters.sorted_couplings
        ]

        # if values are present in cache, then we skip calculations & assign class values there
        if self.check_and_assign_cache():
            print("Chi-square values fetched from cache!!")
            self.post_chi_square_calculation()
            return

        # fill cross-sections
        self.cross_sections = CrossSections()
        self.cross_sections.fill_all_couplings_to_cross_section_map(self.leptoquark_parameters)

        # fill efficiencies
        self.efficiencies = Efficiencies()
        self.efficiencies.fill_all_couplings_to_efficiency_map(self.leptoquark_parameters, self.cross_sections)

        # fill branching fraction
        self.branching_fraction = BranchingFraction()
        self.branching_fraction.make_mass_dictionary(self.leptoquark_parameters.sorted_couplings)
        self.branching_fraction.get_branching_fraction_symbolic(self.leptoquark_parameters, self.symbolic_sorted_couplings)

        # start chi-square calculation
        self.chi_square = self.calculate_chi_square(True)
        self.set_chi_square_in_cache()
        self.numpy_chi_square = self.convert_chi_square_to_numpy(self.chi_square)
        self.set_chi_square_without_leptoquark()
        self.find_minima()

        self.post_chi_square_calculation()


    def post_chi_square_calculation(self):
        self.interactive_input_coupling_values()
        self.non_interactive_output_validity_lists()





