from typing import Any

from classes.config import code_infra_config

def compare_couplings(item1: Any, item2: Any) -> int:
    """
    Use this function as the comparator function while sorting lambdas
    """
    a1 = list(item1[0])
    a2 = list(item2[0])
    if a1[code_infra_config.get('coupling').get('chirality_index')] != a2[code_infra_config.get('coupling').get('chirality_index')]:
        return -1 if a1[code_infra_config.get('coupling').get('chirality_index')] == "L" else 1
    if a1[code_infra_config.get('coupling').get('quark_index')] != a2[code_infra_config.get('coupling').get('quark_index')]:
        return ord(a1[code_infra_config.get('coupling').get('quark_index')]) - ord(a2[code_infra_config.get('coupling').get('quark_index')])
    if a1[code_infra_config.get('coupling').get('lepton_index')] != a2[code_infra_config.get('coupling').get('lepton_index')]:
        return ord(a1[code_infra_config.get('coupling').get('lepton_index')]) - ord(a2[code_infra_config.get('coupling').get('lepton_index')])
    return -1

    