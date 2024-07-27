import pandas as pd
from copy import deepcopy
from scipy.interpolate import interp1d

from calculations.helper import getNumbersFromCsvFiles, transposeMatrix, getImmediateSubdirectories
from utilities.constants import get_efficiency_prefix, get_t_ct_prefix, tagNames, lepton_index, quark_index, chirality_index
from utilities.data_classes import LeptoquarkParameters, SingleCouplingEfficiency, CrossTermsEfficiency


def getEfficiencies(
        leptoquark_parameters: LeptoquarkParameters,
        coupling_to_process_cross_section_map: dict,
    ) -> dict:
    """
    Load efficiencies from the data files

    The dict that is returns has mapping:
    Single coupling: coupling -> SingleCouplingEfficiency
    Cross terms: coupling -> CrossTermsEfficiency
    """
    # this map stores the efficiencies for every coupling
    coupling_to_process_efficiencies_map = dict()

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
            coupling_to_process_efficiencies_map[coupling] = readAndInterpolateCsvTautau(efficiency_directory_paths, leptoquark_parameters.leptoquark_mass)
        else:
            coupling_to_process_efficiencies_map[coupling] = readAndInterpolateEfficiency(efficiency_directory_paths, leptoquark_parameters.leptoquark_mass)

    # cross terms
    # TODO: continue from here

    return coupling_to_process_efficiencies_map



    ee_path_t_ct = []
    mumu_path_t_ct = []
    tautau_path_t_ct = []
    for i in range(num_lam):
        for j in range(i + 1, num_lam):
            if lambdastring[i][8] == lambdastring[j][8]:
                if lambdastring[i][8] == "1":
                    ee_path_t_ct.append(
                        get_t_ct_prefix(leptoquark_parameters.leptoquark_model)
                        + str(
                            lambdastring[i][6] + lambdastring[i][8] + lambdastring[i][4]
                        )
                        + "_"
                        + str(
                            lambdastring[j][6] + lambdastring[j][8] + lambdastring[j][4]
                        )
                    )
                elif lambdastring[i][8] == "2":
                    mumu_path_t_ct.append(
                        get_t_ct_prefix(leptoquark_parameters.leptoquark_model)
                        + str(
                            lambdastring[i][6] + lambdastring[i][8] + lambdastring[i][4]
                        )
                        + "_"
                        + str(
                            lambdastring[j][6] + lambdastring[j][8] + lambdastring[j][4]
                        )
                    )
                elif lambdastring[i][8] == "3":
                    tautau_path_t_ct.append(
                        get_t_ct_prefix(leptoquark_parameters.leptoquark_model)
                        + str(
                            lambdastring[i][6] + lambdastring[i][8] + lambdastring[i][4]
                        )
                        + "_"
                        + str(
                            lambdastring[j][6] + lambdastring[j][8] + lambdastring[j][4]
                        )
                        + "/"
                        + str(closest_mass)
                    )

    ee_eff_l = [
        [
            [
                pd.read_csv(
                    path_pureqcd_ee[i] + "/" + str(int(closest_mass)) + ".csv",
                    header=[0],
                ).to_numpy()[:, 2]
            ]
            for i in range(len(path_pureqcd_ee))
        ],
        [
            [
                pd.read_csv(
                    path_pair_ee[i] + "/" + str(int(closest_mass)) + ".csv", header=[0]
                ).to_numpy()[:, 2]
            ]
            for i in range(len(path_pureqcd_ee))
        ],
        [
            [
                pd.read_csv(
                    path_single_ee[i] + "/" + str(int(closest_mass)) + ".csv",
                    header=[0],
                ).to_numpy()[:, 2]
            ]
            for i in range(len(path_pureqcd_ee))
        ],
        [
            [
                pd.read_csv(
                    path_interference_ee[i] + "/" + str(int(closest_mass)) + ".csv",
                    header=[0],
                ).to_numpy()[:, 2]
            ]
            for i in range(len(path_pureqcd_ee))
        ],
        [
            [
                pd.read_csv(
                    path_tchannel_ee[i] + "/" + str(int(closest_mass)) + ".csv",
                    header=[0],
                ).to_numpy()[:, 2]
            ]
            for i in range(len(path_pureqcd_ee))
        ],
    ]

    mumu_eff_l = [
        [
            [
                pd.read_csv(
                    path_pureqcd_mumu[i] + "/" + str(int(closest_mass)) + ".csv",
                    header=[0],
                ).to_numpy()[:, 2]
            ]
            for i in range(len(path_pureqcd_mumu))
        ],
        [
            [
                pd.read_csv(
                    path_pair_mumu[i] + "/" + str(int(closest_mass)) + ".csv",
                    header=[0],
                ).to_numpy()[:, 2]
            ]
            for i in range(len(path_pureqcd_mumu))
        ],
        [
            [
                pd.read_csv(
                    path_single_mumu[i] + "/" + str(int(closest_mass)) + ".csv",
                    header=[0],
                ).to_numpy()[:, 2]
            ]
            for i in range(len(path_pureqcd_mumu))
        ],
        [
            [
                pd.read_csv(
                    path_interference_mumu[i] + "/" + str(int(closest_mass)) + ".csv",
                    header=[0],
                ).to_numpy()[:, 2]
            ]
            for i in range(len(path_pureqcd_mumu))
        ],
        [
            [
                pd.read_csv(
                    path_tchannel_mumu[i] + "/" + str(int(closest_mass)) + ".csv",
                    header=[0],
                ).to_numpy()[:, 2]
            ]
            for i in range(len(path_pureqcd_mumu))
        ],
    ]

    tautau_eff_l = [
        [
            [
                pd.read_csv(path_pureqcd_tautau[i] + j, header=[0]).to_numpy()[:, 2]
                for j in tagNames
            ]
            for i in range(len(path_pureqcd_tautau))
        ],
        [
            [
                pd.read_csv(path_pair_tautau[i] + j, header=[0]).to_numpy()[:, 2]
                for j in tagNames
            ]
            for i in range(len(path_pureqcd_tautau))
        ],
        [
            [
                pd.read_csv(path_single_tautau[i] + j, header=[0]).to_numpy()[:, 2]
                for j in tagNames
            ]
            for i in range(len(path_pureqcd_tautau))
        ],
        [
            [
                pd.read_csv(path_interference_tautau[i] + j, header=[0]).to_numpy()[
                    :, 2
                ]
                for j in tagNames
            ]
            for i in range(len(path_pureqcd_tautau))
        ],
        [
            [
                pd.read_csv(path_tchannel_tautau[i] + j, header=[0]).to_numpy()[:, 2]
                for j in tagNames
            ]
            for i in range(len(path_pureqcd_tautau))
        ],
    ]

    ee_eff_t_ct_temp = [
        [
            pd.read_csv(
                ee_path_t_ct[i] + "/" + str(int(closest_mass)) + ".csv", header=[0]
            ).to_numpy()[:, 2]
        ]
        for i in range(len(ee_path_t_ct))
    ]
    mumu_eff_t_ct_temp = [
        [
            pd.read_csv(
                mumu_path_t_ct[i] + "/" + str(int(closest_mass)) + ".csv", header=[0]
            ).to_numpy()[:, 2]
        ]
        for i in range(len(mumu_path_t_ct))
    ]
    tautau_eff_t_ct_temp = [
        [
            pd.read_csv(tautau_path_t_ct[j] + i, header=[0]).to_numpy()[:, 2]
            for i in tagNames
        ]
        for j in range(len(tautau_path_t_ct))
    ]

    ee_eff_t_ct = deepcopy(ee_eff_t_ct_temp)
    mumu_eff_t_ct = deepcopy(mumu_eff_t_ct_temp)
    tautau_eff_t_ct = deepcopy(tautau_eff_t_ct_temp)

    ee_cntr = 0
    mumu_cntr = 0
    tautau_cntr = 0
    for i in range(len(path_interference_ee)):
        for j in range(i + 1, len(path_interference_ee)):
            ee_eff_t_ct[ee_cntr][0] = (
                ee_eff_t_ct_temp[ee_cntr][0] * cs_ee_t_ct_temp[ee_cntr]
                - ee_eff_l[4][i][0] * ee_cs[4][i]
                - ee_eff_l[4][j][0] * ee_cs[4][j]
            ) / cs_ee_t_ct[ee_cntr]
            ee_cntr += 1
    for i in range(len(path_interference_mumu)):
        for j in range(i + 1, len(path_interference_mumu)):
            mumu_eff_t_ct[mumu_cntr][0] = (
                mumu_eff_t_ct_temp[mumu_cntr][0] * cs_mumu_t_ct_temp[mumu_cntr]
                - mumu_eff_l[4][i][0] * mumu_cs[4][i]
                - mumu_eff_l[4][j][0] * mumu_cs[4][j]
            ) / cs_mumu_t_ct[mumu_cntr]
            mumu_cntr += 1
    for i in range(len(path_interference_tautau)):
        for j in range(i + 1, len(path_interference_tautau)):
            for tag_num in range(4):
                tautau_eff_t_ct[tautau_cntr][tag_num] = (
                    tautau_eff_t_ct_temp[tautau_cntr][tag_num]
                    * cs_tautau_t_ct_temp[tautau_cntr]
                    - tautau_eff_l[4][i][tag_num] * tautau_cs[4][i]
                    - tautau_eff_l[4][j][tag_num] * tautau_cs[4][j]
                ) / cs_tautau_t_ct[tautau_cntr]
            tautau_cntr += 1
    ee_lambdas_len = len(path_pureqcd_ee)
    mumu_lambdas_len = len(path_pureqcd_mumu)
    tautau_lambdas_len = len(path_pureqcd_tautau)
    return [
        ee_eff_l,
        mumu_eff_l,
        tautau_eff_l,
        ee_eff_t_ct,
        mumu_eff_t_ct,
        tautau_eff_t_ct,
        ee_lambdas_len,
        mumu_lambdas_len,
        tautau_lambdas_len,
    ]

def readAndInterpolateEfficiency(path_list, mass):
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
            interpolated_mass_values.append(interpolation_function(mass))
        process_values.append(interpolated_mass_values)
    
    return process_values


def readAndInterpolateCsvTautau(path_list, mass):
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
                interpolated_mass_values.append(interpolation_function(mass))
            tag_values.append(interpolated_mass_values)
        process_values.append(tag_values)    
    
    return process_values