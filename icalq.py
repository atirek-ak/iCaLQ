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
    parser.add_argument(
        "--branching-fraction",
        type=float,
        default=0,
        help="Width constant to be added to the branching fraction of all processes",
    )

    args = parser.parse_args()
    input_card = args.input_card
    input_vals = args.input_values
    output_yes = args.output_yes
    output_no = args.output_no

    if not args.no_banner:
        welcome_message()

    if args.non_interactive:
        non_interactive_message(
            input_card, input_vals, output_yes, output_no
        )
        initiate_with_files(
            input_card, input_vals, output_yes, output_no
        )
    else:
        initiate_interactive()


def non_interactive_message(
    input_card: str,
    input_vals: str,
    output_yes: str,
    output_no: str,
):
    """
    Print an initial message for the non-interactive mode

    :param input_card: File path to the .card file for non-interactive input
    :param input_vals: File path to the .vals file(values file) for non-interactive input
    :param output_yes: File path of the output file (allowed values)
    :param output_no: File path of the output file (disallowed values)
    """
    if not input_card:
        sys.exit(
            "[Card Error]: Input Card file not specified in the expected format (mandatory for non-interactive mode). Exiting.\n"
        )
    if not input_vals:
        sys.exit(
            "[Values Error]: Input Values file not specified in the expected format (mandatory for non-interactive mode). Exiting.\n"
        )
    print(f"Input Card file: {input_card}")
    print(f"Input Values file: {input_vals}")
    print(f"Output Yes file: {output_yes}")
    print(f"Output No file: {output_no}")


try:
    run()
except KeyboardInterrupt:
    sys.exit("\n\nKeyboardInterrupt recieved. Exiting.")
