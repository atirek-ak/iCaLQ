class LeptoquarkParameters:
    def __init__(
        self,
        leptoquark_model: str,
        leptoquark_mass: float,
        couplings: str,
        ignore_single_pair_processes: bool,
        significance: int,
        systematic_error: float,
        decay_width_constant: float,
        luminosity: float,
    ):
        self.leptoquark_model = leptoquark_model
        self.leptoquark_mass = leptoquark_mass
        self.couplings = couplings
        self.ignore_single_pair_processes = ignore_single_pair_processes
        self.significance = significance
        self.systematic_error = systematic_error
        self.decay_width_constant = decay_width_constant
        self.luminosity = luminosity