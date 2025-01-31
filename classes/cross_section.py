import pandas as pd
from typing import Dict
from scipy.interpolate import interp1d

from classes.leptoquark_parameters import  LeptoquarkParameters
from classes.custom_datatypes import DecayProcess
from classes.config import file_paths_config, code_infra_config

# class SingleCouplingCrossSections:
#     def __init__(
#             self,
#             cross_section_pureqcd: float,
#             cross_section_pair_production: float,
#             cross_section_single_production: float,
#             cross_section_interference: float,
#             cross_section_tchannel: float,
#     ):
#         self.cross_section_pureqcd = cross_section_pureqcd
#         self.cross_section_pair_production = cross_section_pair_production
#         self.cross_section_single_production = cross_section_single_production
#         self.cross_section_interference = cross_section_interference
#         self.cross_section_tchannel = cross_section_tchannel

    # def __str__(self):
    #     return (
    #         f"Cross Section Pure QCD: {self.cross_section_pureqcd}\n"
    #         f"Cross Section Pair Production: {self.cross_section_pair_production}\n"
    #         f"Cross Section Single Production: {self.cross_section_single_production}\n"
    #         f"Cross Section Interference: {self.cross_section_interference}\n"
    #         f"Cross Section T-Channel: {self.cross_section_tchannel}"
    #     )

# class CrossTermsCrossSections:
#         def __init__(
#                 self,
#                 # the cross-section to be used for cross-terms
#                 cross_terms_cross_section_tchannel: float,
#                 # the cross-section when 2 couplings are switched on
#                 actual_cross_section_tchannel: float,
#         ):
#             self.cross_terms_cross_section_tchannel = cross_terms_cross_section_tchannel
#             self.actual_cross_section_tchannel = actual_cross_section_tchannel
#
#     def __str__(self):
#         return (
#             f"Cross-Terms Cross Section T-Channel: {self.cross_terms_cross_section_tchannel}\n"
#             f"Actual Cross Section T-Channel: {self.actual_cross_section_tchannel}"
#         )


class CrossSections:
    def __init__(
            self,
            # Usage: coupling_to_cross_section_map[coupling][decay_process]
            coupling_to_cross_section_map: Dict[str, Dict[str, float]] = None,
        ):
            self.coupling_to_cross_section_map = coupling_to_cross_section_map

    def __getitem__(self, key):
        return self.coupling_to_cross_section_map[key]

    @staticmethod
    # returns pandas dataframe object
    def read_from_data_file(leptoquark_parameters: LeptoquarkParameters, process: DecayProcess):
        return pd.read_csv(
            f"{file_paths_config.get('data_prefix')}/model/{leptoquark_parameters.model}/cross_section/{process.value}.csv",
            header=[0],
        )
    
    @staticmethod
    def interpolate_and_extrapolate_linearly(leptoquark_parameters: LeptoquarkParameters, cross_section_data_frame, coupling) -> float:
        interpolation_function = lambda mass: interp1d(cross_section_data_frame["Mass"], cross_section_data_frame[coupling], kind="slinear", fill_value="extrapolate")(
                mass
            )
        return interpolation_function(leptoquark_parameters.mass)

    def fill_single_coupling_to_cross_section_map(self,leptoquark_parameters: LeptoquarkParameters):
        # read & interpolate for single coupling
        for sorted_coupling in leptoquark_parameters.sorted_couplings:
            for decay_process in DecayProcess:
                # ignore double coupling
                if decay_process in [DecayProcess.T_CHANNEL_DOUBLE_COUPLING, DecayProcess.T_CHANNEL_COMBINED]:
                    continue
                data_frame = CrossSections.read_from_data_file(leptoquark_parameters, decay_process)
                self.coupling_to_cross_section_map[sorted_coupling][decay_process.value] = round(CrossSections.interpolate_and_extrapolate_linearly(leptoquark_parameters, data_frame, sorted_coupling), code_infra_config.get('global_data_precision'))

    def fill_double_coupling_to_cross_section_map(self,leptoquark_parameters: LeptoquarkParameters):
        for i in range(len(leptoquark_parameters.sorted_couplings)):
            for j in range(i + 1, len(leptoquark_parameters.sorted_couplings)):
                if (
                    leptoquark_parameters.sorted_couplings[i][code_infra_config.get('lepton_index')]
                    == leptoquark_parameters.sorted_couplings[j][code_infra_config.get('lepton_index')]
                ):
                    cross_terms_coupling = f"{leptoquark_parameters.sorted_couplings[i]}_{leptoquark_parameters.sorted_couplings[j]}"
                    cross_terms_data_frame = CrossSections.read_from_data_file(leptoquark_parameters, DecayProcess.T_CHANNEL_DOUBLE_COUPLING)
                    cross_terms_cross_section_tchannel = round(CrossSections.interpolate_and_extrapolate_linearly(leptoquark_parameters, cross_terms_data_frame, cross_terms_coupling), code_infra_config.get('global_data_precision'))
                    self.coupling_to_cross_section_map[cross_terms_coupling][DecayProcess.T_CHANNEL_COMBINED.value] = cross_terms_cross_section_tchannel
                    self.coupling_to_cross_section_map[cross_terms_coupling][DecayProcess.T_CHANNEL_DOUBLE_COUPLING.value] = round(
                        cross_terms_cross_section_tchannel
                        - self.coupling_to_cross_section_map[leptoquark_parameters.sorted_couplings[i]][DecayProcess.T_CHANNEL.value]
                        - self.coupling_to_cross_section_map[leptoquark_parameters.sorted_couplings[j]][DecayProcess.T_CHANNEL.value],
                        code_infra_config.get('global_data_precision')
                    )

    def fill_all_couplings_to_cross_section_map(self,leptoquark_parameters: LeptoquarkParameters):
        self.fill_single_coupling_to_cross_section_map(leptoquark_parameters)
        self.fill_double_coupling_to_cross_section_map(leptoquark_parameters)
