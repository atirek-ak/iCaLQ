from typing import Dict, Union
from scipy.interpolate import interp1d

from utilities.data_classes import LeptoquarkParameters, SingleCouplingCrossSections, ParticleCrossSections, CrossTermsCrossSections
from utilities.constants import (
    get_cross_sections_df_pair_production,
    get_cross_sections_df_single_production,
    get_cross_sections_df_interference,
    get_cross_sections_df_tchannel,
    get_cross_sections_df_pureqcd,
    get_cross_sections_df_cross_terms_tchannel,
    quark_index
)

def getCrossSections(leptoquark_parameters: LeptoquarkParameters) -> dict:
    """
    Get cross sections from data files
    
    The dict that is returns has mapping:
    Single coupling: coupling -> SingleCouplingCrossSections
    Cross terms: coupling -> CrossTermsCrossSections
    """
    # this map stores the cross-sections for every coupling
    coupling_to_process_cross_section_map: Dict[str, Union[SingleCouplingCrossSections, CrossTermsCrossSections]] = {}

    # single coupling
    # read interpolated cross-sections dataframes
    cross_section_pureqcd_interpolation_function = interpolateLinearCrossSection(get_cross_sections_df_pureqcd(leptoquark_parameters.leptoquark_model), leptoquark_parameters.sorted_couplings)
    cross_sections_pureqcd = cross_section_pureqcd_interpolation_function(leptoquark_parameters.leptoquark_mass) # list of floats in sorted couplings order
    cross_section_pair_production_interpolation_function = interpolateLinearCrossSection(get_cross_sections_df_pair_production(leptoquark_parameters.leptoquark_model), leptoquark_parameters.sorted_couplings)
    cross_sections_pair_production = cross_section_pair_production_interpolation_function(leptoquark_parameters.leptoquark_mass) # list of floats in sorted couplings order
    cross_section_single_production_interpolation_function = interpolateLinearCrossSection(get_cross_sections_df_single_production(leptoquark_parameters.leptoquark_model), leptoquark_parameters.sorted_couplings)
    cross_sections_single_production = cross_section_single_production_interpolation_function(leptoquark_parameters.leptoquark_mass) # list of floats in sorted couplings order
    cross_section_interference_interpolation_function = interpolateLinearCrossSection(get_cross_sections_df_interference(leptoquark_parameters.leptoquark_model), leptoquark_parameters.sorted_couplings)
    cross_sections_interference = cross_section_interference_interpolation_function(leptoquark_parameters.leptoquark_mass) # list of floats in sorted couplings order
    cross_section_tchannel_interpolation_function = interpolateLinearCrossSection(get_cross_sections_df_tchannel(leptoquark_parameters.leptoquark_model), leptoquark_parameters.sorted_couplings)
    cross_sections_tchannel = cross_section_tchannel_interpolation_function(leptoquark_parameters.leptoquark_mass) # list of floats in sorted couplings order

    # categorise them by particle and assign to ParticleCrossSections instance which will be used everywhere
    for sorted_coupling, cross_section_pureqcd, cross_section_pair_production, cross_section_single_production, cross_section_interference, cross_section_tchannel in zip(leptoquark_parameters.sorted_couplings, cross_sections_pureqcd, cross_sections_pair_production, cross_sections_single_production, cross_sections_interference, cross_sections_tchannel):
        coupling_to_process_cross_section_map[sorted_coupling] = SingleCouplingCrossSections(
            cross_section_pureqcd = cross_section_pureqcd,
            cross_section_pair_production = cross_section_pair_production,
            cross_section_single_production = cross_section_single_production,
            cross_section_interference = cross_section_interference,
            cross_section_tchannel = cross_section_tchannel,
        )
        
    # cross terms
    # read interpolated cross-sections dataframes
    cross_terms_cross_section_tchannel_df = get_cross_sections_df_cross_terms_tchannel(leptoquark_parameters.leptoquark_model)
    for i in range(len(leptoquark_parameters.sorted_couplings)):
        for j in range(i+1, len(leptoquark_parameters.sorted_couplings)):
            # if couplings belong to the same category
            if leptoquark_parameters.sorted_couplings[i][quark_index] == leptoquark_parameters.sorted_couplings[j][quark_index]:
                cross_terms_coupling = f"{leptoquark_parameters.sorted_couplings[i]}_{leptoquark_parameters.sorted_couplings[j]}"
                cross_terms_cross_section_tchannel_interpolation_function = interpolateLinearCrossSection(cross_terms_cross_section_tchannel_df, [cross_terms_coupling])
                cross_terms_cross_section_tchannel = cross_terms_cross_section_tchannel_interpolation_function(leptoquark_parameters.leptoquark_mass)
                coupling_to_process_cross_section_map[cross_terms_coupling] = CrossTermsCrossSections(
                    cross_terms_cross_section_tchannel = cross_terms_cross_section_tchannel - cross_sections_tchannel[i] - cross_sections_tchannel[j],
                    actual_cross_section_tchannel = cross_terms_cross_section_tchannel,
                )
    
    return coupling_to_process_cross_section_map

def interpolateLinearCrossSection(df, couplings):
    """
    Returns a function for linear interpolate of cross-section for all masses
    """
    return lambda mass: [
        interp1d(df["Mass"], df[coupling], kind="slinear")(mass)
        for coupling in couplings
    ]
