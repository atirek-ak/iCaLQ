import sympy as sym
from sympy.utilities.iterables import flatten

from utilities.constants import (
    NSM,
    ND,
    luminosity_tau,
    luminosity_e_mu,
    chi_sq_limits_2,
)


def get_chisq_ind(
    tag, mass, all_lam, cs_list, eff_list, b_frac, ignorePairSingle, margin
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
        cs_ee_t_ct_temp,
        cs_mumu_t_ct_temp,
        cs_tautau_t_ct_temp,
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
    nd = ND[tag]
    denominator = [
        nd[bin_no] + margin * margin * nd[bin_no] ** 2 for bin_no in range(num_bin)
    ]
    if tag < 4:
        nq = [
            nq[bin_no]
            + tautau_cs[0][0]
            * tautau_eff_l[0][0][tag][bin_no]
            * b_frac**2
            * luminosity_tau
            for bin_no in range(num_bin)
        ]
        for i in range(tautau_lambdas_len):
            np = [
                np[bin_no]
                + tautau_cs[1][i]
                * tautau_eff_l[1][i][tag][bin_no]
                * tautau_lam[i] ** 4
                * b_frac**2
                * luminosity_tau
                for bin_no in range(num_bin)
            ]
            ns = [
                ns[bin_no]
                + tautau_cs[2][i]
                * tautau_eff_l[2][i][tag][bin_no]
                * tautau_lam[i] ** 2
                * b_frac
                * luminosity_tau
                for bin_no in range(num_bin)
            ]
            ni = [
                ni[bin_no]
                + tautau_cs[3][i]
                * tautau_eff_l[3][i][tag][bin_no]
                * tautau_lam[i] ** 2
                * luminosity_tau
                for bin_no in range(num_bin)
            ]
            nt = [
                nt[bin_no]
                + tautau_cs[4][i]
                * tautau_eff_l[4][i][tag][bin_no]
                * tautau_lam[i] ** 4
                * luminosity_tau
                for bin_no in range(num_bin)
            ]
        ntc_cntr = 0
        for i in range(tautau_lambdas_len):
            for j in range(i + 1, tautau_lambdas_len):
                "use cross-terms"
                ntc = [
                    ntc[bin_no]
                    + cs_tautau_t_ct[ntc_cntr]
                    * tautau_eff_t_ct[ntc_cntr][tag][bin_no]
                    * tautau_lam[i] ** 2
                    * tautau_lam[j] ** 2
                    * luminosity_tau
                    for bin_no in range(num_bin)
                ]
                ntc_cntr += 1
    elif tag == 4:
        nq = [
            nq[bin_no]
            + ee_cs[0][0] * ee_eff_l[0][0][0][bin_no] * b_frac**2 * luminosity_e_mu
            for bin_no in range(num_bin)
        ]
        for i in range(ee_lambdas_len):
            np = [
                np[bin_no]
                + ee_cs[1][i]
                * ee_eff_l[1][i][0][bin_no]
                * ee_lam[i] ** 4
                * b_frac**2
                * luminosity_e_mu
                for bin_no in range(num_bin)
            ]
            ns = [
                ns[bin_no]
                + ee_cs[2][i]
                * ee_eff_l[2][i][0][bin_no]
                * ee_lam[i] ** 2
                * b_frac
                * luminosity_e_mu
                for bin_no in range(num_bin)
            ]
            ni = [
                ni[bin_no]
                + ee_cs[3][i]
                * ee_eff_l[3][i][0][bin_no]
                * ee_lam[i] ** 2
                * luminosity_e_mu
                for bin_no in range(num_bin)
            ]
            nt = [
                nt[bin_no]
                + ee_cs[4][i]
                * ee_eff_l[4][i][0][bin_no]
                * ee_lam[i] ** 4
                * luminosity_e_mu
                for bin_no in range(num_bin)
            ]
        ntc_cntr = 0
        for i in range(ee_lambdas_len):
            for j in range(i + 1, ee_lambdas_len):
                "use cross-terms"
                ntc = [
                    ntc[bin_no]
                    + cs_ee_t_ct[ntc_cntr]
                    * ee_eff_t_ct[ntc_cntr][0][bin_no]
                    * ee_lam[i] ** 2
                    * ee_lam[j] ** 2
                    * luminosity_e_mu
                    for bin_no in range(num_bin)
                ]
                ntc_cntr += 1
    elif tag == 5:
        nq = [
            nq[bin_no]
            + mumu_cs[0][0]
            * mumu_eff_l[0][0][0][bin_no]
            * b_frac**2
            * luminosity_e_mu
            for bin_no in range(num_bin)
        ]
        for i in range(mumu_lambdas_len):
            np = [
                np[bin_no]
                + mumu_cs[1][i]
                * mumu_eff_l[1][i][0][bin_no]
                * mumu_lam[i] ** 4
                * b_frac**2
                * luminosity_e_mu
                for bin_no in range(num_bin)
            ]
            ns = [
                ns[bin_no]
                + mumu_cs[2][i]
                * mumu_eff_l[2][i][0][bin_no]
                * mumu_lam[i] ** 2
                * b_frac
                * luminosity_e_mu
                for bin_no in range(num_bin)
            ]
            ni = [
                ni[bin_no]
                + mumu_cs[3][i]
                * mumu_eff_l[3][i][0][bin_no]
                * mumu_lam[i] ** 2
                * luminosity_e_mu
                for bin_no in range(num_bin)
            ]
            nt = [
                nt[bin_no]
                + mumu_cs[4][i]
                * mumu_eff_l[4][i][0][bin_no]
                * mumu_lam[i] ** 4
                * luminosity_e_mu
                for bin_no in range(num_bin)
            ]
        ntc_cntr = 0
        for i in range(mumu_lambdas_len):
            for j in range(i + 1, mumu_lambdas_len):
                "use cross-terms"
                ntc = [
                    ntc[bin_no]
                    + cs_mumu_t_ct[ntc_cntr]
                    * mumu_eff_t_ct[ntc_cntr][0][bin_no]
                    * mumu_lam[i] ** 2
                    * mumu_lam[j] ** 2
                    * luminosity_e_mu
                    for bin_no in range(num_bin)
                ]
                ntc_cntr += 1
    chi_ind = 0.0
    for bin_no in range(num_bin):
        if ignorePairSingle:
            chi_ind += (
                (
                    nq[bin_no]
                    + ni[bin_no]
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
    chi_sq_tag = sym.Add(chi_ind)
    return chi_sq_tag


def get_chi_square_symb(
    mass, all_lam, cs_list, eff_list, br_frac, ignorePairSingle, margin
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
            )
        )
        print("Ditau: LHbV contributions computed.")
    return sym.Add(ee_chi, mumu_chi, hhbt_chi, hhbv_chi, lhbt_chi, lhbv_chi)


def get_delta_chisq(
    lam_vals, lam_vals_original, chisq_min, numpy_chisq, num_lam, chi_sq_limits
):
    """
    Use the lambdified function (numpy_chisq) to calculate chi square for the given query input
    """
    validity_list = []
    delta_chisq = []
    for lam_val, lam_val_copy in zip(lam_vals, lam_vals_original):
        temp = [float(x) for x in lam_val]
        all_zeroes = True
        for x in temp:
            if x:
                all_zeroes = False
                break
        if all_zeroes:
            temp = [0.00000001] * len(lam_val)
        chisq_given_vals = numpy_chisq(*flatten(temp))
        delta_chisq.append(chisq_given_vals - chisq_min)
        if chisq_given_vals - chisq_min <= chi_sq_limits[num_lam - 1]:
            validity_list.append("Yes")
        else:
            validity_list.append("No")
    return delta_chisq, validity_list
