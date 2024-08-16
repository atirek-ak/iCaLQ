from scipy.interpolate import interp1d
from scipy.interpolate import InterpolatedUnivariateSpline
import numpy as np

from utilities.constants import (
    interpolation_type,
    data_mass_list,
    get_df_pureqcd,
    get_df_pair,
    get_df_single,
    get_df_interference,
    get_df_tchannel,
    get_double_coupling_data_tchannel,
)


def interpolate_cs_func(df, ls):
    return lambda mass: [
        InterpolatedUnivariateSpline(data_mass_list, df[coupling][:11], k=1)([mass])[0]
        for coupling in ls
    ]


# def interpolate_cs_func(df, ls, mass, interpolation_type='linear'):
#     # Find the minimum values to shift data (adding a small value to avoid log10 of zero)
#     min_shift = abs(np.min(df[ls].values.flatten())) + 1 if np.min(df[ls].values.flatten()) <= 0 else 0

#     # Shift and log-transform the data mass list and df values
#     shifted_mass_list = np.array(data_mass_list) + min_shift
#     log_data_mass_list = np.log10(shifted_mass_list)
    
#     interpolated_values = []
#     for coupling in ls:
#         shifted_y = df[coupling][:9] + min_shift
#         log_y = np.log10(shifted_y)
#         interp_func = interp1d(log_data_mass_list, log_y, kind=interpolation_type)
#         interpolated_log_y = interp_func(np.log10(mass + min_shift))
#         interpolated_y = 10**interpolated_log_y - min_shift
#         interpolated_values.append(interpolated_y)
    
#     return interpolated_values


def interpolate_cs_ct_func(df):
    """
    Interpolating cross-section of t-channel's cross terms
    """
    return lambda mass: [
        interp1d(data_mass_list, df[ij][:11], kind=interpolation_type)([mass])[0]
        for ij in range(len(df))
    ]


def get_cs(mass, lambdastring, num_lam, leptoquark_model):
    """
    Get cross sections from data files
    """
    cs_q = interpolate_cs_func(get_df_pureqcd(leptoquark_model), lambdastring)
    cs_p = interpolate_cs_func(get_df_pair(leptoquark_model), lambdastring)
    cs_s = interpolate_cs_func(get_df_single(leptoquark_model), lambdastring)
    cs_i = interpolate_cs_func(get_df_interference(leptoquark_model), lambdastring)
    cs_t = interpolate_cs_func(get_df_tchannel(leptoquark_model), lambdastring)
    cs_l = []
    cs_l.append(cs_q(mass))
    cs_l.append(cs_p(mass))
    cs_l.append(cs_s(mass))
    cs_l.append(cs_i(mass))
    cs_l.append(cs_t(mass))
    # cs_l = [, cs_p(mass), cs_s(mass), cs_i(mass), cs_t(mass)]
    # cs_q = interpolate_cs_func(get_df_pureqcd(leptoquark_model), lambdastring, mass)
    # cs_p = interpolate_cs_func(get_df_pair(leptoquark_model), lambdastring, mass)
    # cs_s = interpolate_cs_func(get_df_single(leptoquark_model), lambdastring, mass)
    # cs_i = interpolate_cs_func(get_df_interference(leptoquark_model), lambdastring, mass)
    # cs_t = interpolate_cs_func(get_df_tchannel(leptoquark_model), lambdastring, mass)
    # cs_l = [cs_q, cs_p, cs_s, cs_i, cs_t]
    
    ee_cs = []
    mumu_cs = []
    tautau_cs = []
    for process in cs_l:
        ee_temp = []
        mumu_temp = []
        tautau_temp = []
        for lamda, cs in zip(lambdastring, process):
            if lamda[8] == "1":
                ee_temp.append(cs)
            elif lamda[8] == "2":
                mumu_temp.append(cs)
            elif lamda[8] == "3":
                tautau_temp.append(cs)
        ee_cs.append(ee_temp)
        mumu_cs.append(mumu_temp)
        tautau_cs.append(tautau_temp)
    # cross terms:
    double_coupling_data_tchannel = get_double_coupling_data_tchannel(leptoquark_model)
    ee_t_ct = [
        double_coupling_data_tchannel[f"{lambdastring[i]}_{lambdastring[j]}"]
        for i in range(num_lam)
        for j in range(i + 1, num_lam)
        if lambdastring[i][8] == lambdastring[j][8] and lambdastring[i][8] == "1"
    ]
    mumu_t_ct = [
        double_coupling_data_tchannel[f"{lambdastring[i]}_{lambdastring[j]}"]
        for i in range(num_lam)
        for j in range(i + 1, num_lam)
        if lambdastring[i][8] == lambdastring[j][8] and lambdastring[i][8] == "2"
    ]
    tautau_t_ct = [
        double_coupling_data_tchannel[f"{lambdastring[i]}_{lambdastring[j]}"]
        for i in range(num_lam)
        for j in range(i + 1, num_lam)
        if lambdastring[i][8] == lambdastring[j][8] and lambdastring[i][8] == "3"
    ]
    cs_ee_t_ct_func = interpolate_cs_ct_func(ee_t_ct)
    cs_ee_t_ct_temp = cs_ee_t_ct_func(mass)
    cs_mumu_t_ct_func = interpolate_cs_ct_func(mumu_t_ct)
    cs_mumu_t_ct_temp = cs_mumu_t_ct_func(mass)
    cs_tautau_t_ct_func = interpolate_cs_ct_func(tautau_t_ct)
    cs_tautau_t_ct_temp = cs_tautau_t_ct_func(mass)
    #
    ee_cntr = 0
    cs_ee_t_ct = cs_ee_t_ct_temp[:]
    mumu_cntr = 0
    cs_mumu_t_ct = cs_mumu_t_ct_temp[:]
    tautau_cntr = 0
    cs_tautau_t_ct = cs_tautau_t_ct_temp[:]
    for i in range(num_lam):
        for j in range(i + 1, num_lam):
            if lambdastring[i][8] == lambdastring[j][8]:
                if lambdastring[i][8] == "1":
                    cs_ee_t_ct[ee_cntr] = (
                        cs_ee_t_ct_temp[ee_cntr] - cs_l[4][i] - cs_l[4][j]
                    )
                    ee_cntr += 1
                elif lambdastring[i][8] == "2":
                    cs_mumu_t_ct[mumu_cntr] = (
                        cs_mumu_t_ct_temp[mumu_cntr] - cs_l[4][i] - cs_l[4][j]
                    )
                    mumu_cntr += 1
                elif lambdastring[i][8] == "3":
                    cs_tautau_t_ct[tautau_cntr] = (
                        cs_tautau_t_ct_temp[tautau_cntr] - cs_l[4][i] - cs_l[4][j]
                    )
                    tautau_cntr += 1
    return [
        ee_cs,
        mumu_cs,
        tautau_cs,
        cs_ee_t_ct,
        cs_mumu_t_ct,
        cs_tautau_t_ct,
        cs_ee_t_ct_temp,
        cs_mumu_t_ct_temp,
        cs_tautau_t_ct_temp,
    ]
