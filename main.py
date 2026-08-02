import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.parser import build_parser
from src.runner import run


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
