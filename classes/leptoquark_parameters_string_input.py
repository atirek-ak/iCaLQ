import os
import random
import sys

from calculate import calculate
from classes.config import physics_config, code_infra_config
from classes.config import physics_config, code_infra_config
from classes.leptoquark_parameters import LeptoquarkParameters
from helper.strings import strip_comments_and_spaces
from helper.output import raise_error_or_print_warning, pr_blue, pr_blue_no_new_line, pr_red, raise_error_or_print_warning
from utilities.constants import InputMode


class LeptoquarkParametersStringInput:
    def __init__(
            self,
            model: str = "U1",
            mass: str = "1000.0",
            ignore_single_pair_processes: str = "no",
            significance: str = "2",
            systematic_error: str = "0.1",
            couplings: str = "X10LL[3,3]",
            extra_width: str = "0.0",
            random_points: str = "0",
            start_calculation: bool = False,
    ):
        self.model = model
        self.mass = mass
        self.couplings = couplings
        self.ignore_single_pair_processes = ignore_single_pair_processes
        self.significance = significance
        self.systematic_error = systematic_error
        self.extra_width = extra_width
        self.random_points = random_points
        # used for interactive mode to start calculation or not
        self.start_calculation = start_calculation
        
    def read_data_from_input_file(self, input_card_path: str = ""):
        if not os.path.isfile(input_card_path):
            sys.exit(
                f"Input card file {input_card_path} does not exist. Exiting.\n"
            )
        with open(input_card_path, encoding="utf8") as c:
            input_card_lines = c.readlines()
        if len(input_card_lines) != code_infra_config.get('non_interactive_input').get('card').get('number_of_lines'):
            sys.exit(
                f"Number of lines in file: {len(input_card_lines)}, expected {code_infra_config.get('non_interactive_input').get('card').get('number_of_lines')}. Please refer to README to check if all the data is present."
            )

        self.model = strip_comments_and_spaces(input_card_lines[code_infra_config.get("non_interactive_input").get("card").get("leptoquark_model_index")])
        self.mass = strip_comments_and_spaces(input_card_lines[code_infra_config.get("non_interactive_input").get("card").get("mass_index")])
        self.couplings = strip_comments_and_spaces(input_card_lines[code_infra_config.get("non_interactive_input").get("card").get("couplings_index")])
        self.ignore_single_pair_processes = strip_comments_and_spaces(input_card_lines[code_infra_config.get("non_interactive_input").get("card").get("ignore_single_and_pair_productions_index")])
        self.significance = strip_comments_and_spaces(input_card_lines[code_infra_config.get("non_interactive_input").get("card").get("significance_index")])
        self.systematic_error = strip_comments_and_spaces(input_card_lines[code_infra_config.get("non_interactive_input").get("card").get("systematic_error_index")])
        self.extra_width = strip_comments_and_spaces(input_card_lines[code_infra_config.get("non_interactive_input").get("card").get("width_constant_index")])
        self.random_points = strip_comments_and_spaces(input_card_lines[code_infra_config.get("non_interactive_input").get("card").get("number_of_random_points_index")])

    def validate_and_write_random_points_to_input_values_file(self, input_values_path: str = "", couplings_length: int = 0):
        if not os.path.isfile(input_values_path):
            sys.exit(
                f"Input values file {input_values_path} does not exist. Exiting.\n"
            )

        try:
            random_points = int(self.random_points)
            if random_points < 0:
                raise ValueError("Random points should be a non-negative integer")
        except:
            raise ValueError("Random points should be a valid number")

        if self.random_points > 0:
            f = open(input_values_path, "w")
            for _ in range(random_points):
                coupling_values_list = [
                    str(random.uniform(physics_config.get("minimum_coupling_value_limit"), physics_config.get("maximum_coupling_value_limit")))
                    for _ in range(couplings_length)
                ]
                coupling_values_string = " ".join(coupling_values_list)
                f.write(f"{coupling_values_string}\n")
            f.close()
  
    def print_initial_message(self):
        pr_blue("========================================================")
        pr_blue("Commands available:")
        print(
            " import_model:, mass=, couplings: , extra_width=,\n ignore_single_pair: (yes/no), significance=(1/2),\n systematic_error=, status, initiate, help"
        )

        pr_blue("Couplings available:")
        print(
            " Examples for S1: Y10LL[1,1] Y10RR[3,1] [...]\n Examples for U1: X10LL[3,2] X10RR[1,1] [...]"
        )

        pr_blue("Default values:")
        print(f" import_model: U1")
        print(f" mass = 1000")
        print(f" couplings: X10LL[3,3]")
        print(f" extra_width = {self.extra_width}")
        print(f" ignore_single_pair: {self.ignore_single_pair_processes}")
        print(f" significance = {self.significance}")
        print(f" systematic_error = {self.systematic_error}")
        pr_blue("========================================================")

    def print_interactive_help(self):
        pr_blue(
            "Commands with '=' expect a numerical value. Read README.md for more info on individual commands."
        )
        pr_blue("Value input commands: ")
        print(" import_model: [Leptoquark model]")
        print(" mass= [Leptoquark mass] (should be between 1000 and 5000)")
        print(" couplings: [Couplings. For the format, refer to README.md]")
        print(
            " ignore_single_pair: [If true, the single & pair production contributions are ignored]"
        )
        print(
            " significance= [Significance of the limit in standard deviations. Possible values=1,2]"
        )
        print(
            " systematic_error= [Systematic error to be included in the calculations. Should be between 0 and 1]"
        )
        print(
            " extra_width= [extra width to account for additional unaccounted decays]")
        pr_blue("Other commands:")
        print(" status [To print current values]")
        print(" initiate [To start the calcualation]")
        print(" exit [To exit the calculator]")
        
    def validate_leptoquark_model(self, raise_error=False):
        if (
            self.model not in physics_config.get('scalar_leptoquark_models')
            and self.model not in physics_config.get('vector_leptoquark_models')
        ):
            raise_error_or_print_warning(
                f"[Model error]: Not a valid leptoquark model. Allowed models: {physics_config.get('scalar_leptoquark_models') + physics_config.get('vector_leptoquark_models')}",
                raise_error
            )
        
    def validate_leptoquark_mass(self, raise_error=False):
        try:
            mass = float(self.mass)
            if (
                mass < physics_config.get('minimum_leptoquark_mass')
                or mass > physics_config.get('maximum_leptoquark_mass')
            ):
                raise_error_or_print_warning(
                    f"[Mass error]: Leptoquark mass should be from {physics_config.get('minimum_leptoquark_mass')} to {physics_config.get('maximum_leptoquark_mass')} GeV",
                    raise_error
                )
        except:
            raise_error_or_print_warning(
                "[Mass error]: Leptoquark mass should be a valid number",
                raise_error
            )
    
    def validate_couplings(self, raise_error=False):
        couplings_list = self.couplings.strip().split(" ")
        if not len(couplings_list):
            raise_error_or_print_warning(
                "[Couplings error]: Couplings cannot be empty. For valid format, refer to README",
                raise_error
            )
        # Count frequency of each element
        frequency = {}
        for item in couplings_list:
            if item in frequency:
                raise_error_or_print_warning(
                    f"[Couplings error]: Coupling {item} is repeated. A coupling can only be inputted once",
                    raise_error
                )
            else:
                frequency[item] = 1
        for i in range(len(couplings_list)):
            if len(couplings_list[i].strip()) != code_infra_config.get("coupling").get("length"):
                raise_error_or_print_warning(
                    f"[Couplings error]: The couplings input {couplings_list[i]} is not {code_infra_config.get('coupling').get('length')} characters. For valid format, refer to README",
                    raise_error
                )
            if not (
                (
                    couplings_list[i][0] == code_infra_config.get("coupling").get("scalar_leptoquark_0th_index_value")
                    and self.model in physics_config.get('scalar_leptoquark_models')
                )
                or (
                    couplings_list[i][0] == code_infra_config.get("coupling").get("vector_leptoquark_0th_index_value")
                    and self.model in physics_config.get('vector_leptoquark_models')
                )
            ):
                raise_error_or_print_warning(
                    f"[Couplings error]: For scalar leptoquarks, the first letter should be {code_infra_config.get('coupling').get('scalar_leptoquark_0th_index_value')} & for vector leptoquarks it should be {config.get('coupling').get('vector_leptoquark_0th_index_value')}. For valid format, refer to README",
                    raise_error
                )
            if couplings_list[i][1:3] != code_infra_config.get('coupling').get('2nd_and_3rd_index_values'):
                raise_error_or_print_warning(
                    f"[Couplings error]: The second and third characters of {couplings_list[i]} should be '{code_infra_config.get('coupling').get('2nd_and_3rd_index_values')}'. For valid format, refer to README",
                    raise_error
                )
            if couplings_list[i][3] not in code_infra_config.get('coupling').get('chirality_index_values'):
                raise_error_or_print_warning(
                    f"[Couplings error]: The 4th character of {couplings_list[i]} should be in {code_infra_config.get('coupling').get('chirality_index_values')} for left-handed & right-handed couplings respectively. For valid format, refer to README",
                    raise_error
                )
            if couplings_list[i][4] not in code_infra_config.get('coupling').get('chirality_index_values'):
                raise_error_or_print_warning(
                    f"[Couplings error]: The 5th character of {couplings_list[i]} should be in {code_infra_config.get('coupling').get('chirality_index_values')} for left-handed & right-handed couplings respectively. For valid format, refer to README",
                    raise_error
                )
            if couplings_list[i][5] != code_infra_config.get('coupling').get('5th_index_value'):
                raise_error_or_print_warning(
                    f"[Couplings error]: The 6th character of {couplings_list[i]} should be {code_infra_config.get('coupling').get('5th_index_value')}. For valid format, refer to README",
                    raise_error
                )
            if (
                self.model in physics_config.get('scalar_leptoquark_models')
                and couplings_list[i][6] not in code_infra_config.get('coupling').get('scalar_leptoquark_valid_quark_generations')
            ) or (
                self.model in physics_config.get('vector_leptoquark_models')
                and couplings_list[i][6] not in code_infra_config.get('coupling').get('vector_leptoquark_valid_quark_generations')
            ):
                raise_error_or_print_warning(
                    f"[Couplings error]: The 7th character of {couplings_list[i]} should be a valid quark generation. For valid format, refer to README",
                    raise_error
                )
            if couplings_list[i][7] != code_infra_config.get('coupling').get('7th_index_value'):
                raise_error_or_print_warning(
                    f"[Couplings error]: The 8th character of {couplings_list[i]} should be {code_infra_config.get('coupling').get('7th_index_value')}. For valid format, refer to README",
                    raise_error
                )
            if couplings_list[i][8] not in code_infra_config.get('coupling').get('valid_lepton_generations'):
                raise_error_or_print_warning(
                    f"[Couplings error]: The 9th character of {couplings_list[i]} should be a valid lepton generation. For valid format, refer to README",
                    raise_error
                )
            if couplings_list[i][9] != code_infra_config.get('coupling').get('9th_index_value'):
                raise_error_or_print_warning(
                    f"[Couplings error]: The 10th character of {couplings_list[i]} should be {code_infra_config.get('coupling').get('9th_index_value')}. For valid format, refer to README",
                    raise_error
                )

    def validate_ignore_single_pair_processes(self, raise_error=False):
        if not (self.ignore_single_pair_processes.lower() in code_infra_config.get("leptoquark_parameters").get("ignore_single_pair_processes_yes_values") or self.ignore_single_pair_processes.lower() in code_infra_config.get("leptoquark_parameters").get("ignore_single_pair_processes_no_values")):
            raise_error_or_print_warning(
                f"[Ignore single pair production error]: ignore_single_pair takes input either {code_infra_config.get('leptoquark_parameters').get('ignore_single_pair_processes_yes_values')} or {code_infra_config.get('leptoquark_parameters').get('ignore_single_pair_processes_no_values')}",
                raise_error
            )

    def validate_significance(self, raise_error=False):
        try:
            significance = int(self.significance)
            if significance not in code_infra_config.get('leptoquark_parameters').get('valid_significance_values'):
                raise_error_or_print_warning(
                    f"[Significance error]: Significance should be a valid number in {code_infra_config.get('leptoquark_parameters').get('valid_significance_values')}",
                    raise_error
            )
        except:
            raise_error_or_print_warning(
                "[Significance error]: Significance should be a valid number: either 1 or 2",
                raise_error
            )
        
    
    def validate_systematic_error(self, raise_error=False):
        try:
            systematic_error = float(self.systematic_error)
            if systematic_error < code_infra_config.get('leptoquark_parameters').get('systematic_error_lower_limit') or systematic_error > code_infra_config.get('leptoquark_parameters').get('systematic_error_upper_limit'):
                raise_error_or_print_warning(
                    f"[Systematic error]: [Systematic error should be a valid number from {code_infra_config.get('leptoquark_parameters').get('systematic_error_lower_limit')} to {code_infra_config.get('leptoquark_parameters').get('systematic_error_upper_limit')}.",
                    raise_error
                )
        except:
            raise_error_or_print_warning(
                f"[Systematic error]: [Systematic error should be a valid number from {code_infra_config.get('leptoquark_parameters').get('systematic_error_lower_limit')} to {code_infra_config.get('leptoquark_parameters').get('systematic_error_upper_limit')}.",
                    raise_error
            )
        

    def validate_extra_width(self, raise_error=False):
        try:
            extra_width = float(self.extra_width)
            if extra_width < 0:
                raise_error_or_print_warning(
                    "[Extra width error]: Extra Width should be a valid number",
                    raise_error
                )
        except:
            raise_error_or_print_warning(
                "[Extra width error]: Extra Width should be a valid number",
                raise_error
            )
        
            
    def validate(self):
        self.validate_leptoquark_model(raise_error=True)
        self.validate_leptoquark_mass(raise_error=True)
        self.validate_couplings(raise_error=True)
        self.validate_ignore_single_pair_processes(raise_error=True)
        self.validate_significance(raise_error=True)
        self.validate_systematic_error(raise_error=True)

    # returns whether to start calculation on input
    def interactive_input(self):
        while True:
            pr_blue_no_new_line("calq > ")
            inpt = input()
            s = inpt.split("=")
            if ":" in inpt:
                s = inpt.split(":")
            slen = len(s)
            if s[0].strip() == "import_model" and slen == 2:
                self.model = s[1].strip().upper()
                self.validate_leptoquark_model()
            elif s[0].strip() == "mass" and slen == 2:
                self.mass = s[1].strip().upper()
                self.validate_leptoquark_mass()
            elif s[0].strip() == "couplings" and slen > 1:
                self.couplings = s[1].strip().upper()
                self.validate_couplings()
            elif s[0].strip() == "ignore_single_pair" and slen == 2:
                self.ignore_single_pair_processes = s[1].strip().lower()
                self.validate_ignore_single_pair_processes()
            elif s[0].strip() == "significance" and slen == 2:
                self.significance = s[1].strip()
                self.validate_significance()
            elif s[0].strip() == "systematic_error" and slen == 2:
                self.systematic_error = s[1].strip()
                self.validate_systematic_error()
            elif s[0].strip() == "extra_width" and slen == 2:
                self.extra_width = s[1].strip()
                self.validate_extra_width() 
            elif s[0].strip() == "status":
                print(f" Leptoquark model: {self.model}")
                print(f" Leptoquark mass = {self.mass}")
                print(f" Couplings: {self.couplings}")
                print(f" Extra width = {self.extra_width}")
                print(
                    f" Ignore single & pair processes: {self.ignore_single_pair_processes}")
                print(f" Significance = {self.significance}")
                print(f" Systematic error = {self.systematic_error}")
            elif s[0].strip() == "help":
                self.print_interactive_help()
            elif s[0].strip() == "initiate":
                self.start_calculation = True
                return
                # leptoquark_parameters.couplings_values = [
                #     " ".join(["0"] * len(leptoquark_parameters.couplings))]
                leptoquark_parameters.sort_couplings_and_values()
                calculate(leptoquark_parameters, InputMode.INTERACTIVE)
            elif s[0].strip().lower() in ["exit", "q", "quit", "exit()", ".exit"]:
                return
            elif s[0].strip() == "":
                continue
            else:
                pr_red(
                    f" Command {s[0]} not recognised. Please retry or enter 'q', 'quit' or 'exit' to exit."
                )


    # this function assumes data validation has been performed
    def convert_data_to_leptoquark_model(self) -> LeptoquarkParameters:
        leptoquark_parameters = LeptoquarkParameters()

        leptoquark_parameters.model = self.model
        leptoquark_parameters.mass = float(self.mass)
        # convert couplings from string to list of strings
        leptoquark_parameters.couplings = self.couplings.strip().split(" ")
        # convert ignore_single_pair_processes
        if self.ignore_single_pair_processes.lower() in code_infra_config.get("leptoquark_parameters").get("ignore_single_pair_processes_yes_values"):
            leptoquark_parameters.ignore_single_pair_processes = True
        elif self.ignore_single_pair_processes.lower() in code_infra_config.get("leptoquark_parameters").get("ignore_single_pair_processes_no_values"):
            leptoquark_parameters = False
        #convert significance
        leptoquark_parameters.significance = int(self.significance)
        # convert Systematic error
        leptoquark_parameters.systematic_error = float(self.systematic_error)

        # convert extra width
        try:
            leptoquark_parameters.extra_width = float(self.extra_width)
        except:
            raise ValueError(
                "[Extra width error]: Extra Width should be a valid number")
    