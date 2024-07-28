import pandas as pd
from typing import Dict, Union, List
from copy import deepcopy
from scipy.interpolate import interp1d

from calculations.helper import getNumbersFromCsvFiles, transposeMatrix, getImmediateSubdirectories
from utilities.constants import get_efficiency_prefix, get_t_ct_prefix, tagNames, lepton_index, quark_index, chirality_index
from utilities.data_classes import LeptoquarkParameters, SingleCouplingEfficiency, SingleCouplingEfficiencyTauTau, CrossTermsEfficiency, CrossTermsEfficiencyTauTau, TagsTauTau, SingleCouplingCrossSections, CrossTermsCrossSections


def getEfficiencies(
        leptoquark_parameters: LeptoquarkParameters,
        coupling_to_process_cross_section_map: Dict[str, Union[SingleCouplingCrossSections, CrossTermsCrossSections]],
    ) -> dict:
    """
    Load efficiencies from the data files

    The dict that is returns has mapping:
    Single coupling: coupling -> SingleCouplingEfficiency
    Cross terms: coupling -> CrossTermsEfficiency
    """
    # this map stores the efficiencies for every coupling
    coupling_to_process_efficiencies_map: Dict[str, Union[SingleCouplingEfficiency, SingleCouplingEfficiencyTauTau, CrossTermsEfficiency, CrossTermsEfficiencyTauTau]] = {}

    # directory paths of efficiency files
    path_interference = [
        f"{get_efficiency_prefix(leptoquark_parameters.leptoquark_model)}/i/{coupling[lepton_index]}{coupling[quark_index]}{coupling[chirality_index]}/"
        for coupling in leptoquark_parameters.sorted_couplings
    ]
    path_pair = [
        f"{get_efficiency_prefix(leptoquark_parameters.leptoquark_model)}/p/{coupling[lepton_index]}{coupling[quark_index]}{coupling[chirality_index]}/"
        for coupling in leptoquark_parameters.sorted_couplings
    ]
    path_single = [
        f"{get_efficiency_prefix(leptoquark_parameters.leptoquark_model)}/s/{coupling[lepton_index]}{coupling[quark_index]}{coupling[chirality_index]}/"
        for coupling in leptoquark_parameters.sorted_couplings
    ]
    path_tchannel = [
        f"{get_efficiency_prefix(leptoquark_parameters.leptoquark_model)}/t/{coupling[lepton_index]}{coupling[quark_index]}{coupling[chirality_index]}/"
        for coupling in leptoquark_parameters.sorted_couplings
    ]
    path_pureqcd = [
        f"{get_efficiency_prefix(leptoquark_parameters.leptoquark_model)}/q/{coupling[lepton_index]}{coupling[quark_index]}{coupling[chirality_index]}/"
        for coupling in leptoquark_parameters.sorted_couplings
    ]
    # Order: qpits
    efficiency_directory_paths = [path_pureqcd, path_pair, path_interference, path_tchannel, path_single]

    # single coupling efficiencies
    for coupling in leptoquark_parameters.sorted_couplings:
        # case tau tau
        if coupling[quark_index] == 3:
            coupling_to_process_efficiencies_map[coupling] = readAndInterpolateEfficiencyTauTau(efficiency_directory_paths, leptoquark_parameters)
        else:
            coupling_to_process_efficiencies_map[coupling] = readAndInterpolateEfficiency(efficiency_directory_paths, leptoquark_parameters)

    # cross terms
    for i in range(len(leptoquark_parameters.sorted_couplings)):
        for j in range(i+1, len(leptoquark_parameters.sorted_couplings)):
            # if couplings belong to the same category
            if leptoquark_parameters.couplings[i][quark_index] == leptoquark_parameters.couplings[j][quark_index]:
                cross_terms_coupling = f"{leptoquark_parameters.sorted_couplings[i]}_{leptoquark_parameters.sorted_couplings[j]}"
                cross_terms_directory_path = f"{get_efficiency_prefix(leptoquark_parameters.leptoquark_model)}/t/{leptoquark_parameters.couplings[i][lepton_index]}{leptoquark_parameters.couplings[i][quark_index]}{leptoquark_parameters.couplings[i][chirality_index]}_{leptoquark_parameters.couplings[j][lepton_index]}{leptoquark_parameters.couplings[j][quark_index]}{leptoquark_parameters.couplings[j][chirality_index]}/"
                if coupling[quark_index] == 3:
                    coupling_to_process_efficiencies_map[cross_terms_coupling] = readAndInterpolateEfficiencyTauTau([[cross_terms_directory_path]], leptoquark_parameters, coupling_to_process_cross_section_map, coupling_to_process_efficiencies_map, cross_terms_coupling, cross_terms= True)
                else:
                    coupling_to_process_efficiencies_map[cross_terms_coupling] = readAndInterpolateEfficiency([[cross_terms_directory_path]], leptoquark_parameters, coupling_to_process_cross_section_map, coupling_to_process_efficiencies_map, cross_terms_coupling, cross_terms= True)

    return coupling_to_process_efficiencies_map


