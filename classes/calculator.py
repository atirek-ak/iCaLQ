import math
import sympy as sym
import pandas as pd
from typing import List, Dict

from sympy.strategies.core import switch

from classes.config import code_infra_config, file_paths_config, physics_config
from classes.leptoquark_parameters import LeptoquarkParameters
from classes.non_interactive_input_params import NonInteractiveInputParameters
from classes.custom_datatypes import InputMode, Generation, Tag, KFactor, DecayProcess
from classes.cross_section import CrossSections
from classes.efficiency import Efficiencies
from classes.branching_fraction import BranchingFraction


class Calculator:
    def __init__(
            self,
            leptoquark_parameters: LeptoquarkParameters,
            input_mode: InputMode,
            non_interactive_input_parameters: NonInteractiveInputParameters = None,
            cross_sections: CrossSections = None,
            efficiencies: Efficiencies = None,
            symbolic_sorted_couplings: List[sym.Symbol] = None,
            branching_fraction: BranchingFraction = None,
            chi_square: sym.Symbol = None
        ):
        self.leptoquark_parameters = leptoquark_parameters
        self.input_mode = input_mode
        self.non_interactive_input_parameters = non_interactive_input_parameters
        self.cross_sections = cross_sections
        self.efficiencies = efficiencies
        self.symbolic_sorted_couplings = symbolic_sorted_couplings
        self.branching_fraction = branching_fraction
        self.chi_square = chi_square

    def initiate(self):
        # fill cross-sections
        self.cross_sections = CrossSections()
        self.cross_sections.fill_all_couplings_to_cross_section_map(self.leptoquark_parameters)

        # fill efficiencies
        self.efficiencies = Efficiencies()
        self.efficiencies.fill_all_couplings_to_efficiency_map(self.leptoquark_parameters, self.cross_sections)

        # create symbolic couplings
        self.symbolic_sorted_couplings = [
            sym.Symbol(coupling) for coupling in self.leptoquark_parameters.sorted_couplings
        ]

        # fill branching fraction
        self.branching_fraction = BranchingFraction()
        self.branching_fraction.make_mass_dictionary(self.leptoquark_parameters.sorted_couplings)
        self.branching_fraction.get_branching_fraction_symbolic(self.leptoquark_parameters, self.symbolic_sorted_couplings)

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
            leptoquark_processes_contribution: List[Dict[str,sym.Symbol]] = [{} for bin_number in range(number_of_bins)]
            for bin_number in range(number_of_bins):
                denominator = nd_contribution[bin_number] + math.pow(self.leptoquark_parameters.systematic_error, 2) * math.pow(nd_contribution[bin_number],2)
                for decay_process in DecayProcess:
                    if decay_process in [DecayProcess.T_CHANNEL_DOUBLE_COUPLING, DecayProcess.T_CHANNEL_COMBINED]:
                        continue
                    if decay_process == DecayProcess.PAIR_PRODUCTION:
                        leptoquark_processes_contribution[bin_number][decay_process.value] = KFactor.dictionary[self.leptoquark_parameters.model][decay_process.value] \
                        * self.cross_sections.coupling_to_cross_section_map[coupling][decay_process.value] \
                        * self.efficiencies.coupling_to_efficiency_map[decay_process.value][coupling][tag.value] \
                        * math.pow(symbolic_coupling, 4) \
                        * math.pow(self.branching_fraction.branching_fraction, 2) \
                        * self.leptoquark_parameters.luminosity * 1000
                    elif decay_process == DecayProcess.SINGLE_PRODUCTION:
                        leptoquark_processes_contribution[bin_number][decay_process.value] = KFactor.dictionary[self.leptoquark_parameters.model][decay_process.value] \
                                                                                             * self.cross_sections.coupling_to_cross_section_map[coupling][decay_process.value] \
                                                                                             * self.efficiencies.coupling_to_efficiency_map[decay_process.value][coupling][tag.value] \
                                                                                             * math.pow(symbolic_coupling, 2) \
                                                                                             * self.branching_fraction.branching_fraction \
                                                                                             * self.leptoquark_parameters.luminosity * 1000
                    elif decay_process == DecayProcess.INTERFERENCE:
                        leptoquark_processes_contribution[bin_number][decay_process.value] = KFactor.dictionary[self.leptoquark_parameters.model][decay_process.value] \
                                                                                             * self.cross_sections.coupling_to_cross_section_map[coupling][decay_process.value] \
                                                                                             * self.efficiencies.coupling_to_efficiency_map[decay_process.value][coupling][tag.value] \
                                                                                             * math.pow(symbolic_coupling, 2) \
                                                                                             * self.leptoquark_parameters.luminosity * 1000
                    elif decay_process == DecayProcess.T_CHANNEL:
                        leptoquark_processes_contribution[bin_number][decay_process.value] = KFactor.dictionary[self.leptoquark_parameters.model][decay_process.value] \
                                                                                             * self.cross_sections.coupling_to_cross_section_map[coupling][decay_process.value] \
                                                                                             * self.efficiencies.coupling_to_efficiency_map[decay_process.value][coupling][tag.value] \
                                                                                             * math.pow(symbolic_coupling, 4) \
                                                                                             * self.leptoquark_parameters.luminosity * 1000
                    elif decay_process == DecayProcess.PUREQCD and self.leptoquark_parameters.mass <= physics_config.get('pureqcd_contribution_mass_limit'):
                        leptoquark_processes_contribution[bin_number][decay_process.value] = KFactor.dictionary[self.leptoquark_parameters.model][decay_process.value] \
                                                                                             * self.cross_sections.coupling_to_cross_section_map[coupling][decay_process.value] \
                                                                                             * self.efficiencies.coupling_to_efficiency_map[decay_process.value][coupling][tag.value] \
                                                                                             * math.pow(self.branching_fraction.branching_fraction, 2) \
                                                                                             * self.leptoquark_parameters.luminosity * 1000
                if self.leptoquark_parameters.ignore_single_pair_processes:
                    total_contribution += sym.simplify(math.pow((
                        + leptoquark_processes_contribution[bin_number][DecayProcess.T_CHANNEL.value]
                        + leptoquark_processes_contribution[bin_number][DecayProcess.INTERFERENCE.value]
                        + standard_model_contribution[bin_number]
                        - nd_contribution[bin_number]
                    ),2) / denominator)
                else:
                    total_contribution +=  sym.simplify(math.pow((
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
        leptoquark_processes_contribution: List[Dict[str,sym.Symbol]] = [{} for bin_number in range(number_of_bins)]
        for bin_number in range(number_of_bins):
            denominator = nd_contribution[bin_number] + math.pow(self.leptoquark_parameters.systematic_error, 2) * math.pow(nd_contribution[bin_number],2)
            for decay_process in DecayProcess:
                if decay_process in [DecayProcess.T_CHANNEL_DOUBLE_COUPLING, DecayProcess.T_CHANNEL_COMBINED]:
                    continue
                if decay_process == DecayProcess.PAIR_PRODUCTION:
                    leptoquark_processes_contribution[bin_number][decay_process.value] = KFactor.dictionary[self.leptoquark_parameters.model][decay_process.value] \
                                                                                         * self.cross_sections.coupling_to_cross_section_map[coupling][decay_process.value] \
                                                                                         * self.efficiencies.coupling_to_efficiency_map[decay_process.value][coupling] \
                                                                                         * math.pow(symbolic_coupling, 4) \
                                                                                         * math.pow(self.branching_fraction.branching_fraction, 2) \
                                                                                         * self.leptoquark_parameters.luminosity * 1000
                elif decay_process == DecayProcess.SINGLE_PRODUCTION:
                    leptoquark_processes_contribution[bin_number][decay_process.value] = KFactor.dictionary[self.leptoquark_parameters.model][decay_process.value] \
                                                                                         * self.cross_sections.coupling_to_cross_section_map[coupling][decay_process.value] \
                                                                                         * self.efficiencies.coupling_to_efficiency_map[decay_process.value][coupling] \
                                                                                         * math.pow(symbolic_coupling, 2) \
                                                                                         * self.branching_fraction.branching_fraction \
                                                                                         * self.leptoquark_parameters.luminosity * 1000
                elif decay_process == DecayProcess.INTERFERENCE:
                    leptoquark_processes_contribution[bin_number][decay_process.value] = KFactor.dictionary[self.leptoquark_parameters.model][decay_process.value] \
                                                                                         * self.cross_sections.coupling_to_cross_section_map[coupling][decay_process.value] \
                                                                                         * self.efficiencies.coupling_to_efficiency_map[decay_process.value][coupling] \
                                                                                         * math.pow(symbolic_coupling, 2) \
                                                                                         * self.leptoquark_parameters.luminosity * 1000
                elif decay_process == DecayProcess.T_CHANNEL:
                    leptoquark_processes_contribution[bin_number][decay_process.value] = KFactor.dictionary[self.leptoquark_parameters.model][decay_process.value] \
                                                                                         * self.cross_sections.coupling_to_cross_section_map[coupling][decay_process.value] \
                                                                                         * self.efficiencies.coupling_to_efficiency_map[decay_process.value][coupling] \
                                                                                         * math.pow(symbolic_coupling, 4) \
                                                                                         * self.leptoquark_parameters.luminosity * 1000
                elif decay_process == DecayProcess.PUREQCD and self.leptoquark_parameters.mass <= physics_config.get('pureqcd_contribution_mass_limit'):
                    leptoquark_processes_contribution[bin_number][decay_process.value] = KFactor.dictionary[self.leptoquark_parameters.model][decay_process.value] \
                                                                                         * self.cross_sections.coupling_to_cross_section_map[coupling][decay_process.value] \
                                                                                         * self.efficiencies.coupling_to_efficiency_map[decay_process.value][coupling] \
                                                                                         * math.pow(self.branching_fraction.branching_fraction, 2) \
                                                                                         * self.leptoquark_parameters.luminosity * 1000
            if self.leptoquark_parameters.ignore_single_pair_processes:
                total_contribution += sym.simplify(math.pow((
                        + leptoquark_processes_contribution[bin_number][DecayProcess.T_CHANNEL.value]
                        + leptoquark_processes_contribution[bin_number][DecayProcess.INTERFERENCE.value]
                        + standard_model_contribution[bin_number]
                        - nd_contribution[bin_number]
                ),2) / denominator)
            else:
                total_contribution +=  sym.simplify(math.pow((
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
            leptoquark_processes_contribution: List[Dict[str,sym.Symbol]] = [{} for bin_number in range(number_of_bins)]
            for bin_number in range(number_of_bins):
                denominator = nd_contribution[bin_number] + math.pow(self.leptoquark_parameters.systematic_error, 2) * math.pow(nd_contribution[bin_number],2)
                for decay_process in DecayProcess:
                    if decay_process != DecayProcess.T_CHANNEL:
                        continue
                    leptoquark_processes_contribution[bin_number][decay_process.value] = KFactor.dictionary[self.leptoquark_parameters.model][decay_process.value] \
                                                                                         * self.cross_sections.coupling_to_cross_section_map[cross_terms_coupling][decay_process.value] \
                                                                                         * self.efficiencies.coupling_to_efficiency_map[decay_process.value][cross_terms_coupling][tag.value] \
                                                                                         * math.pow(self.symbolic_sorted_couplings[coupling_1_index], 2) \
                                                                                         * math.pow(self.symbolic_sorted_couplings[coupling_2_index], 2) \
                                                                                         * self.leptoquark_parameters.luminosity * 1000

                total_contribution +=  sym.simplify(math.pow((
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
        leptoquark_processes_contribution: List[Dict[str,sym.Symbol]] = [{} for bin_number in range(number_of_bins)]
        for bin_number in range(number_of_bins):
            denominator = nd_contribution[bin_number] + math.pow(self.leptoquark_parameters.systematic_error, 2) * math.pow(nd_contribution[bin_number],2)
            for decay_process in DecayProcess:
                if decay_process != DecayProcess.T_CHANNEL:
                    continue
                leptoquark_processes_contribution[bin_number][decay_process.value] = KFactor.dictionary[self.leptoquark_parameters.model][decay_process.value] \
                                                                                     * self.cross_sections.coupling_to_cross_section_map[cross_terms_coupling][decay_process.value] \
                                                                                     * self.efficiencies.coupling_to_efficiency_map[decay_process.value][cross_terms_coupling] \
                                                                                     * math.pow(self.symbolic_sorted_couplings[coupling_1_index], 2) \
                                                                                     * math.pow(self.symbolic_sorted_couplings[coupling_2_index], 2) \
                                                                                     * self.leptoquark_parameters.luminosity * 1000

            total_contribution +=  sym.simplify(math.pow((
                    + leptoquark_processes_contribution[bin_number][DecayProcess.T_CHANNEL.value]
                    + standard_model_contribution[bin_number]
                    - nd_contribution[bin_number]
            ),2) / denominator)
        return sym.simplify(total_contribution)

    def calculate_chi_square(self, print_output: bool = False):
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
                        self.leptoquark_parameters.sorted_couplings[i][code_infra_config.get('lepton_index')]
                        == self.leptoquark_parameters.sorted_couplings[j][code_infra_config.get('lepton_index')]
                ):
                    cross_terms_coupling = f"{self.leptoquark_parameters.sorted_couplings[i]}_{self.leptoquark_parameters.sorted_couplings[j]}"
                    if self.leptoquark_parameters.sorted_couplings[i][code_infra_config.get('coupling').get('lepton_index')] == str(Generation.TAU.value):
                        chi_square += self.calculate_double_coupling_contribution_tau_tau(cross_terms_coupling, i, j)
                    else:
                        chi_square += self.calculate_double_coupling_contribution(cross_terms_coupling, i, j)
                    if print_output:
                        print(f"{cross_terms_coupling} contributions calculated!!")
        self.chi_square = chi_square


