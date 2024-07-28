import pandas as pd
from enum import Enum

# INFRA
# coupling input params
lepton_index = 6
quark_index = 8
chirality_index = 6

# input modes
class InputMode(Enum):
    INTERACTIVE = "interactive"
    NONINTERACTIVE = "noninteractive"

# non-interactive card params
input_card_number_of_lines = 9

# interactive mode default values
default_ignore_single_pair_processes = "no"
default_significane = 2
default_systematic_error = "0.1"
default_decay_width_constant = 0

# FILES
DATA_PREFIX = "data"

# cross-section
def get_cross_sections_df_pair_production(model: str):
    return pd.read_csv(f"{DATA_PREFIX}/model/{model}/cross_section/pair.csv", header=[0])
def get_cross_sections_df_single_production(model: str):
    return pd.read_csv(f"{DATA_PREFIX}/model/{model}/cross_section/single.csv", header=[0])
def get_cross_sections_df_interference(model: str):
    return pd.read_csv(f"{DATA_PREFIX}/model/{model}/cross_section/interference.csv", header=[0])
def get_cross_sections_df_tchannel(model: str):
    return pd.read_csv(f"{DATA_PREFIX}/model/{model}/cross_section/tchannel.csv", header=[0])
def get_cross_sections_df_pureqcd(model: str):
    return pd.read_csv(f"{DATA_PREFIX}/model/{model}/cross_section/pureqcd.csv", header=[0])
def get_cross_sections_df_cross_terms_tchannel(model: str):
    return pd.read_csv(f"{DATA_PREFIX}/model/{model}/cross_section/tchannel_doublecoupling.csv",header=[0])

# efficiency
def get_efficiency_prefix(model: str):
    return f"{DATA_PREFIX}/model/{model}/efficiency"
def get_t_ct_prefix(model: str):
    return f"{DATA_PREFIX}/model/{model}/efficiency/t"

# tau-tau tagNames
tagNames = ["HHbT.csv", "HHbV.csv", "LHbT.csv", "LHbV.csv"]

# CALCUATION
# coupling value limits
# Currently being used for generating random coupling values
min_coupling_value_limit = -3.5
max_coupling_value_limit = 3.5

# lepton & quark masses
mass_quarks = {'1': [0.0023, 0.0048], '2': [1.275, 0.095], '3': [173.07, 4.18]}
mass_leptons = {'1': [0.000511, 2.2e-06], '2': [0.1057, 0.00017], '3': [1.777, 0.0155]}




# Declaring variables which need not be reloaded every run
chi_sq_limits_1 = [
    1.00,
    2.295748928898636,
    3.5267403802617303,
    4.719474460025883,
    5.887595445915204,
    7.038400923736641,
    8.176236497856527,
    9.30391276903717,
    10.423363154355838,
    11.535981713319316,
    12.64281133339149,
    13.744655587189282,
    14.842148802786893,
    15.935801892195538,
    17.026033423371082,
    18.11319133873574,
    19.197568537049687,
]
chi_sq_limits_2 = [
    4.00,
    6.180074306244173,
    8.024881760266252,
    9.715627154871333,
    11.313855908361862,
    12.848834791793395,
    14.337110231671799,
    15.789092974617745,
    17.21182898078949,
    18.610346565823498,
    19.988381717650192,
    21.348799569984315,
    22.693854280452445,
    24.025357063756637,
    25.344789151124267,
    26.653380234523553,
    27.952164463248984,
]

scalar_leptoquark_models = ["S1"]
vector_leptoquark_models = ["U1"]

minimum_lepptoquark_mass_supported = 1000
maximum_lepptoquark_mass_supported = 5000

data_mass_list = [1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000]

luminosity_tau = 139 * 1000
luminosity_e_mu = 140 * 1000

LHC_DATA_PREFIX = f"{DATA_PREFIX}/HEPdata"

standard_HHbT = pd.read_csv(f"{LHC_DATA_PREFIX}/HHbT.csv", header=[0])
standard_HHbV = pd.read_csv(f"{LHC_DATA_PREFIX}/HHbV.csv", header=[0])
standard_LHbT = pd.read_csv(f"{LHC_DATA_PREFIX}/LHbT.csv", header=[0])
standard_LHbV = pd.read_csv(f"{LHC_DATA_PREFIX}/LHbV.csv", header=[0])
standard_ee = pd.read_csv(f"{LHC_DATA_PREFIX}/dielectron.csv", header=[0])
standard_mumu = pd.read_csv(f"{LHC_DATA_PREFIX}/dimuon.csv", header=[0])
ND = [
    standard_HHbT["ND"].to_numpy(),
    standard_HHbV["ND"].to_numpy(),
    standard_LHbT["ND"].to_numpy(),
    standard_LHbV["ND"].to_numpy(),
    standard_ee["ND"].to_numpy(),
    standard_mumu["ND"].to_numpy(),
]
NSM = [
    standard_HHbT["Standard Model"].to_numpy(),
    standard_HHbV["Standard Model"].to_numpy(),
    standard_LHbT["Standard Model"].to_numpy(),
    standard_LHbV["Standard Model"].to_numpy(),
    standard_ee["Standard Model"].to_numpy(),
    standard_mumu["Standard Model"].to_numpy(),
]


k_factor_pair_production = 1.5
k_factor_pureqcd = 1.5
k_factor_single_production = 1.0
k_factor_t_channel = 1.0
k_factor_interference = 1.0