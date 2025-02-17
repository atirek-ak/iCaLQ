import math
import sympy as sym
from typing import Dict, List

from classes.config import code_infra_config, physics_config
from classes.leptoquark_parameters import LeptoquarkParameters

class LeptoquarkMassDictionary:
    def __init__(
            self,
            dictionary: Dict[str, List[List[str]]] = {}
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
            mass_dictionary: LeptoquarkMassDictionary = LeptoquarkMassDictionary(),
            branching_fraction: sym.Symbol = sym.Float(0),
    ):
        self.mass_dictionary = mass_dictionary
        self.branching_fraction = branching_fraction

    def make_mass_dictionary(self, couplings: List[str]):
        self.mass_dictionary.make(couplings)

    @staticmethod
    def s1_decay_width_mass_factor(leptoquark_mass: float, mass_dictionary_coupling_element :list[float]):
        quark_mass = mass_dictionary_coupling_element[0]
        lepton_mass = mass_dictionary_coupling_element[1]
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


    @staticmethod
    def u1_decay_width_mass_factor( mass: float, mass_dictionary_coupling_element :list[float]):
        quark_mass = mass_dictionary_coupling_element[0]
        lepton_mass = mass_dictionary_coupling_element[1]
        return (
                BranchingFraction.momentum(mass, quark_mass, lepton_mass)
                * BranchingFraction.absolute_efficiency_coupling_mass_factor(
            mass, quark_mass, lepton_mass
        )
                / (8 * math.pow(math.pi, 2) * math.pow(mass, 2))
        )

    def get_branching_fraction_symbolic(
            self,
            leptoquark_parameters: LeptoquarkParameters,
            symbolic_couplings: List[sym.Symbol],
    ):
        numerator: sym.Symbol = sym.Float(0)
        denominator: sym.Symbol = sym.Float(leptoquark_parameters.extra_width)
        for coupling, symbolic_coupling in zip(
                leptoquark_parameters.sorted_couplings, symbolic_couplings
        ):
            if leptoquark_parameters.model == "U1":
                denominator += symbolic_coupling**2 * BranchingFraction.u1_decay_width_mass_factor(
                    leptoquark_parameters.mass, self.mass_dictionary.dictionary[coupling][0],
                )
                numerator += symbolic_coupling**2 * BranchingFraction.u1_decay_width_mass_factor(
                    leptoquark_parameters.mass, self.mass_dictionary.dictionary[coupling][0]
                )
                if coupling[code_infra_config.get('coupling').get('chirality_index')] == "L":
                    denominator += symbolic_coupling**2 * BranchingFraction.u1_decay_width_mass_factor(
                        leptoquark_parameters.mass, self.mass_dictionary.dictionary[coupling][1]
                    )
            elif leptoquark_parameters.model == "S1":
                denominator += symbolic_coupling**2 * BranchingFraction.s1_decay_width_mass_factor(
                    leptoquark_parameters.mass, self.mass_dictionary.dictionary[coupling][0]
                )
                numerator += symbolic_coupling**2 * BranchingFraction.s1_decay_width_mass_factor(
                    leptoquark_parameters.mass, self.mass_dictionary.dictionary[coupling][0],
                )
                if coupling[code_infra_config.get('coupling').get('chirality_index')] == "L":
                    denominator += symbolic_coupling**2 * BranchingFraction.s1_decay_width_mass_factor(
                        leptoquark_parameters.mass, self.mass_dictionary.dictionary[coupling][1],
                    )

        if denominator == sym.Float(0):
            self.branching_fraction = sym.Float(0)
        else:
            self.branching_fraction = numerator / denominator
