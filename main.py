import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.cli_argument_parser import CLIArgumentParser
from src.runner import Runner


def main() -> None:
    cli_args_parser = CLIArgumentParser()
    args = cli_args_parser.parse()
    Runner(args).run()


if __name__ == "__main__":
    main()
