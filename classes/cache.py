import re
import sympy as sym
from diskcache import Cache
from typing import List

from classes.leptoquark_parameters import LeptoquarkParameters
from helper.strings import convert_coupling_to_symbolic_coupling_format

class PersistentDiskCache:
    def __init__(self, cache_dir="cache", size_limit=1024 * 1024 * 100, cull_limit=1000):
        self.cache = Cache(cache_dir, size_limit=size_limit, cull_limit=cull_limit)

    @staticmethod
    def construct_chi_square_expression_cache_key(leptoquark_parameters: LeptoquarkParameters):
        return f"chi_square_{leptoquark_parameters.model}_{str(leptoquark_parameters.mass)}_{str(leptoquark_parameters.ignore_single_pair_processes)}_{str(leptoquark_parameters.systematic_error)}_{str(leptoquark_parameters.extra_width)}_{'_'.join(leptoquark_parameters.sorted_couplings)}"

    @staticmethod
    def construct_chi_square_without_leptoquark_expression_cache_key(leptoquark_parameters: LeptoquarkParameters):
        return f"chi_square_without_leptoquark_{leptoquark_parameters.model}_{str(leptoquark_parameters.mass)}_{str(leptoquark_parameters.ignore_single_pair_processes)}_{str(leptoquark_parameters.systematic_error)}_{str(leptoquark_parameters.extra_width)}_{'_'.join(leptoquark_parameters.sorted_couplings)}"

    @staticmethod
    def construct_chi_square_minima_cache_key(leptoquark_parameters: LeptoquarkParameters):
        return f"minima_{leptoquark_parameters.model}_{str(leptoquark_parameters.mass)}_{str(leptoquark_parameters.ignore_single_pair_processes)}_{str(leptoquark_parameters.systematic_error)}_{str(leptoquark_parameters.extra_width)}_{'_'.join(leptoquark_parameters.sorted_couplings)}"

    @staticmethod
    def construct_chi_square_minima_couplings_cache_key(leptoquark_parameters: LeptoquarkParameters):
        return f"minima_couplings_{leptoquark_parameters.model}_{str(leptoquark_parameters.mass)}_{str(leptoquark_parameters.ignore_single_pair_processes)}_{str(leptoquark_parameters.systematic_error)}_{str(leptoquark_parameters.extra_width)}_{'_'.join(leptoquark_parameters.sorted_couplings)}"

    def set(self, key: str, value: str):
        self.cache[key] = value

    def get_symbolic_expression(self, key: str) -> sym.Symbol:
        value = self.cache.get(key, None)
        if value is None:
            return sym.Float(0)

        coupling_regex_expression = r'[XY]10(?:LL|RR)\[[1-3],[1-3]\]'
        coupling_matches = re.findall(coupling_regex_expression, value)
        placeholder_string_value = value
        for i, match in enumerate(coupling_matches):
            substituted_value_for_match = convert_coupling_to_symbolic_coupling_format(match)
            placeholder_string_value = placeholder_string_value.replace(match, substituted_value_for_match)

        symbolic_expression = sym.sympify(placeholder_string_value)
        return symbolic_expression

    def get_float_value(self, key: str) -> float:
        value = self.cache.get(key, None)
        if value is None:
            return 0
        return float(value)

    def get_list_of_floats_value(self, key: str) -> List[float]:
        value = self.cache.get(key, None)
        if value is None:
            return []
        return [float(element) for element in value.split(' ')]


    def delete(self, key: str):
        if key in self.cache:
            del self.cache[key]

    def clear(self):
        self.cache.clear()

    def close(self):
        self.cache.close()