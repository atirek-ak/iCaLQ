import pandas as pd
from copy import deepcopy
from scipy.interpolate import interp1d
from scipy.interpolate import InterpolatedUnivariateSpline
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from utilities.constants import get_efficiency_prefix, get_t_ct_prefix, tagnames, data_mass_list

def read_and_interpolate_csv(path_list, mass, data_mass_list):
    if any(any(inner_list) for inner_list in path_list) == False:
        return path_list
    interpolated_values = []
    print(path_list)
    for path in path_list:
        for index in range(len(path)):
            # Read data from CSV files for each mass in data_mass_list
            values = []
            for m in data_mass_list:
                csv_path = f"{path[index]}/{int(m)}.csv"
                data = pd.read_csv(csv_path, header=[0]).to_numpy()[:, 2]
                values.append(data)

            # Convert values to a numpy array for interpolation
            values = np.array(values)
            # print(values)
            # Perform interpolation for each column
            # interp_func = InterpolatedUnivariateSpline(data_mass_list, values, k=1)
            splines = [InterpolatedUnivariateSpline(data_mass_list, values[:, i], k=1) for i in range(values.shape[1])]
            interpolated_values.append([np.array([spline(mass) for spline in splines])])
    
    return [interpolated_values]


def read_and_interpolate_csv_tautau(path_list, mass, data_mass_list):
    if any(any(inner_list) for inner_list in path_list) == False:
        return path_list
    interpolated_values = []
    for path in path_list:
        # Read data from CSV files for each mass in data_mass_list
        path_values = []
        for tag_name in tagnames:
            values = []
            for m in data_mass_list:
                csv_path = f"{path[0]}{int(m)}{tag_name}"
                data = pd.read_csv(csv_path, header=[0]).to_numpy()[:, 2]
                values.append(data)
            # tag_values.append(values)
            # Convert values to a numpy array for interpolation
            values = np.array(values)

            # polynomial interpolation
            # poly_coeffs = np.polyfit(data_mass_list, values, deg=len(data_mass_list)-1)
            # poly_interp_func = np.poly1d(poly_coeffs)
            # path_values.append(poly_interp_func(mass))
            
            # Perform interpolation for each column
            splines = [InterpolatedUnivariateSpline(data_mass_list, values[:, i], k=1) for i in range(values.shape[1])]
            # if tag_name == "/LHbV.csv":
            #     counter = 0
            #     for i in range(values.shape[1]):
            #         spline = InterpolatedUnivariateSpline(data_mass_list, values[:, i], k=1)
            #         plt.clf()
            #         plt.plot(data_mass_list, values[:, i], 'o', color='brown')
            #         plt.plot(mass, spline(mass), 'o', color='blue')
            #         # reg = LinearRegression().fit(data_mass_list, values[:, i])
            #         # line_x = np.linspace(data_mass_list.min(), data_mass_list.max(), 100).reshape(-1, 1)
            #         # line_y = reg.predict(line_x)

            #         # Plotting the points
            #         # plt.scatter(data_mass_list, values[:, i], color='blue', label='Points')
            #         # plt.scatter(mass, spline(mass), color='brown', label='Points')

            #         # Plotting the best fit line
            #         # plt.plot(line_x, line_y, color='red', label='Best fit line')
            #         plt.xlabel('Leptoquark mass')
            #         plt.ylabel('Coupling value')
            #         plt.title('Single coupling values plot')
            #         # plt.show()
            #         plt.savefig(f"plots/{counter}.png")
            #         counter += 1



            # interp_func = InterpolatedUnivariateSpline(data_mass_list, values, k=1)
            # print("######")
            # print(np.array([spline(mass) for spline in splines]))
            # print("######")
            path_values.append(np.array([spline(mass) for spline in splines]))
        interpolated_values.append([path_values])
    
    return interpolated_values

