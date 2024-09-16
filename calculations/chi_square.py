import sympy as sym
from sympy.utilities.iterables import flatten

from utilities.constants import (
    NSM,
    ND,
    k_factor_pair_production,
    k_factor_pureqcd,
    k_factor_single_production,
    k_factor_t_channel,
    k_factor_interference
)


def get_chisq_ind(
    tag, mass, all_lam, cs_list, eff_list, b_frac, ignorePairSingle, margin, leptoquark_model, luminosity,
):
    """
    Calculate a partial polynomial
    """
    [ee_lam, mumu_lam, tautau_lam] = all_lam
    [
        ee_eff_l,
        mumu_eff_l,
        tautau_eff_l,
        ee_eff_t_ct,
        mumu_eff_t_ct,
        tautau_eff_t_ct,
        ee_lambdas_len,
        mumu_lambdas_len,
        tautau_lambdas_len,
    ] = eff_list
    [
        ee_cs,
        mumu_cs,
        tautau_cs,
        cs_ee_t_ct,
        cs_mumu_t_ct,
        cs_tautau_t_ct,
        _,
        _,
        _,
    ] = cs_list
    if (
        (tag < 4 and len(tautau_eff_l[0]) == 0)
        or (tag == 4 and len(ee_eff_l[0]) == 0)
        or (tag == 5 and len(mumu_eff_l[0]) == 0)
    ):
        return 0
    if tag < 4:
        num_bin = len(tautau_eff_l[0][0][tag])
    elif tag == 4:
        num_bin = len(ee_eff_l[0][0][0])
    elif tag == 5:
        num_bin = len(mumu_eff_l[0][0][0])
    nq = [0.0] * num_bin
    np = [0.0] * num_bin
    ns = [0.0] * num_bin
    ni = [0.0] * num_bin
    nt = [0.0] * num_bin
    ntc = [0.0] * num_bin
    nsm = NSM[tag]
    # nsm = [x*luminosity/139000 for x in nsm]
    nd = ND[tag]
    # nd = [x*luminosity/139000 for x in nd]
    denominator = [
        nd[bin_no] + margin * margin * nd[bin_no] ** 2 for bin_no in range(num_bin)
    ]
    if tag < 4:
        nq = [
            nq[bin_no]
            + tautau_cs[0][0] * (k_factor_pureqcd if leptoquark_model == "S1" else 1.0)
            * tautau_eff_l[0][0][tag][bin_no]
            * b_frac**2
            * luminosity
            for bin_no in range(num_bin)
        ] if mass <=6000 else nq
        for i in range(tautau_lambdas_len):
            np = [
                np[bin_no]
                + tautau_cs[1][i] * (k_factor_pair_production if leptoquark_model == "S1" else 1.0)
                * tautau_eff_l[1][i][tag][bin_no]
                * tautau_lam[i] ** 4
                * b_frac**2
                * luminosity
                for bin_no in range(num_bin)
            ] if mass <=6000 else np
            ns = [
                ns[bin_no]
                + tautau_cs[2][i] * (k_factor_single_production if leptoquark_model == "S1" else 1.0)
                * tautau_eff_l[2][i][tag][bin_no]
                * tautau_lam[i] ** 2
                * b_frac
                * luminosity
                for bin_no in range(num_bin)
            ]
            ni = [
                ni[bin_no]
                + tautau_cs[3][i] * (k_factor_interference if leptoquark_model == "S1" else 1.0)
                * tautau_eff_l[3][i][tag][bin_no]
                * tautau_lam[i] ** 2
                * luminosity
                for bin_no in range(num_bin)
            ]
            nt = [
                nt[bin_no] * (k_factor_t_channel if leptoquark_model == "S1" else 1.0)
                + tautau_cs[4][i]
                * tautau_eff_l[4][i][tag][bin_no]
                * tautau_lam[i] ** 4
                * luminosity
                for bin_no in range(num_bin)
            ]
        ntc_cntr = 0
        for i in range(tautau_lambdas_len):
            for j in range(i + 1, tautau_lambdas_len):
                "use cross-terms"
                ntc = [
                    ntc[bin_no]
                    + cs_tautau_t_ct[ntc_cntr] * (k_factor_t_channel if leptoquark_model == "S1" else 1.0)
                    * tautau_eff_t_ct[ntc_cntr][tag][bin_no]
                    * tautau_lam[i] ** 2
                    * tautau_lam[j] ** 2
                    * luminosity
                    for bin_no in range(num_bin)
                ]
                ntc_cntr += 1
    elif tag == 4:
        nq = [
            nq[bin_no]
            + ee_cs[0][0] * (k_factor_pureqcd if leptoquark_model == "S1" else 1.0) * ee_eff_l[0][0][0][bin_no] * b_frac**2 * luminosity
            for bin_no in range(num_bin)
        ] if mass <=6000 else nq
        for i in range(ee_lambdas_len):
            np = [
                np[bin_no]
                + ee_cs[1][i] * (k_factor_pair_production if leptoquark_model == "S1" else 1.0)
                * ee_eff_l[1][i][0][bin_no]
                * ee_lam[i] ** 4
                * b_frac**2
                * luminosity
                for bin_no in range(num_bin)
            ] if mass <=6000 else np
            ns = [
                ns[bin_no]
                + ee_cs[2][i] * (k_factor_single_production if leptoquark_model == "S1" else 1.0)
                * ee_eff_l[2][i][0][bin_no]
                * ee_lam[i] ** 2
                * b_frac
                * luminosity
                for bin_no in range(num_bin)
            ]
            ni = [
                ni[bin_no]
                + ee_cs[3][i] * (k_factor_interference if leptoquark_model == "S1" else 1.0)
                * ee_eff_l[3][i][0][bin_no]
                * ee_lam[i] ** 2
                * luminosity
                for bin_no in range(num_bin)
            ]
            nt = [
                nt[bin_no]
                + ee_cs[4][i] * (k_factor_t_channel if leptoquark_model == "S1" else 1.0)
                * ee_eff_l[4][i][0][bin_no]
                * ee_lam[i] ** 4
                * luminosity
                for bin_no in range(num_bin)
            ]
        ntc_cntr = 0
        for i in range(ee_lambdas_len):
            for j in range(i + 1, ee_lambdas_len):
                "use cross-terms"
                ntc = [
                    ntc[bin_no]
                    + cs_ee_t_ct[ntc_cntr] * (k_factor_t_channel if leptoquark_model == "S1" else 1.0)
                    * ee_eff_t_ct[ntc_cntr][0][bin_no]
                    * ee_lam[i] ** 2
                    * ee_lam[j] ** 2
                    * luminosity
                    for bin_no in range(num_bin)
                ]
                ntc_cntr += 1
    elif tag == 5:
        nq = [
            nq[bin_no]
            + mumu_cs[0][0] * (k_factor_pureqcd if leptoquark_model == "S1" else 1.0)
            * mumu_eff_l[0][0][0][bin_no]
            * b_frac**2
            * luminosity
            for bin_no in range(num_bin)
        ] if mass <=6000 else nq
        for i in range(mumu_lambdas_len):
            np = [
                np[bin_no]
                + mumu_cs[1][i] * (k_factor_pair_production if leptoquark_model == "S1" else 1.0)
                * mumu_eff_l[1][i][0][bin_no]
                * mumu_lam[i] ** 4
                * b_frac**2
                * luminosity
                for bin_no in range(num_bin)
            ] if mass <=6000 else np
            ns = [
                ns[bin_no]
                + mumu_cs[2][i] * (k_factor_single_production if leptoquark_model == "S1" else 1.0)
                * mumu_eff_l[2][i][0][bin_no]
                * mumu_lam[i] ** 2
                * b_frac
                * luminosity
                for bin_no in range(num_bin)
            ]
            ni = [
                ni[bin_no]
                + mumu_cs[3][i] * (k_factor_interference if leptoquark_model == "S1" else 1.0)
                * mumu_eff_l[3][i][0][bin_no]
                * mumu_lam[i] ** 2
                * luminosity
                for bin_no in range(num_bin)
            ]
            nt = [
                nt[bin_no]
                + mumu_cs[4][i] * (k_factor_t_channel if leptoquark_model == "S1" else 1.0)
                * mumu_eff_l[4][i][0][bin_no]
                * mumu_lam[i] ** 4
                * luminosity
                for bin_no in range(num_bin)
            ]
        ntc_cntr = 0
        for i in range(mumu_lambdas_len):
            for j in range(i + 1, mumu_lambdas_len):
                "use cross-terms"
                ntc = [
                    ntc[bin_no]
                    + cs_mumu_t_ct[ntc_cntr] * (k_factor_t_channel if leptoquark_model == "S1" else 1.0)
                    * mumu_eff_t_ct[ntc_cntr][0][bin_no]
                    * mumu_lam[i] ** 2
                    * mumu_lam[j] ** 2
                    * luminosity
                    for bin_no in range(num_bin)
                ]
                ntc_cntr += 1
    chi_ind = 0.0
    for bin_no in range(num_bin):
        if ignorePairSingle:
            chi_ind += (
                (
                    ni[bin_no]
                    + nt[bin_no]
                    + ntc[bin_no]
                    + nsm[bin_no]
                    - nd[bin_no]
                )
                ** 2
            ) / denominator[bin_no]
        else:
            chi_ind += (
                (
                    nq[bin_no]
                    + np[bin_no]
                    + ns[bin_no]
                    + ni[bin_no]
                    + nt[bin_no]
                    + ntc[bin_no]
                    + nsm[bin_no]
                    - nd[bin_no]
                )
                ** 2
            ) / denominator[bin_no]
            # chi_ind += nq[bin_no]+ np[bin_no]+ ns[bin_no]+ ni[bin_no]+ nt[bin_no]+ ntc[bin_no]
              
    return sym.Add(chi_ind)


