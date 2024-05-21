class LeptoquarkParameters:
    def __init__(
        self,
        leptoquark_model: str,
        leptoquark_mass: float,
        couplings: list,
        ignore_single_pair_processes: bool,
        significance: int,
        systematic_error: float,
        decay_width_constant: float,
        luminosity: float,
        couplings_values: list = [],
        sorted_couplings: list = [],
        sorted_couplings_values: list = [],
    ):
        self.leptoquark_model = leptoquark_model
        self.leptoquark_mass = leptoquark_mass
        self.couplings = couplings
        self.ignore_single_pair_processes = ignore_single_pair_processes
        self.significance = significance
        self.systematic_error = systematic_error
        self.decay_width_constant = decay_width_constant
        self.luminosity = luminosity
        self.couplings_values = couplings_values
        self.sorted_couplings = sorted_couplings
        self.sorted_couplings_values = sorted_couplings_values

class NonInteractiveInputParameters:
    def __init__(
        self,
        input_card_path: str,
        input_values_path: str,
        output_yes_path: str,
        output_no_path: str,
    ):
        self.input_card_path = input_card_path
        self.input_values_path = input_values_path
        self.output_yes_path = output_yes_path
        self.output_no_path = output_no_path


class ProcessCrossSections:
    def __init__(
        self,
        cross_section_pureqcd: float,
        cross_section_pair_production: float,
        cross_section_single_production: float,
        cross_section_interference: float,
        cross_section_tchannel: float,
        coupling: str,
    ):
        self.cross_section_pureqcd = cross_section_pureqcd
        self.cross_section_pair_production = cross_section_pair_production
        self.cross_section_single_production = cross_section_single_production
        self.cross_section_interference = cross_section_interference
        self.cross_section_tchannel = cross_section_tchannel
        self.coupling = coupling

class CrossTermsCrossSections:
    def __init__(
        self,
        cross_section_cross_terms_tchannel: float,
        coupling: str,
    ):
        self.cross_section_cross_terms_tchannel = cross_section_cross_terms_tchannel
        self.coupling = coupling

class ParticleCrossSections:
    def __init__(
        self,
        single_coupling_cross_sections: list[ProcessCrossSections] = [],
        cross_terms_cross_sections: list[CrossTermsCrossSections] = [],
    ):
        self.single_coupling_cross_sections = single_coupling_cross_sections
        self.cross_terms_cross_sections = cross_terms_cross_sections