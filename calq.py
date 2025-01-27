import sys

from classes.cli_argument_parser import CliArgumentParser


# calq execution starts here
def main():
    """
    Calq starting function that parses command line argument
    """
    cli_argument_parser = CliArgumentParser()
    args = cli_argument_parser.parse_args()
    cli_argument_parser.execute_args(args)


try:
    main()
except KeyboardInterrupt:
    sys.exit("\n\nKeyboardInterrupt recieved. Exiting.")