def get_chi_square_symb(
    mass, all_lam, cs_list, eff_list, br_frac, ignorePairSingle, margin, leptoquark_model, luminosity
):
    """
    Compute the polynomial by getting partial polynomials
    """
    ee_chi = 0
    mumu_chi = 0
    hhbt_chi = 0
    hhbv_chi = 0
    lhbt_chi = 0
    lhbv_chi = 0
    if len(all_lam[0]) > 0:
        ee_chi = sym.simplify(
            get_chisq_ind(
                4,
                mass,
                all_lam,
                cs_list,
                eff_list,
                br_frac[0],
                ignorePairSingle,
                margin,
                leptoquark_model,
                luminosity,
            )
        )
        print("Dielectron contributions computed.")
    if len(all_lam[1]) > 0:
        mumu_chi = sym.simplify(
            get_chisq_ind(
                5,
                mass,
                all_lam,
                cs_list,
                eff_list,
                br_frac[1],
                ignorePairSingle,
                margin,
                leptoquark_model,
                luminosity,
            )
        )
        print("Dimuon contributions computed.")
    if len(all_lam[2]) > 0:
        hhbt_chi = sym.simplify(
            get_chisq_ind(
                0,
                mass,
                all_lam,
                cs_list,
                eff_list,
                br_frac[2],
                ignorePairSingle,
                margin,
                leptoquark_model,
                luminosity,
            )
        )
        print("Ditau: HHbT contributions computed.")
        hhbv_chi = sym.simplify(
            get_chisq_ind(
                1,
                mass,
                all_lam,
                cs_list,
                eff_list,
                br_frac[2],
                ignorePairSingle,
                margin,
                leptoquark_model,
                luminosity,
            )
        )
        print("Ditau: HHbV contributions computed.")
        lhbt_chi = sym.simplify(
            get_chisq_ind(
                2,
                mass,
                all_lam,
                cs_list,
                eff_list,
                br_frac[2],
                ignorePairSingle,
                margin,
                leptoquark_model,
                luminosity,
            )
        )
        print("Ditau: LHbT contributions computed.")
        lhbv_chi = sym.simplify(
            get_chisq_ind(
                3,
                mass,
                all_lam,
                cs_list,
                eff_list,
                br_frac[2],
                ignorePairSingle,
                margin,
                leptoquark_model,
                luminosity,
            )
        )
        print("Ditau: LHbV contributions computed.")
    return sym.Add(ee_chi, mumu_chi, hhbt_chi, hhbv_chi, lhbt_chi, lhbv_chi)

