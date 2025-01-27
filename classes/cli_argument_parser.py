import argparse

from calculate import calculate
from classes.non_interactive_input_params import NonInteractiveInputParameters
from classes.leptoquark_parameters_string_input import LeptoquarkParametersStringInput
from utilities.constants import InputMode
from utilities.output import print_welcome_banner

class CliArgumentParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="CaLQ Usage:")
        # for choosing interactive/non-interactive modes
        self.parser.add_argument(
            "--non-interactive",
            "-ni",
            action="store_true",
            help="Run in non-interactive mode. This requires input-card and input-values to be specified.",
        )
        # wheter to display banner from banner.txt
        self.parser.add_argument(
            "--no-banner", "-nb", action="store_true", help="CaLQ banner is not printed."
        )
        # non-interactive mode parameters
        self.parser.add_argument(
            "--input-card",
            type=str,
            default="",
            help="[filename]: Input card file. Format is explained in README.txt",
        )
        self.parser.add_argument(
            "--input-values",
            type=str,
            default="",
            help="[filename]: Input values to check from the given file. Format is explained in README.txt",
        )
        self.parser.add_argument(
            "--output-yes",
            type=str,
            default="calq_yes.csv",
            help="[filename]: Specify the name of output file (allowed values) (overwrites the existing file). Default: calq_yes.csv",
        )
        self.parser.add_argument(
            "--output-no",
            type=str,
            default="calq_no.csv",
            help="[filename]: Specify the name of output file (disallowed values) (overwrites the existing file). Default: calq_no.csv",
        )
        self.parser.add_argument(
            "--output-common",
            type=str,
            default="calq_common.csv",
            help="[filename]: Specify the name of output file (overwrites the existing file). Default: calq_common.csv",
        )

    def parse_args(self):
        return self.parser.parse_args()
    
    def execute_args(self, args):
        if not args.no_banner:
            print_welcome_banner()

        if args.non_interactive:
            non_interactive_input_parameters = NonInteractiveInputParameters(
                input_card_path=args.input_card,
                input_values_path=args.input_values,
                output_yes_path=args.output_yes,
                output_no_path=args.output_no,
                output_common_path=args.output_common,
            )
            non_interactive_input_parameters.validate()
            non_interactive_input_parameters.create_output_files_if_not_present()
            non_interactive_input_parameters.card_data.read_data_from_input_file(non_interactive_input_parameters.input_card_path)
            non_interactive_input_parameters.card_data.validate()
            non_interactive_input_parameters.card_data.validate_and_write_random_points_to_input_values_file(non_interactive_input_parameters.input_values_path, len(leptoquark_parameters.couplings))

            leptoquark_parameters = non_interactive_input_parameters.card_data.convert_data_to_leptoquark_model()
            leptoquark_parameters.read_non_interactive_input_coupling_values_from_file()
            leptoquark_parameters.sort_couplings_and_values()

            non_interactive_input_parameters.print_initial_message()
            calculate(
                leptoquark_parameters,
                InputMode.NONINTERACTIVE,
                non_interactive_input_parameters,
            )
        else:
            leptoquark_parameters_string_input = LeptoquarkParametersStringInput()
            leptoquark_parameters_string_input.print_initial_message()
            leptoquark_parameters_string_input.interactive_input()
