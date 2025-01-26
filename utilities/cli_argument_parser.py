import argparse


def initialise_cli_argument_parser() -> argparse.ArgumentParser:
    # argparser for CLI arguments
    parser = argparse.ArgumentParser(description="CaLQ Usage:")
    # for choosing interactive/non-interactive modes
    parser.add_argument(
        "--non-interactive",
        "-ni",
        action="store_true",
        help="Run in non-interactive mode. This requires input-card and input-values to be specified.",
    )
    # wheter to display banner from banner.txt
    parser.add_argument(
        "--no-banner", "-nb", action="store_true", help="CaLQ banner is not printed."
    )
    # non-interactive mode parameters
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
    parser.add_argument(
        "--output-common",
        type=str,
        default="calq_common.csv",
        help="[filename]: Specify the name of output file (overwrites the existing file). Default: calq_common.csv",
    )
    return parser


def parse_cli_arguments_and_execute(parser: argparse.ArgumentParser):
    args = parser.parse_args()

    if not args.no_banner:
        printBanner()

    if args.non_interactive:
        non_interactive_input_parameters = NonInteractiveInputParameters(
            input_card_path=args.input_card,
            input_values_path=args.input_values,
            output_yes_path=args.output_yes,
            output_no_path=args.output_no,
            output_common_path=args.output_common,
        )
        nonInteractiveMessage(non_interactive_input_parameters)
        initiateNonInteractive(non_interactive_input_parameters)
    else:
        initiateInteractive()
