from scipy.interpolate import interp1d

from utilities.data_classes import LeptoquarkParameters, ProcessCrossSections, ParticleCrossSections, CrossTermsCrossSections
from utilities.constants import (
    interpolation_type,
    data_mass_list,
    get_df_pureqcd,
    get_df_pair_production,
    get_df_single_production,
    get_df_interference,
    get_df_tchannel,
    get_cross_terms_data_tchannel,
)


def interpolate_cross_section(df, couplings):
    """
    Returns a function to interpolate cross-section for masses whose cross-sections are not generated
    """
    return lambda mass: [
        interp1d(data_mass_list, df[coupling][:len(data_mass_list)], kind=interpolation_type)([mass])[0]
        for coupling in couplings
    ]


def interpolate_cross_section_cross_terms(df):
    """
    Interpolating cross-section of t-channel's cross terms
    """
    return lambda mass: [
        interp1d(data_mass_list, df[i][:len(data_mass_list)], kind=interpolation_type)([mass])[0]
        for i in range(len(df))
    ]


def get_cross_sections(leptoquark_parameters: LeptoquarkParameters):
    """
    Get cross sections from data files
    """
    # initialse particle cross section objects
    electron_electron_cross_section = ParticleCrossSections()
    muon_muon_cross_section = ParticleCrossSections()
    tau_tau_cross_section = ParticleCrossSections()

    # single coupling
    # read interpolated cross-sections dataframes
    cross_section_pureqcd_interpolation_function = interpolate_cross_section(get_df_pureqcd(leptoquark_parameters.leptoquark_model), leptoquark_parameters.sorted_couplings)
    cross_sections_pureqcd = cross_section_pureqcd_interpolation_function(leptoquark_parameters.leptoquark_mass) # list of floats in sorted couplings order
    cross_section_pair_production_interpolation_function = interpolate_cross_section(get_df_pair_production(leptoquark_parameters.leptoquark_model), leptoquark_parameters.sorted_couplings)
    cross_sections_pair_production = cross_section_pair_production_interpolation_function(leptoquark_parameters.leptoquark_mass) # list of floats in sorted couplings order
    cross_section_single_production_interpolation_function = interpolate_cross_section(get_df_single_production(leptoquark_parameters.leptoquark_model), leptoquark_parameters.sorted_couplings)
    cross_sections_single_production = cross_section_single_production_interpolation_function(leptoquark_parameters.leptoquark_mass) # list of floats in sorted couplings order
    cross_section_interference_interpolation_function = interpolate_cross_section(get_df_interference(leptoquark_parameters.leptoquark_model), leptoquark_parameters.sorted_couplings)
    cross_sections_interference = cross_section_interference_interpolation_function(leptoquark_parameters.leptoquark_mass) # list of floats in sorted couplings order
    cross_section_tchannel_interpolation_function = interpolate_cross_section(get_df_tchannel(leptoquark_parameters.leptoquark_model), leptoquark_parameters.sorted_couplings)
    cross_sections_tchannel = cross_section_tchannel_interpolation_function(leptoquark_parameters.leptoquark_mass) # list of floats in sorted couplings order

    # categorise them by particle and assign to ParticleCrossSections instance which will be used everywhere
    for sorted_coupling, cross_section_pureqcd, cross_section_pair_production, cross_section_single_production, cross_section_interference, cross_section_tchannel in zip(leptoquark_parameters.sorted_couplings, cross_sections_pureqcd, cross_sections_pair_production, cross_sections_single_production, cross_sections_interference, cross_sections_tchannel):
        process_cross_section = ProcessCrossSections(
            cross_section_pureqcd = cross_section_pureqcd,
            cross_section_pair_production = cross_section_pair_production,
            cross_section_single_production = cross_section_single_production,
            cross_section_interference = cross_section_interference,
            cross_section_tchannel = cross_section_tchannel,
            coupling = sorted_coupling,
        )
        if sorted_coupling[8] == '1': # electron 
            electron_electron_cross_section.single_coupling_cross_sections.append(process_cross_section)
        elif sorted_coupling[8] == '2': # muon
            muon_muon_cross_section.single_coupling_cross_sections.append(process_cross_section)
        elif sorted_coupling[8] == '3': # tau
            tau_tau_cross_section.single_coupling_cross_sections.append(process_cross_section)


    # cross terms
    # read interpolated cross-sections dataframes
    cross_terms_cross_section_tchannel_df = get_cross_terms_data_tchannel(leptoquark_parameters.leptoquark_model)

    for i in range(len(leptoquark_parameters.sorted_couplings)):
        for j in range(i+1, len(leptoquark_parameters.sorted_couplings)):
            cross_terms_coupling = f"{leptoquark_parameters.sorted_couplings[i]}_{leptoquark_parameters.sorted_couplings[j]}"
            cross_terms_cross_section_tchannel_df_for_coupling = [ 
                cross_terms_cross_section_tchannel_df[cross_terms_coupling]
                for i in range(len(leptoquark_parameters.sorted_couplings))
                for j in range(i + 1, len(leptoquark_parameters.sorted_couplings))
                if leptoquark_parameters.couplings[i][8] == leptoquark_parameters.couplings[j][8] # if couplings belong to the same category
            ]
            cross_terms_cross_section_tchannel_interpolation_function = interpolate_cross_section_cross_terms(cross_terms_cross_section_tchannel_df_for_coupling)
            cross_terms_cross_section_tchannel = cross_terms_cross_section_tchannel_interpolation_function(leptoquark_parameters.leptoquark_mass)
            cross_terms_cross_section = CrossTermsCrossSections(
                cross_section_cross_terms_tchannel = cross_terms_cross_section_tchannel - cross_sections_tchannel[i] - cross_sections_tchannel[j],
                coupling = cross_terms_coupling,
            )
            if cross_terms_coupling[8] == '1': # electron 
                electron_electron_cross_section.cross_terms_cross_sections.append(cross_terms_cross_section)
            elif cross_terms_coupling[8] == '2': # muon
                muon_muon_cross_section.cross_terms_cross_sections.append(cross_terms_cross_section)
            elif cross_terms_coupling[8] == '3': # tau
                tau_tau_cross_section.cross_terms_cross_sections.append(cross_terms_cross_section)

    return [
        electron_electron_cross_section,
        muon_muon_cross_section,
        tau_tau_cross_section,
    ]
