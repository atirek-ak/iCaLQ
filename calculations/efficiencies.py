import pandas as pd
from copy import deepcopy

from utilities.constants import efficiency_prefix, t_ct_prefix, tagnames


def get_efficiencies(closest_mass, lambdastring, num_lam, cs_list):
    """
    Load efficiencies from the data files
    """
    [
        ee_cs,
        mumu_cs,
        tautau_cs,
        cs_ee_t_ct,
        cs_mumu_t_ct,
        cs_tautau_t_ct,
        cs_ee_t_ct_temp,
        cs_mumu_t_ct_temp,
        cs_tautau_t_ct_temp,
    ] = cs_list

    path_interference_ee = [
        efficiency_prefix + "i/" + str(coupling[2:])
        for coupling in lambdastring
        if coupling[3] == "1"
    ]
    path_pair_ee = [
        efficiency_prefix + "p/" + str(coupling[2:])
        for coupling in lambdastring
        if coupling[3] == "1"
    ]
    path_single_ee = [
        efficiency_prefix + "s/" + str(coupling[2:])
        for coupling in lambdastring
        if coupling[3] == "1"
    ]
    path_tchannel_ee = [
        efficiency_prefix + "t/" + str(coupling[2:])
        for coupling in lambdastring
        if coupling[3] == "1"
    ]
    path_pureqcd_ee = [
        efficiency_prefix + "q/" + str(coupling[2:])
        for coupling in lambdastring
        if coupling[3] == "1"
    ]

    path_interference_mumu = [
        efficiency_prefix + "i/" + str(coupling[2:])
        for coupling in lambdastring
        if coupling[3] == "2"
    ]
    path_pair_mumu = [
        efficiency_prefix + "p/" + str(coupling[2:])
        for coupling in lambdastring
        if coupling[3] == "2"
    ]
    path_single_mumu = [
        efficiency_prefix + "s/" + str(coupling[2:])
        for coupling in lambdastring
        if coupling[3] == "2"
    ]
    path_tchannel_mumu = [
        efficiency_prefix + "t/" + str(coupling[2:])
        for coupling in lambdastring
        if coupling[3] == "2"
    ]
    path_pureqcd_mumu = [
        efficiency_prefix + "q/" + str(coupling[2:])
        for coupling in lambdastring
        if coupling[3] == "2"
    ]

    path_interference_tautau = [
        efficiency_prefix + "i/" + str(coupling[2:]) + "/" + str(closest_mass)
        for coupling in lambdastring
        if coupling[3] == "3"
    ]
    path_pair_tautau = [
        efficiency_prefix + "p/" + str(coupling[2:]) + "/" + str(closest_mass)
        for coupling in lambdastring
        if coupling[3] == "3"
    ]
    path_single_tautau = [
        efficiency_prefix + "s/" + str(coupling[2:]) + "/" + str(closest_mass)
        for coupling in lambdastring
        if coupling[3] == "3"
    ]
    path_tchannel_tautau = [
        efficiency_prefix + "t/" + str(coupling[2:]) + "/" + str(closest_mass)
        for coupling in lambdastring
        if coupling[3] == "3"
    ]
    path_pureqcd_tautau = [
        efficiency_prefix + "q/" + str(coupling[2:]) + "/" + str(closest_mass)
        for coupling in lambdastring
        if coupling[3] == "3"
    ]

    ee_path_t_ct = []
    mumu_path_t_ct = []
    tautau_path_t_ct = []
    for i in range(num_lam):
        for j in range(i + 1, num_lam):
            if lambdastring[i][3] == lambdastring[j][3]:
                if lambdastring[i][3] == "1":
                    ee_path_t_ct.append(
                        t_ct_prefix
                        + str(lambdastring[i][2:])
                        + "_"
                        + str(lambdastring[j][2:])
                    )
                elif lambdastring[i][3] == "2":
                    mumu_path_t_ct.append(
                        t_ct_prefix
                        + str(lambdastring[i][2:])
                        + "_"
                        + str(lambdastring[j][2:])
                    )
                elif lambdastring[i][3] == "3":
                    tautau_path_t_ct.append(
                        t_ct_prefix
                        + str(lambdastring[i][2:])
                        + "_"
                        + str(lambdastring[j][2:])
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
                for j in tagnames
            ]
            for i in range(len(path_pureqcd_tautau))
        ],
        [
            [
                pd.read_csv(path_pair_tautau[i] + j, header=[0]).to_numpy()[:, 2]
                for j in tagnames
            ]
            for i in range(len(path_pureqcd_tautau))
        ],
        [
            [
                pd.read_csv(path_single_tautau[i] + j, header=[0]).to_numpy()[:, 2]
                for j in tagnames
            ]
            for i in range(len(path_pureqcd_tautau))
        ],
        [
            [
                pd.read_csv(path_interference_tautau[i] + j, header=[0]).to_numpy()[
                    :, 2
                ]
                for j in tagnames
            ]
            for i in range(len(path_pureqcd_tautau))
        ],
        [
            [
                pd.read_csv(path_tchannel_tautau[i] + j, header=[0]).to_numpy()[:, 2]
                for j in tagnames
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
            for i in tagnames
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