def add_plot_data(chisq_min, lam_vals, numpy_chisq, mass, lambdastring):
    for lam_val in lam_vals:
        temp = [float(x) for x in lam_val]
        if not any(temp):
            temp = [0.00000001] * len(lam_val)
        chisq_given_vals = numpy_chisq(*flatten(temp))
        # file_path = f"plots/data/{lambdastring[0]}.csv"
        file_path = f"plots/data/{lambdastring[0]}_{lambdastring[1]}.csv"
        if round(float(chisq_given_vals),5) - round(float(chisq_min),5) <=4 :
            with open(file_path, "a") as f:
                # f.write(f"{mass},{round(float(chisq_min),5)},{round(float(chisq_given_vals),5)},{round(float(lam_val[0]),3)}\n")
                f.write(f"{mass},{round(float(chisq_min),5)},{round(float(chisq_given_vals),5)},{round(float(lam_val[0]),3)},{round(float(lam_val[1]),3)}\n")



def get_delta_chisq(
    lam_vals, lam_vals_original, chisq_min, numpy_chisq, num_lam, chi_sq_limits, mass, lambdastring
):
    """
    Use the lambdified function (numpy_chisq) to calculate chi square for the given query input
    """
    validity_list = []
    delta_chisq = []
    add_plot_data(chisq_min, lam_vals, numpy_chisq, mass, lambdastring)
    for lam_val, lam_val_copy in zip(lam_vals, lam_vals_original):
        temp = [float(x) for x in lam_val]
        if not any(temp):
            temp = [0.00000001] * len(lam_val)
        chisq_given_vals = numpy_chisq(*flatten(temp))
        delta_chisq.append(chisq_given_vals - chisq_min)
        if chisq_given_vals - chisq_min <= chi_sq_limits[num_lam - 1]:
            validity_list.append("Yes")
        else:
            validity_list.append("No")
    return delta_chisq, validity_list
