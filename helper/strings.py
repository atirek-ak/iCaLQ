from classes.config import code_infra_config

number_dict = {
    "1": "ONE",
    "2": "TWO",
    "3": "THREE"
}

def strip_comments_and_spaces(arg: str) -> str:
    return arg.split("#")[0].strip()

def convert_coupling_to_symbolic_coupling_format(coupling: str) -> str:
    return f"{number_dict[coupling[code_infra_config.get('coupling').get('quark_index')]]}_{number_dict[coupling[code_infra_config.get('coupling').get('lepton_index')]]}_{coupling[code_infra_config.get('coupling').get('chirality_index')]}"