def readAndInterpolateEfficiency(path_list: List[List[str]], leptoquark_parameters: LeptoquarkParameters, coupling_to_process_cross_section_map: Dict[str, Union[SingleCouplingCrossSections, CrossTermsCrossSections]] = {}, coupling_to_process_efficiencies_map: Dict[str, Union[SingleCouplingEfficiency, SingleCouplingEfficiencyTauTau, CrossTermsEfficiency, CrossTermsEfficiencyTauTau]] = {}, cross_terms_coupling: str = "", coupling1: str = "", coupling2: str = "", cross_terms: bool = False):
    # variable which has a list of efficiencies corresponding to each process for given mass
    process_values = []
    for process_path in path_list:
        data_mass_list = getNumbersFromCsvFiles(process_path)
        # variable which has a list of efficiencies corresponding
        mass_values = []
        for file in data_mass_list:
            file_path = f"{process_path}{file}.csv"
            data = pd.read_csv(file_path, header=[0]).to_numpy()[:, 2]
            mass_values.append(data)

        # taking the transpose as we will interpolate over each bin
        transposed_mass_values = transposeMatrix(mass_values)
        # this will have a list of interpolated values corresponding to each bin
        interpolated_mass_values = []
        # start interpolation
        for bin_values in transposed_mass_values:
            interpolation_function = lambda m: interp1d(data_mass_list, bin_values, kind="slinear")(m)
            interpolated_mass_values.append(interpolation_function(leptoquark_parameters.leptoquark_mass))
        if cross_terms:
            cross_terms_interpolated_values = []
            # get single couplings cross-sections
            coupling1_cross_section = getCrossSectionFromProcess(process_path, coupling_to_process_cross_section_map, coupling1)
            coupling2_cross_section = getCrossSectionFromProcess(process_path, coupling_to_process_cross_section_map, coupling2)
            # get single couplings efficiencies
            coupling1_efficiencies = getEfficienciesFromProcessAndTagName(process_path, coupling_to_process_efficiencies_map, coupling1)
            coupling2_efficiencies = getEfficienciesFromProcessAndTagName(process_path, coupling_to_process_efficiencies_map, coupling2)
            for interpolated_mass_value, coupling1_efficiency, coupling2_efficiency in zip(interpolated_mass_values, coupling1_efficiencies, coupling2_efficiencies):
            # we compute the cross-terms efficiency using the formula
            # CS1 * EFF1 + CS2 * EFF2 + cross-terms-CS *  cross-terms-EFF = 2-couplings-CS * 2-couplings-EFF
                cross_terms_efficiency = (
                    coupling_to_process_cross_section_map[cross_terms_coupling].actual_cross_section_tchannel * interpolated_mass_value
                    - coupling1_cross_section * coupling1_efficiency
                    - coupling2_cross_section * coupling2_efficiency
                ) / (coupling_to_process_cross_section_map[cross_terms_coupling].cross_terms_cross_section_tchannel)
                cross_terms_interpolated_values.append(cross_terms_efficiency)
            process_values.append(cross_terms_interpolated_values)
        else:    
            process_values.append(interpolated_mass_values)
    
    # if we are interpolating cross-terms, then we only need to parse t-channel
    if cross_terms == True:
        return CrossTermsEfficiency(
            efficiency_tchannel = process_values[0],
        )

    # Processes order: qpits
    # We convert efficiencies list from this to SingleCouplingEfficiency object
    return SingleCouplingEfficiency(
        efficiency_pureqcd = process_values[0],
        efficiency_pair_production = process_values[1],
        efficiency_interference = process_values[2],
        efficiency_tchannel = process_values[3],
        efficiency_single_production = process_values[4],
    )

