from scipy.interpolate import interp1d

from utilities.constants import (
    interpolation_type,
    data_mass_list,
    df_pureqcd,
    df_pair,
    df_single,
    df_interference,
    df_tchannel,
    double_coupling_data_tchannel,
)


def interpolate_cs_func(df, ls):
    return lambda mass: [
        interp1d(data_mass_list, df[coupling][:5], kind=interpolation_type)([mass])[0]
        for coupling in ls
    ]


def interpolate_cs_ct_func(df):
    """
    Interpolating cross-section of t-channel's cross terms
    """
    return lambda mass: [
        interp1d(data_mass_list, df[ij], kind=interpolation_type)([mass])[0]
        for ij in range(len(df))
    ]


def get_cs(mass, lambdastring, num_lam):
    """
    Get cross sections from data files
    """
    cs_q = interpolate_cs_func(df_pureqcd, lambdastring)
    cs_p = interpolate_cs_func(df_pair, lambdastring)
    cs_s = interpolate_cs_func(df_single, lambdastring)
    cs_i = interpolate_cs_func(df_interference, lambdastring)
    cs_t = interpolate_cs_func(df_tchannel, lambdastring)
    cs_l = [cs_q(mass), cs_p(mass), cs_s(mass), cs_i(mass), cs_t(mass)]
    #
    ee_cs = []
    mumu_cs = []
    tautau_cs = []
    for process in cs_l:
        ee_temp = []
        mumu_temp = []
        tautau_temp = []
        for lamda, cs in zip(lambdastring, process):
            if lamda[3] == "1":
                ee_temp.append(cs)
            elif lamda[3] == "2":
                mumu_temp.append(cs)
            elif lamda[3] == "3":
                tautau_temp.append(cs)
        ee_cs.append(ee_temp)
        mumu_cs.append(mumu_temp)
        tautau_cs.append(tautau_temp)
    # cross terms:
    ee_t_ct = [
        double_coupling_data_tchannel[f"{lambdastring[i]}_{lambdastring[j]}"]
        for i in range(num_lam)
        for j in range(i + 1, num_lam)
        if lambdastring[i][3] == lambdastring[j][3] and lambdastring[i][3] == "1"
    ]
    mumu_t_ct = [
        double_coupling_data_tchannel[f"{lambdastring[i]}_{lambdastring[j]}"]
        for i in range(num_lam)
        for j in range(i + 1, num_lam)
        if lambdastring[i][3] == lambdastring[j][3] and lambdastring[i][3] == "2"
    ]
    tautau_t_ct = [
        double_coupling_data_tchannel[f"{lambdastring[i]}_{lambdastring[j]}"]
        for i in range(num_lam)
        for j in range(i + 1, num_lam)
        if lambdastring[i][3] == lambdastring[j][3] and lambdastring[i][3] == "3"
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
            if lambdastring[i][3] == lambdastring[j][3]:
                if lambdastring[i][3] == "1":
                    cs_ee_t_ct[ee_cntr] = (
                        cs_ee_t_ct_temp[ee_cntr] - cs_l[4][i] - cs_l[4][j]
                    )
                    ee_cntr += 1
                elif lambdastring[i][3] == "2":
                    cs_mumu_t_ct[mumu_cntr] = (
                        cs_mumu_t_ct_temp[mumu_cntr] - cs_l[4][i] - cs_l[4][j]
                    )
                    mumu_cntr += 1
                elif lambdastring[i][3] == "3":
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
