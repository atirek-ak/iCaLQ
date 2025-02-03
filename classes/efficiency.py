import pandas as pd
from typing import Dict, List, Union
from scipy.interpolate import interp1d

from classes.leptoquark_parameters import  LeptoquarkParameters
from classes.custom_datatypes import DecayProcess, Generation, Tag
from classes.config import file_paths_config, code_infra_config
from classes.cross_section import CrossSections
from helper.paths import get_immediate_sub_directories, get_immediate_sub_directory_csv_files
from helper.matrix import transpose_matrix

class Efficiencies:
    def __init__(
        self,
            # Usage:
            # [process][coupling]
            # [process][coupling][tag] (for 3rd generation leptons where a tag is one of HHbT, HHbV, LHbT, LHbV)
            coupling_to_efficiency_map: Union[
                Dict[str, Dict[str, List[float]]],
                Dict[str, Dict[str, Dict[str, List[float]]]],
            ] = {},
    ):
        self.coupling_to_efficiency_map = coupling_to_efficiency_map

    @staticmethod
    def get_directory_path_for_single_coupling(leptoquark_model: str, decay_process: DecayProcess, coupling:str) -> str:
        directory_path = f"{file_paths_config.get('data_prefix')}/model/{leptoquark_model}/efficiency/{decay_process.value}"\
                        f"/{coupling[code_infra_config.get('coupling').get('quark_index')]}{coupling[code_infra_config.get('coupling').get('lepton_index')]}{coupling[code_infra_config.get('coupling').get('chirality_index')]}"
        return directory_path

    @staticmethod
    def get_directory_path_for_double_coupling(leptoquark_model: str, decay_process: DecayProcess, coupling1:str, coupling2:str,) -> str:
        directory_path = f"{file_paths_config.get('data_prefix')}/model/{leptoquark_model}/efficiency/{decay_process.value}" \
                            f"/{coupling1[code_infra_config.get('coupling').get('quark_index')]}{coupling1[code_infra_config.get('coupling').get('lepton_index')]}{coupling1[code_infra_config.get('coupling').get('chirality_index')]}_"\
                            f"/{coupling2[code_infra_config.get('coupling').get('quark_index')]}{coupling2[code_infra_config.get('coupling').get('lepton_index')]}{coupling2[code_infra_config.get('coupling').get('chirality_index')]}"
        return directory_path

    @staticmethod
    def read_and_interpolate_and_extrapolate_linearly_for_single_coupling(leptoquark_parameters: LeptoquarkParameters, process: DecayProcess, coupling: str) -> List[float]:
        coupling_directory_path = Efficiencies.get_directory_path_for_single_coupling(leptoquark_parameters.model, process, coupling)
        mass_csv_files = get_immediate_sub_directory_csv_files(coupling_directory_path)
        mass_csv_files_int = [int(entry.split('.')[0]) for entry in mass_csv_files]
        # Sort both lists by the order of mass_csv_files_int
        mass_csv_files, mass_csv_files_int = zip(*sorted(zip(mass_csv_files, mass_csv_files_int), key=lambda x: x[1]))
        mass_csv_files = list(mass_csv_files)
        mass_csv_files_int = list(mass_csv_files_int)
        mass_values = []
        for mass_csv_file in mass_csv_files:
            csv_file_path = f"{coupling_directory_path}/{mass_csv_file}"
            data = pd.read_csv(csv_file_path, header=[0]).to_numpy()[:, 2]
            mass_values.append(data)

        # taking the transpose as we will interpolate over each bin
        transposed_mass_values = transpose_matrix(mass_values)

        interpolated_mass_values = []
        for bin_values in transposed_mass_values:
            def interpolation_function(mass): return interp1d(
                mass_csv_files_int, bin_values, kind="slinear", fill_value="extrapolate"
            )(mass)

            interpolated_mass_values.append(
                round(float(interpolation_function(leptoquark_parameters.mass)), code_infra_config.get('global_data_precision'))
            )

        return interpolated_mass_values


    @staticmethod
    def read_and_interpolate_and_extrapolate_linearly_for_single_coupling_with_tags(leptoquark_parameters: LeptoquarkParameters, process: DecayProcess, coupling: str) -> Dict[str, List[float]]:
        coupling_directory_path = Efficiencies.get_directory_path_for_single_coupling(leptoquark_parameters.model, process, coupling)
        mass_directories = get_immediate_sub_directories(coupling_directory_path)
        mass_directories_int = [int(entry) for entry in mass_directories]
        # Sort both lists by the order of mass_csv_files_int
        mass_directories, mass_directories_int = zip(*sorted(zip(mass_directories, mass_directories_int), key=lambda x: x[1]))
        mass_directories = list(mass_directories)
        mass_directories_int = list(mass_directories_int)
        tag_values: Dict[str, List[float]] = {}
        for tag in Tag:
            mass_values = []
            for mass_directory in mass_directories:
                csv_file_path = f"{coupling_directory_path}/{mass_directory}/{tag.value}.csv"
                data = pd.read_csv(csv_file_path, header=[0]).to_numpy()[:, 2]
                mass_values.append(data)

            # taking the transpose as we will interpolate over each bin
            transposed_mass_values = transpose_matrix(mass_values)
            interpolated_mass_values = []
            for bin_values in transposed_mass_values:
                def interpolation_function(mass): return float(interp1d(
                    mass_directories_int, bin_values, kind="slinear", fill_value="extrapolate"
                )(mass))
                interpolated_mass_values.append(
                    round(float(interpolation_function(leptoquark_parameters.mass)), code_infra_config.get('global_data_precision'))
                )
            tag_values[tag.value] = interpolated_mass_values

        return tag_values

    def fill_single_coupling_to_efficiency_map(self, leptoquark_parameters: LeptoquarkParameters):
        for decay_process in DecayProcess:
            self.coupling_to_efficiency_map[decay_process.value] = {}
            # ignore double coupling
            if decay_process in [DecayProcess.T_CHANNEL_DOUBLE_COUPLING, DecayProcess.T_CHANNEL_COMBINED]:
                continue
            for sorted_coupling in leptoquark_parameters.sorted_couplings:
                if sorted_coupling[code_infra_config.get('coupling').get('lepton_index')] == str(Generation.TAU.value):
                    self.coupling_to_efficiency_map[decay_process.value][sorted_coupling] = Efficiencies.read_and_interpolate_and_extrapolate_linearly_for_single_coupling_with_tags(leptoquark_parameters, decay_process, sorted_coupling)
                else:
                    self.coupling_to_efficiency_map[decay_process.value][sorted_coupling] = Efficiencies.read_and_interpolate_and_extrapolate_linearly_for_single_coupling(leptoquark_parameters, decay_process, sorted_coupling)

    def fill_double_coupling_to_efficiency_map(self, leptoquark_parameters: LeptoquarkParameters, cross_sections: CrossSections):
        for i in range(len(leptoquark_parameters.sorted_couplings)):
            for j in range(i + 1, len(leptoquark_parameters.sorted_couplings)):
                if (
                        leptoquark_parameters.sorted_couplings[i][code_infra_config.get('coupling').get('lepton_index')]
                        == leptoquark_parameters.sorted_couplings[j][code_infra_config.get('coupling').get('lepton_index')]
                ):
                    cross_terms_coupling = f"{leptoquark_parameters.sorted_couplings[i]}_{leptoquark_parameters.sorted_couplings[j]}"
                    if leptoquark_parameters.sorted_couplings[i][code_infra_config.get('coupling').get('lepton_index')] == str(Generation.TAU.value):
                        tag_values: Dict[str, List[float]] = {}
                        for tag in Tag:
                            combined_efficiencies = Efficiencies.read_and_interpolate_and_extrapolate_linearly_for_single_coupling_with_tags(leptoquark_parameters, DecayProcess.T_CHANNEL, cross_terms_coupling)[tag.value]
                            coupling_1_efficiencies = self.coupling_to_efficiency_map[DecayProcess.T_CHANNEL.value][leptoquark_parameters.sorted_couplings[i]][tag.value]
                            coupling_2_efficiencies = self.coupling_to_efficiency_map[DecayProcess.T_CHANNEL.value][leptoquark_parameters.sorted_couplings[j]][tag.value]
                            cross_terms_efficiency = []
                            for (
                                combined_efficiency,
                                coupling_1_efficiency,
                                coupling_2_efficiency,
                            ) in zip(combined_efficiencies, coupling_1_efficiencies, coupling_2_efficiencies):
                                cross_terms_efficiency.append(round((
                                    combined_efficiency * cross_sections[cross_terms_coupling][DecayProcess.T_CHANNEL_COMBINED.value]
                                    - coupling_1_efficiency * cross_sections[leptoquark_parameters.sorted_couplings[i]][DecayProcess.T_CHANNEL.value]
                                    - coupling_2_efficiency * cross_sections[leptoquark_parameters.sorted_couplings[j]][DecayProcess.T_CHANNEL.value]
                                ) / cross_sections[cross_terms_coupling][DecayProcess.T_CHANNEL_DOUBLE_COUPLING.value], code_infra_config.get('global_data_precision')))
                            tag_values[tag.value] = cross_terms_efficiency
                        self.coupling_to_efficiency_map[DecayProcess.T_CHANNEL.value][cross_terms_coupling] = tag_values
                    else:
                        combined_efficiencies = Efficiencies.read_and_interpolate_and_extrapolate_linearly_for_single_coupling(leptoquark_parameters, DecayProcess.T_CHANNEL, cross_terms_coupling)
                        coupling_1_efficiencies = self.coupling_to_efficiency_map[DecayProcess.T_CHANNEL.value][leptoquark_parameters.sorted_couplings[i]]
                        coupling_2_efficiencies = self.coupling_to_efficiency_map[DecayProcess.T_CHANNEL.value][leptoquark_parameters.sorted_couplings[j]]
                        cross_terms_efficiency = []
                        for (
                                combined_efficiency,
                                coupling_1_efficiency,
                                coupling_2_efficiency,
                        ) in zip(combined_efficiencies, coupling_1_efficiencies, coupling_2_efficiencies):
                            cross_terms_efficiency.append(round((
                                combined_efficiency * cross_sections[cross_terms_coupling][DecayProcess.T_CHANNEL_COMBINED.value]
                                - coupling_1_efficiency * cross_sections[leptoquark_parameters.sorted_couplings[i]][DecayProcess.T_CHANNEL.value]
                                - coupling_2_efficiency * cross_sections[leptoquark_parameters.sorted_couplings[j]][DecayProcess.T_CHANNEL.value]
                        ) / cross_sections[cross_terms_coupling][DecayProcess.T_CHANNEL_DOUBLE_COUPLING.value], code_infra_config.get('global_data_precision')))
                        self.coupling_to_efficiency_map[DecayProcess.T_CHANNEL.value][cross_terms_coupling] = cross_terms_efficiency

    def fill_all_couplings_to_efficiency_map(self, leptoquark_parameters: LeptoquarkParameters, cross_sections: CrossSections):
        self.fill_single_coupling_to_efficiency_map(leptoquark_parameters)
        self.fill_double_coupling_to_efficiency_map(leptoquark_parameters, cross_sections)