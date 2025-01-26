# Calculator Imports
import argparse
import sys

from utilities.cli_argument_parser import (initialise_cli_argument_parser,
                                           parse_cli_arguments_and_execute)
from utilities.constants import default_input_file_path
from utilities.data_classes import NonInteractiveInputParameters
from utilities.initiate.interactive.interactive import initiateInteractive
from utilities.initiate.non_interactive.non_interactive import \
    initiateNonInteractive


# calq execution starts here
def main():
    """
    Calq starting function that parses command line argument
    """
    cli_argument_parser = initialise_cli_argument_parser()
    parse_cli_arguments_and_execute(cli_argument_parser)


def nonInteractiveMessage(
    non_interactive_input_parameters: NonInteractiveInputParameters,
):
    """
    Print an initial message for non-interactive mode
    """
    if not non_interactive_input_parameters.input_card_path:
        sys.exit(
            "[Card error]: Input Card file not specified in the expected format (mandatory for non-interactive mode). Exiting.\n"
        )
    if not non_interactive_input_parameters.input_values_path:
        non_interactive_input_parameters.input_values_path = default_input_file_path
        with open(
            non_interactive_input_parameters.input_card_path, encoding="utf8"
        ) as c:
            input_card_lines = c.readlines()
            random_points = input_card_lines[7].split("#")[0].strip()
            if random_points == "0":
                sys.exit(
                    "[Values error]: Input Values file not specified & random points is set to zero. Exiting.\n"
                )
    print(
        f"Input Card file: {non_interactive_input_parameters.input_card_path}")
    print(
        f"Input Values file: {non_interactive_input_parameters.input_values_path}")
    print(
        f"Output Yes file: {non_interactive_input_parameters.output_yes_path}")
    print(f"Output No file: {non_interactive_input_parameters.output_no_path}")
    print(
        f"Output Common file: {non_interactive_input_parameters.output_common_path}")


try:
    main()
except KeyboardInterrupt:
    sys.exit("\n\nKeyboardInterrupt recieved. Exiting.")
