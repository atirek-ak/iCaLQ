# Calculator Imports
import sys
import argparse

from utilities.welcome import welcome_message
from utilities.initiate import initiate_with_files, initiate_interactive


def run():
    """
    Starting function, accepts command line argument and passes control to further functions accordingly.
    """
    parser = argparse.ArgumentParser(description="iCaLQ Usage:")

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
        "--no-banner", "-nb", action="store_true", help="iCaLQ banner is not printed."
    )
    parser.add_argument(
        "--output-yes",
        type=str,
        default="icalq_yes.csv",
        help="[filename]: Specify the name of output file (allowed values) (overwrites the existing file). Default: icalq_yes.csv",
    )
    parser.add_argument(
        "--output-no",
        type=str,
        default="icalq_no.csv",
        help="[filename]: Specify the name of output file (disallowed values) (overwrites the existing file). Default: icalq_no.csv",
    )

    args = parser.parse_args()
    input_card_file = args.input_card
    input_vals_file = args.input_values
    output_yes_file = args.output_yes
    output_no_file= args.output_no

    if not args.no_banner:
        welcome_message()

    if args.non_interactive:
        non_interactive_message(
            input_card_file, input_vals_file, output_yes_file, output_no_file
        )
        initiate_with_files(
            input_card_file, input_vals_file, output_yes_file, output_no_file
        )
    else:
        initiate_interactive()


def non_interactive_message(
    input_card_file: str,
    input_vals_file: str,
    output_yes_file: str,
    output_no_file: str,
):
    """
    Print an initial message for the non-interactive mode

    :param input_card: File path to the .card file for non-interactive input
    :param input_vals: File path to the .vals file(values file) for non-interactive input
    :param output_yes: File path of the output file (allowed values)
    :param output_no: File path of the output file (disallowed values)
    """
    if not input_card_file:
        sys.exit(
            "[Card Error]: Input Card file not specified in the expected format (mandatory for non-interactive mode). Exiting.\n"
        )
    if not input_vals_file:
        sys.exit(
            "[Values Error]: Input Values file not specified in the expected format (mandatory for non-interactive mode). Exiting.\n"
        )
    print(f"Input Card file: {input_card_file}")
    print(f"Input Values file: {input_vals_file}")
    print(f"Output Yes file: {output_yes_file}")
    print(f"Output No file: {output_no_file}")


try:
    run()
except KeyboardInterrupt:
    sys.exit("\n\nKeyboardInterrupt recieved. Exiting.")