def get_efficiencies(mass, closest_mass, lambdastring, num_lam, cs_list, leptoquark_model):
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
        get_efficiency_prefix(leptoquark_model)
        + "i/"
        + str(coupling[6] + coupling[8] + coupling[4])
        for coupling in lambdastring
        if coupling[8] == "1"
    ]
    path_pair_ee = [
        get_efficiency_prefix(leptoquark_model)
        + "p/"
        + str(coupling[6] + coupling[8] + coupling[4])
        for coupling in lambdastring
        if coupling[8] == "1"
    ]
    path_single_ee = [
        get_efficiency_prefix(leptoquark_model)
        + "s/"
        + str(coupling[6] + coupling[8] + coupling[4])
        for coupling in lambdastring
        if coupling[8] == "1"
    ]
    path_tchannel_ee = [
        get_efficiency_prefix(leptoquark_model)
        + "t/"
        + str(coupling[6] + coupling[8] + coupling[4])
        for coupling in lambdastring
        if coupling[8] == "1"
    ]
    path_pureqcd_ee = [
        get_efficiency_prefix(leptoquark_model)
        + "q/"
        + str(coupling[6] + coupling[8] + coupling[4])
        for coupling in lambdastring
        if coupling[8] == "1"
    ]

    path_interference_mumu = [
        get_efficiency_prefix(leptoquark_model)
        + "i/"
        + str(coupling[6] + coupling[8] + coupling[4])
        for coupling in lambdastring
        if coupling[8] == "2"
]
    path_pair_mumu = [
        get_efficiency_prefix(leptoquark_model)
        + "p/"
        + str(coupling[6] + coupling[8] + coupling[4])
        for coupling in lambdastring
        if coupling[8] == "2"
    ]
    path_single_mumu = [
        get_efficiency_prefix(leptoquark_model)
        + "s/"
        + str(coupling[6] + coupling[8] + coupling[4])
        for coupling in lambdastring
        if coupling[8] == "2"
    ]
    path_tchannel_mumu = [
        get_efficiency_prefix(leptoquark_model)
        + "t/"
        + str(coupling[6] + coupling[8] + coupling[4])
        for coupling in lambdastring
        if coupling[8] == "2"
    ]
    path_pureqcd_mumu = [
        get_efficiency_prefix(leptoquark_model)
        + "q/"
        + str(coupling[6] + coupling[8] + coupling[4])
        for coupling in lambdastring
        if coupling[8] == "2"
    ]

    path_interference_tautau = [
        get_efficiency_prefix(leptoquark_model)
        + "i/"
        + str(coupling[6] + coupling[8] + coupling[4])
        + "/"
        # + str(closest_mass)
        for coupling in lambdastring
        if coupling[8] == "3"
    ]
    path_pair_tautau = [
        get_efficiency_prefix(leptoquark_model)
        + "p/"
        + str(coupling[6] + coupling[8] + coupling[4])
        + "/"
        # + str(closest_mass)
        for coupling in lambdastring
        if coupling[8] == "3"
    ]
    path_single_tautau = [
        get_efficiency_prefix(leptoquark_model)
        + "s/"
        + str(coupling[6] + coupling[8] + coupling[4])
        + "/"
        # + str(closest_mass)
        for coupling in lambdastring
        if coupling[8] == "3"
    ]
    path_tchannel_tautau = [
        get_efficiency_prefix(leptoquark_model)
        + "t/"
        + str(coupling[6] + coupling[8] + coupling[4])
        + "/"
        # + str(closest_mass)
        for coupling in lambdastring
        if coupling[8] == "3"
    ]
    path_pureqcd_tautau = [
        get_efficiency_prefix(leptoquark_model)
        + "q/"
        + str(coupling[6] + coupling[8] + coupling[4])
        + "/"
        # + str(closest_mass)
        for coupling in lambdastring
        if coupling[8] == "3"
    ]

    ee_path_t_ct = []
    mumu_path_t_ct = []
    tautau_path_t_ct = []
    for i in range(num_lam):
        for j in range(i + 1, num_lam):
            if lambdastring[i][8] == lambdastring[j][8]:
                if lambdastring[i][8] == "1":
                    ee_path_t_ct.append(
                        get_t_ct_prefix(leptoquark_model)
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
                        get_t_ct_prefix(leptoquark_model)
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
                        get_t_ct_prefix(leptoquark_model)
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

    ee_eff_paths = [
        path_pureqcd_ee, path_pair_ee, path_single_ee, path_interference_ee, path_tchannel_ee
    ]
    ee_eff_l = read_and_interpolate_csv(ee_eff_paths, mass, data_mass_list)


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
    mumu_eff_paths = [
        path_pureqcd_mumu, path_pair_mumu, path_single_mumu, path_interference_mumu, path_tchannel_mumu
    ]
    
    mumu_eff_l = read_and_interpolate_csv(mumu_eff_paths, mass, data_mass_list)
    print(mumu_eff_l)
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
    # tautau_eff_l = [
    #     [
    #         [
    #             pd.read_csv(path_pureqcd_tautau[i] + j, header=[0]).to_numpy()[:, 2]
    #             for j in tagnames
    #         ]
    #         for i in range(len(path_pureqcd_tautau))
    #     ],
    #     [
    #         [
    #             pd.read_csv(path_pair_tautau[i] + j, header=[0]).to_numpy()[:, 2]
    #             for j in tagnames
    #         ]
    #         for i in range(len(path_pureqcd_tautau))
    #     ],
    #     [
    #         [
    #             pd.read_csv(path_single_tautau[i] + j, header=[0]).to_numpy()[:, 2]
    #             for j in tagnames
    #         ]
    #         for i in range(len(path_pureqcd_tautau))
    #     ],
    #     [
    #         [
    #             pd.read_csv(path_interference_tautau[i] + j, header=[0]).to_numpy()[
    #                 :, 2
    #             ]
    #             for j in tagnames
    #         ]
    #         for i in range(len(path_pureqcd_tautau))
    #     ],
    #     [
    #         [
    #             pd.read_csv(path_tchannel_tautau[i] + j, header=[0]).to_numpy()[:, 2]
    #             for j in tagnames
    #         ]
    #         for i in range(len(path_pureqcd_tautau))
    #     ],
    # ]
    tautau_eff_paths = [
        path_pureqcd_tautau, path_pair_tautau, path_single_tautau, path_interference_tautau, path_tchannel_tautau
    ]

    tautau_eff_l = read_and_interpolate_csv_tautau(tautau_eff_paths, mass, data_mass_list)
    print(tautau_eff_l)

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