def getCrossSectionFromProcess(process_path: str, coupling_to_process_cross_section_map: Dict[str, Union[SingleCouplingCrossSections, CrossTermsCrossSections]], coupling: str) -> float:
    singleCouplingCrossSection = coupling_to_process_cross_section_map[coupling]
    # Path: {DATA_PREFIX}/model/{model}/efficiency/i/{coupling[lepton_index]}{coupling[quark_index]}{coupling[chirality_index]}/
    if process_path.split('/')[4] == 'q':
        return singleCouplingCrossSection.cross_section_pureqcd
    elif process_path.split('/')[4] == 'p':
        return singleCouplingCrossSection.cross_section_pair_production
    elif process_path.split('/')[4] == 'i':
        return singleCouplingCrossSection.cross_section_interference
    elif process_path.split('/')[4] == 't':
        return singleCouplingCrossSection.cross_section_tchannel
    elif process_path.split('/')[4] == 's':
        return singleCouplingCrossSection.cross_section_single_production
    return 0

def getEfficienciesFromProcessAndTagName(process_path: str, coupling_to_process_efficiencies_map: Dict[str, Union[SingleCouplingEfficiency, SingleCouplingEfficiencyTauTau, CrossTermsEfficiency, CrossTermsEfficiencyTauTau]], coupling: str) -> List[float]:
    efficienciesObject = coupling_to_process_efficiencies_map[coupling]
    # Path: {DATA_PREFIX}/model/{model}/efficiency/i/{coupling[lepton_index]}{coupling[quark_index]}{coupling[chirality_index]}/
    if process_path.split('/')[4] == 'q':
        return efficienciesObject.efficiency_pureqcd
    elif process_path.split('/')[4] == 'p':
        return efficienciesObject.efficiency_pair_production
    elif process_path.split('/')[4] == 'i':
        return efficienciesObject.efficiency_interference
    elif process_path.split('/')[4] == 't':
        return efficienciesObject.efficiency_tchannel
    elif process_path.split('/')[4] == 's':
        return efficienciesObject.efficiency_single_production

    return []

