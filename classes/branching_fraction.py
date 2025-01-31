import math
import sympy as sym
from typing import Dict, List

from classes.config import code_infra_config, physics_config
from classes.leptoquark_parameters import LeptoquarkParameters

class LeptoquarkMassDictionary:
    def __init__(
            self,
            dictionary: Dict[str, List[List[str]]] = None
    ):
        self.dictionary = dictionary

    def make(self, couplings: List[str]):
        for coupling in couplings:
            if coupling[code_infra_config.get('coupling').get('chirality_index')] == "L":
                self.dictionary[coupling] = [
                    [
                        physics_config.get('mass_quarks')[coupling[code_infra_config.get('coupling').get('quark_index')]][1],
                        physics_config.get('mass_leptons')[coupling[code_infra_config.get('coupling').get('lepton_index')]][0],
                    ],
                    [
                        physics_config.get('mass_quarks')[coupling[code_infra_config.get('coupling').get('quark_index')]][0],
                        physics_config.get('mass_leptons')[coupling[code_infra_config.get('coupling').get('lepton_index')]][1],
                    ],
                ]
            elif coupling[code_infra_config.get('coupling').get('chirality_index')] == "R":
                self.dictionary[coupling] = [
                    [
                        physics_config.get('mass_quarks')[coupling[code_infra_config.get('coupling').get('quark_index')]][1],
                        physics_config.get('mass_leptons')[coupling[code_infra_config.get('coupling').get('lepton_index')]][0],
                    ]
                ]

class BranchingFraction:
    def __init__(
            self,
            mass_dictionary: LeptoquarkMassDictionary = None,
            branching_fraction: sym.Symbol = None,
    ):
        self.mass_dictionary = mass_dictionary
        self.branching_fraction = branching_fraction

    def make_mass_dictionary(self, couplings: List[str]):
        self.mass_dictionary.make(couplings)

    def s1_decay_width_mass_factor(self, leptoquark_mass: float):
        quark_mass = self.mass_dictionary[0]
        lepton_mass = self.mass_dictionary[1]
        return (
                (math.pow(leptoquark_mass, 2) - math.pow(lepton_mass + quark_mass, 2))
                * (
                    math.sqrt(
                        (math.pow(leptoquark_mass, 2) -
                         math.pow(lepton_mass + quark_mass, 2))
                        * (math.pow(leptoquark_mass, 2) - math.pow(lepton_mass - quark_mass, 2))
                    )
                )
                / (8 * math.pi * math.pow(leptoquark_mass, 3))
        )

    @staticmethod
    def momentum(leptoquark_mass: float, quark_mass: float, lepton_mass: float):
        a = math.pow(leptoquark_mass + lepton_mass, 2) - math.pow(quark_mass, 2)
        b = math.pow(leptoquark_mass - lepton_mass, 2) - math.pow(quark_mass, 2)
        return math.sqrt(a * b) / (2 * leptoquark_mass)


    @staticmethod
    def absolute_efficiency_coupling_mass_factor(
            leptoquark_mass: float, quark_mass: float, lepton_mass: float
    ):
        return (
                math.pow(leptoquark_mass, 2)
                - (math.pow(lepton_mass, 2) + math.pow(quark_mass, 2))
                - math.pow((math.pow(lepton_mass, 2) - math.pow(quark_mass, 2)), 2)
                / math.pow(leptoquark_mass, 2)
                - (6 * lepton_mass * quark_mass)
        )


    def u1_decay_width_mass_factor(self, mass: float):
        return (
                BranchingFraction.momentum(mass, self.mass_dictionary[0], self.mass_dictionary[1])
                * BranchingFraction.absolute_efficiency_coupling_mass_factor(
            mass, self.mass_dictionary[0], self.mass_dictionary[1]
        )
                / (8 * math.pow(math.pi, 2) * math.pow(mass, 2))
        )

    def get_branching_fraction_symbolic(
            self,
            leptoquark_parameters: LeptoquarkParameters,
            symbolic_couplings: List[sym.Symbol],
    ) -> sym.Symbol:
        numerator: sym.Symbol = sym.Float(0)
        denominator: sym.Symbol = sym.Float(leptoquark_parameters.extra_width)
        for coupling, symbolic_coupling in zip(
                leptoquark_parameters.sorted_couplings, symbolic_couplings
        ):
            if leptoquark_parameters.model == "U1":
                denominator += symbolic_coupling**2 * self.u1_decay_width_mass_factor(
                    leptoquark_parameters.mass
                )
                numerator += symbolic_coupling**2 * self.u1_decay_width_mass_factor(
                    leptoquark_parameters.mass
                )
                if coupling[code_infra_config.get('coupling').get('chirality_index')] == "L":
                    denominator += symbolic_coupling**2 * self.u1_decay_width_mass_factor(
                        leptoquark_parameters.mass
                    )
            elif leptoquark_parameters.model == "S1":
                denominator += symbolic_coupling**2 * self.s1_decay_width_mass_factor(
                    leptoquark_parameters.mass
                )
                numerator += symbolic_coupling**2 * self.s1_decay_width_mass_factor(
                    leptoquark_parameters.mass
                )
                if coupling[code_infra_config.get('coupling').get('chirality_index')] == "L":
                    denominator += symbolic_coupling**2 * self.s1_decay_width_mass_factor(
                        leptoquark_parameters.mass,
                    )

        self.branching_fraction = numerator / denominator
