import sys
import os
import threading

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import uvicorn

from src.backend.api.app import app
from src.backend.api.routes import set_pipeline_manager
from src.runner import Runner
from src.cli_argument_parser import CLIArgumentParser


def main() -> None:
    cli_args_parser = CLIArgumentParser()
    args = cli_args_parser.parse()

    runner = Runner(args)
    runner.start_pipeline()

    set_pipeline_manager(runner.manager)

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