def readAndInterpolateEfficiencyTauTau(path_list: List[List[str]], leptoquark_parameters: LeptoquarkParameters, coupling_to_process_cross_section_map: Dict[str, Union[SingleCouplingCrossSections, CrossTermsCrossSections]] = {}, coupling_to_process_efficiencies_map: Dict[str, Union[SingleCouplingEfficiency, SingleCouplingEfficiencyTauTau, CrossTermsEfficiency, CrossTermsEfficiencyTauTau]] = {}, cross_terms_coupling: str = "", coupling1: str = "", coupling2: str = "", cross_terms: bool = False):
    # variable which has a list of efficiencies corresponding to each process for given mass
    process_values = []
    for process_path in path_list:
        data_mass_list = getImmediateSubdirectories(process_path)
        # variable which has a list of efficiencies corresponding to each tag
        tag_values = []
        for tagName in tagNames:
            mass_values = []
            for file in data_mass_list:
                file_path = f"{process_path}{file}/{tagName}"
                data = pd.read_csv(file_path, header=[0]).to_numpy()[:, 2]
                mass_values.append(data)

            # taking the transpose as we will interpolate over each bin
            transposed_mass_values = transposeMatrix(mass_values)
            # this will have a list of interpolated values corresponding to each bin
            interpolated_mass_values = []
            # start interpolation
            for bin_values in transposed_mass_values:
                interpolation_function = lambda m: interp1d(data_mass_list, bin_values, kind="slinear")(m)
                interpolated_mass_values.append(interpolation_function(leptoquark_parameters.leptoquark_mass))
            if cross_terms:
                cross_terms_interpolated_values = []
                # get single couplings cross-sections
                coupling1_cross_section = getCrossSectionFromProcess(process_path, coupling_to_process_cross_section_map, coupling1)
                coupling2_cross_section = getCrossSectionFromProcess(process_path, coupling_to_process_cross_section_map, coupling2)
                # get single couplings efficiencies
                coupling1_efficiencies = getEfficienciesFromProcessAndTagNameTauTau(process_path, tagName, coupling_to_process_efficiencies_map, coupling1)
                coupling2_efficiencies = getEfficienciesFromProcessAndTagNameTauTau(process_path, tagName, coupling_to_process_efficiencies_map, coupling2)
                for interpolated_mass_value, coupling1_efficiency, coupling2_efficiency in zip(interpolated_mass_values, coupling1_efficiencies, coupling2_efficiencies):
                # we compute the cross-terms efficiency using the formula
                # CS1 * EFF1 + CS2 * EFF2 + cross-terms-CS *  cross-terms-EFF = 2-couplings-CS * 2-couplings-EFF
                    cross_terms_efficiency = (
                        coupling_to_process_cross_section_map[cross_terms_coupling].actual_cross_section_tchannel * interpolated_mass_value
                        - coupling1_cross_section * coupling1_efficiency
                        - coupling2_cross_section * coupling2_efficiency
                    ) / (coupling_to_process_cross_section_map[cross_terms_coupling].cross_terms_cross_section_tchannel)
                    cross_terms_interpolated_values.append(cross_terms_efficiency)
                tag_values.append(cross_terms_interpolated_values)
            else:
                tag_values.append(interpolated_mass_values)
        # Tagnames order: HHbT, HHbV, LHbT, LHbV
        # Convert these tagnames to TagsTauTau object
        tagsTauTau = TagsTauTau(
            hhbt = tag_values[0],
            hhbv = tag_values[1],
            lhbt = tag_values[2],
            lhbv = tag_values[3],
        )
        process_values.append(tagsTauTau)    
    
    # if we are interpolating cross-terms, then we only need to parse t-channel
    if cross_terms == True:
        return CrossTermsEfficiencyTauTau(
            efficiency_tchannel = process_values[0],
        )
    
    # Processes order: qpits
    # We convert efficiencies list from this to SingleCouplingEfficiency object
    return SingleCouplingEfficiencyTauTau(
        efficiency_pureqcd = process_values[0],
        efficiency_pair_production = process_values[1],
        efficiency_interference = process_values[2],
        efficiency_tchannel = process_values[3],
        efficiency_single_production = process_values[4],
    )

def getEfficienciesFromProcessAndTagNameTauTau(process_path: str, tagName: str, coupling_to_process_efficiencies_map: Dict[str, Union[SingleCouplingEfficiency, SingleCouplingEfficiencyTauTau, CrossTermsEfficiency, CrossTermsEfficiencyTauTau]], coupling: str) -> List[float]:
    efficienciesObject = coupling_to_process_efficiencies_map[coupling]
    # Path: {DATA_PREFIX}/model/{model}/efficiency/i/{coupling[lepton_index]}{coupling[quark_index]}{coupling[chirality_index]}/
    # get TagsTauTau object
    tagsTauTau: TagsTauTau
    if process_path.split('/')[4] == 'q':
        tagsTauTau = efficienciesObject.efficiency_pureqcd
    elif process_path.split('/')[4] == 'p':
        tagsTauTau = efficienciesObject.efficiency_pair_production
    elif process_path.split('/')[4] == 'i':
        tagsTauTau = efficienciesObject.efficiency_interference
    elif process_path.split('/')[4] == 't':
        tagsTauTau = efficienciesObject.efficiency_tchannel
    elif process_path.split('/')[4] == 's':
        tagsTauTau = efficienciesObject.efficiency_single_production
    
    # from TagsTauTau object, we get the list of efficiencies
    if tagName == "HHbT.csv":
        return tagsTauTau.hhbt
    elif tagName == "HHbV.csv":
        return tagsTauTau.hhbv
    elif tagName == "LHbT.csv":
        return tagsTauTau.lhbt
    elif tagName == "LHbV.csv":
        return tagsTauTau.lhbv

    return []