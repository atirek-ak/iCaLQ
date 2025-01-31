



class SingleCouplingEfficiency:
    def __init__(
        self,
        efficiency_pureqcd: List[float],
        efficiency_pair_production: List[float],
        efficiency_single_production: List[float],
        efficiency_interference: List[float],
        efficiency_tchannel: List[float],
    ):
        self.efficiency_pureqcd = efficiency_pureqcd
        self.efficiency_pair_production = efficiency_pair_production
        self.efficiency_single_production = efficiency_single_production
        self.efficiency_interference = efficiency_interference
        self.efficiency_tchannel = efficiency_tchannel

    def __str__(self):
        return (
            f"Efficiency Pure QCD: {self.efficiency_pureqcd}\n"
            f"Efficiency Pair Production: {self.efficiency_pair_production}\n"
            f"Efficiency Single Production: {self.efficiency_single_production}\n"
            f"Efficiency Interference: {self.efficiency_interference}\n"
            f"Efficiency T-Channel: {self.efficiency_tchannel}"
        )


class CrossTermsEfficiency:
    # This will only have t channel for now
    def __init__(
        self,
        efficiency_tchannel: List[float],
    ):
        self.efficiency_tchannel = efficiency_tchannel


class TagsTauTau:
    def __init__(
        self,
        hhbt: List[float],
        hhbv: List[float],
        lhbt: List[float],
        lhbv: List[float],
    ):
        self.hhbt = hhbt
        self.hhbv = hhbv
        self.lhbt = lhbt
        self.lhbv = lhbv


class SingleCouplingEfficiencyTauTau:
    def __init__(
        self,
        efficiency_pureqcd: TagsTauTau,
        efficiency_pair_production: TagsTauTau,
        efficiency_single_production: TagsTauTau,
        efficiency_interference: TagsTauTau,
        efficiency_tchannel: TagsTauTau,
    ):
        self.efficiency_pureqcd = efficiency_pureqcd
        self.efficiency_pair_production = efficiency_pair_production
        self.efficiency_single_production = efficiency_single_production
        self.efficiency_interference = efficiency_interference
        self.efficiency_tchannel = efficiency_tchannel


class CrossTermsEfficiencyTauTau:
    # This will only have t channel for now
    def __init__(
        self,
        efficiency_tchannel: TagsTauTau,
    ):
        self.efficiency_tchannel = efficiency_tchannel
