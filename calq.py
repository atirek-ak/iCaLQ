# Calculator Imports
import sys
import argparse

from utilities.data_classes import NonInteractiveInputParameters
from utilities.welcome import welcome_message
from utilities.initiate import initiate_with_files, initiate_interactive


def run():
    """
    Starting function, accepts command line argument and passes control to further functions accordingly.
    """
    parser = argparse.ArgumentParser(description="CaLQ Usage:")

    parser.add_argument(
        "--input-card",
        type=str,
        default="",
        help="[filename]: Input card file. Format is explained in README.txt",
    )
    parser.add_argument(
        "--input-values",
        type=str,
        default="",
        help="[filename]: Input values to check from the given file. Format is explained in README.txt",
    )
    parser.add_argument(
        "--non-interactive",
        "-ni",
        action="store_true",
        help="Run in non-interactive mode. This requires input-card and input-values to be specified.",
    )
    parser.add_argument(
        "--no-banner", "-nb", action="store_true", help="CaLQ banner is not printed."
    )
    parser.add_argument(
        "--output-yes",
        type=str,
        default="calq_yes.csv",
        help="[filename]: Specify the name of output file (allowed values) (overwrites the existing file). Default: calq_yes.csv",
    )
    parser.add_argument(
        "--output-no",
        type=str,
        default="calq_no.csv",
        help="[filename]: Specify the name of output file (disallowed values) (overwrites the existing file). Default: calq_no.csv",
    )

    args = parser.parse_args()
    non_interactive_input_parameters = NonInteractiveInputParameters(
        input_card_path = args.input_card, 
        input_values_path = args.input_values, 
        output_yes_path = args.output_yes, 
        output_no_path = args.output_no, 
    )
    # input_card_file = args.input_card
    # input_vals_file = args.input_values
    # output_yes_file = args.output_yes
    # output_no_file= args.output_no

    if not args.no_banner:
        welcome_message()

    if args.non_interactive:
        non_interactive_message(
            non_interactive_input_parameters
        )
        initiate_with_files(
            non_interactive_input_parameters
        )
    else:
        initiate_interactive()


def non_interactive_message(
    non_interactive_input_parameters: NonInteractiveInputParameters,
):
    """
    Print an initial message for the non-interactive mode

    :param input_card: File path to the .card file for non-interactive input
    :param input_vals: File path to the .vals file(values file) for non-interactive input
    :param output_yes: File path of the output file (allowed values)
    :param output_no: File path of the output file (disallowed values)
    """
    if not non_interactive_input_parameters.input_card_path:
        sys.exit(
            "[Card Error]: Input Card file not specified in the expected format (mandatory for non-interactive mode). Exiting.\n"
        )
    if not non_interactive_input_parameters.input_values_path:
        sys.exit(
            "[Values Error]: Input Values file not specified in the expected format (mandatory for non-interactive mode). Exiting.\n"
        )
    print(f"Input Card file: {non_interactive_input_parameters.input_card_path}")
    print(f"Input Values file: {non_interactive_input_parameters.input_values_path}")
    print(f"Output Yes file: {non_interactive_input_parameters.output_yes_path}")
    print(f"Output No file: {non_interactive_input_parameters.output_no_path}")


try:
    run()
except KeyboardInterrupt:
    sys.exit("\n\nKeyboardInterrupt recieved. Exiting.")
