import sys


from classes.config import file_paths_config, code_infra_config
from classes.leptoquark_parameters_string_input import LeptoquarkParametersStringInput
from helper.miscellaneous import strip_comments_and_spaces
        

class NonInteractiveInputParameters:
    """
    class for non-interactive mode input parameters to be taken from the user

    :param input_card_path: File path to the .card file for non-interactive input
    :param input_values_path: File path to the .vals file(values file) for non-interactive input
    :param output_yes_path: File path of the output file (allowed values)
    :param output_no_path: File path of the output file (disallowed values)
    """

    def __init__(
        self,
        input_card_path: str = "",
        input_values_path: str = "",
        output_yes_path: str = "",
        output_no_path: str = "",
        output_common_path: str = "",
        card_data: LeptoquarkParametersStringInput = LeptoquarkParametersStringInput(),
    ):
        self.input_card_path = input_card_path
        self.input_values_path = input_values_path
        self.output_yes_path = output_yes_path
        self.output_no_path = output_no_path
        self.output_common_path = output_common_path
        self.card_data = card_data

    def print_initial_message(self):
        print(
            f"Input Card file: {self.input_card_path}")
        print(
            f"Input Values file: {self.input_values_path}")
        print(
            f"Output Yes file: {self.output_yes_path}")
        print(f"Output No file: {self.output_no_path}")
        print(
            f"Output Common file: {self.output_common_path}")

    def validate(self):
        if not self.non_interactive_input_parameters.input_values_path:
            self.non_interactive_input_parameters.input_values_path = file_paths_config.get("default_coupling_values_input")
            with open(
                self.non_interactive_input_parameters.input_card_path, encoding="utf8"
            ) as c:
                input_card_lines = c.readlines()
                random_points = strip_comments_and_spaces(input_card_lines[code_infra_config.get("non_interactive_input").get("card").get("number_of_random_points_index")])
                if random_points == "0":
                    sys.exit(
                        "[Values error]: Input Values file not specified & random points is set to zero. Exiting.\n"
                    )

    def create_output_files_if_not_present(self):
        if not self.non_interactive_input_parameters.output_yes_path:
            self.non_interactive_input_parameters.output_yes_path = file_paths_config.get("default_coupling_output_values_yes")
        if not self.non_interactive_input_parameters.output_no_path:
            self.non_interactive_input_parameters.output_no_path = file_paths_config.get("default_coupling_output_values_no")
        if not self.non_interactive_input_parameters.output_common_path:
            self.non_interactive_input_parameters.output_common_path = file_paths_config.get("default_coupling_output_values_common")
