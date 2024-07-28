import os
from typing import Dict, Union, List
from utilities.data_classes import SingleCouplingEfficiency, SingleCouplingEfficiencyTauTau, CrossTermsEfficiency, CrossTermsEfficiencyTauTau, TagsTauTau, SingleCouplingCrossSections, CrossTermsCrossSections

def getNumbersFromCsvFiles(directory):
    # List to store the numbers
    numbers = []
    
    # Iterate over all files in the given directory
    for filename in os.listdir(directory):
        # Check if the file ends with .csv
        if filename.endswith('.csv'):
            # Remove the .csv extension and convert to an integer
            number = int(filename[:-4])
            # Add the number to the list
            numbers.append(number)
    
    return numbers

def getImmediateSubdirectories(directory):
    # List to store the names of subdirectories
    subdirectories = []
    
    # Iterate over all entries in the given directory
    for entry in os.listdir(directory):
        # Create the full path
        full_path = os.path.join(directory, entry)
        # Check if the entry is a directory
        if os.path.isdir(full_path):
            # Add the directory name to the list
            subdirectories.append(int(entry))
    
    return subdirectories

def transposeMatrix(matrix):
    # Use zip to transpose the rows to columns and convert them to lists
    columns = [list(column) for column in zip(*matrix)]
    return columns

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

def getEfficienciesFromProcess(process_path: str, coupling_to_process_efficiencies_map: Dict[str, Union[SingleCouplingEfficiency, SingleCouplingEfficiencyTauTau, CrossTermsEfficiency, CrossTermsEfficiencyTauTau]], coupling: str) -> List[float]:
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