import pandas as pd

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

interpolation_type = "slinear"
mev2gev = 0.001

mass_quarks = {"1": [2.3, 4.8], "2": [1275, 95], "3": [173070, 4180]}

for gen in mass_quarks:
    mass_quarks[gen] = [x * mev2gev for x in mass_quarks[gen]]

mass_leptons = {"1": [0.511, 0.0022], "2": [105.7, 0.17], "3": [1777, 15.5]}
for gen in mass_leptons:
    mass_leptons[gen] = [x * mev2gev for x in mass_leptons[gen]]

data_mass_list = [1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000]
luminosity_tau = 139 * 1000
luminosity_e_mu = 140 * 1000

DATA_PREFIX = "data"
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

# Path variables for cross section:
cs_sc_path = "./data/cross_section/"


# df_pair = pd.read_csv(f"{cs_sc_path}pair.csv")
def get_df_pair(model: str):
    return pd.read_csv(f"{DATA_PREFIX}/model/{model}/cross_section/pair.csv")


# df_single = pd.read_csv(f"{cs_sc_path}single.csv")
def get_df_single(model: str):
    return pd.read_csv(f"{DATA_PREFIX}/model/{model}/cross_section/single.csv")


# df_interference = pd.read_csv(f"{cs_sc_path}interference.csv")
def get_df_interference(model: str):
    return pd.read_csv(f"{DATA_PREFIX}/model/{model}/cross_section/interference.csv")


# df_tchannel = pd.read_csv(f"{cs_sc_path}tchannel.csv")
def get_df_tchannel(model: str):
    return pd.read_csv(f"{DATA_PREFIX}/model/{model}/cross_section/tchannel.csv")


# df_pureqcd = pd.read_csv(f"{cs_sc_path}pureqcd.csv")
def get_df_pureqcd(model: str):
    return pd.read_csv(f"{DATA_PREFIX}/model/{model}/cross_section/pureqcd.csv")


# double_coupling_data_tchannel = pd.read_csv(cross_terms_tchannel, header=[0])
def get_double_coupling_data_tchannel(model: str):
    return pd.read_csv(
        f"{DATA_PREFIX}/model/{model}/cross_section/tchannel_doublecoupling.csv",
        header=[0],
    )


# efficiency_prefix = "./data/efficiency/"
def get_efficiency_prefix(model: str):
    return f"{DATA_PREFIX}/model/{model}/efficiency/"


# t_ct_prefix = "./data/efficiency/t/"
def get_t_ct_prefix(model: str):
    return f"{DATA_PREFIX}/model/{model}/efficiency/t/"


tagnames = ["/HHbT.csv", "/HHbV.csv", "/LHbT.csv", "/LHbV.csv"]

k_factor_pair_production = 1.5
k_factor_pureqcd = 1.5
k_factor_single_production = 1.0
k_factor_t_channel = 1.0
k_factor_interference = 1.0