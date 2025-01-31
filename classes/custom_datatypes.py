# input modes
from enum import Enum

class InputMode(Enum):
    INTERACTIVE = "interactive"
    NONINTERACTIVE = "noninteractive"

# corresponds to
class DecayProcess(Enum):
    PAIR_PRODUCTION = "pair_production"
    SINGLE_PRODUCTION = "single_production"
    INTERFERENCE = "interference"
    PUREQCD = "pureqcd"
    T_CHANNEL = "t_channel"
    T_CHANNEL_DOUBLE_COUPLING = "t_channel_double_coupling"
    T_CHANNEL_COMBINED = "t_channel_combined"

class Generation(Enum):
    ELECTRON = 1
    MUON = 2
    TAU = 3

class Tag(Enum):
    HHBT = "HHbT"
    HHBV = "HHbV"
    LHBT = "LHbT"
    LHBV = "LHbV"

class KFactor:
    dictionary = {
        "U1": {
            DecayProcess.PAIR_PRODUCTION: 1.5,
            DecayProcess.SINGLE_PRODUCTION: 1.0,
            DecayProcess.INTERFERENCE: 1.0,
            DecayProcess.PUREQCD: 1.5,
            DecayProcess.T_CHANNEL: 1.0,
        },
        "S1": {
            DecayProcess.PAIR_PRODUCTION: 1.0,
            DecayProcess.SINGLE_PRODUCTION: 1.0,
            DecayProcess.INTERFERENCE: 1.0,
            DecayProcess.PUREQCD: 1.0,
            DecayProcess.T_CHANNEL: 1.0,
        },
    }