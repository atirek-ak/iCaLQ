import sys
from typing import List
from functools import cmp_to_key


from helper.sort import compare_couplings

class LeptoquarkParameters:
    def __init__(
        self,
        model: str = "",
        mass: float = 0,
        ignore_single_pair_processes: bool = False,
        significance: int = 0,
        systematic_error: float = 0,
        extra_width: float = 0,
        luminosity: float = 139,
        couplings: List[str] = ["X10LL[3,3]"],
        couplings_values: List[List[float]] = [],
        sorted_couplings: List[str] = [],
        sorted_couplings_values: List[List[float]] = [],
    ):
        self.model = model
        self.mass = mass
        self.couplings = couplings
        self.ignore_single_pair_processes = ignore_single_pair_processes
        self.significance = significance
        self.systematic_error = systematic_error
        self.extra_width = extra_width
        self.luminosity = luminosity
        self.couplings_values = couplings_values
        self.sorted_couplings = sorted_couplings
        self.sorted_couplings_values = sorted_couplings_values

    def __str__(self):
        return (
            f"Leptoquark Model: {self.model}\n"
            f"Leptoquark Mass: {self.mass} GeV\n"
            f"Ignore Single/Pair Processes: {self.ignore_single_pair_processes}\n"
            f"Significance: {self.significance}\n"
            f"Systematic error: {self.systematic_error * 100:.2f}%\n"
            f"Extra Width: {self.extra_width} GeV\n"
            f"Luminosity: {self.luminosity} fb^-1\n"
            f"Couplings: {self.couplings}\n"
            f"Couplings Values: {self.couplings_values}\n"
            f"Sorted Couplings: {self.sorted_couplings}\n"
            f"Sorted Couplings Values: {self.sorted_couplings_values}"
        )

    def read_non_interactive_input_coupling_values_from_file(self, input_file_path: str):
        with open(input_file_path) as v:
            self.couplings_values = v.readlines()
            # parse the coupling values data
            coupling_values = []
            for coupling_value in self.couplings_values:
                coupling_value = coupling_value.strip("\n").strip().split(" ")
                coupling_value = [float(value) for value in coupling_value]
                coupling_values.append(coupling_value)
            self.couplings_values = coupling_values

    def sort_couplings_and_values(self):
        for line_number, coupling_value in enumerate(
            self.couplings_values
        ):
            if len(coupling_value) != len(self.couplings):
                sys.exit(
                    f"[Query error]: Coupling values length in line {line_number+1} is {coupling_value} which does not match the length of input couplings {self.couplings}"
                )
            combined_couplings_and_values = zip(
                self.couplings, coupling_value
            )
            sorted_combined_couplings_and_values = sorted(
                combined_couplings_and_values, key=cmp_to_key(compare_couplings)
            )
            sorted_combined_couplings_and_values = list(
                zip(*sorted_combined_couplings_and_values)
            )
            self.sorted_couplings = list(
                sorted_combined_couplings_and_values[0]
            )
            self.sorted_couplings_values.append(
                list(sorted_combined_couplings_and_values[1])
            )
