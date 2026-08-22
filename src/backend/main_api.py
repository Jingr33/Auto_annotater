import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import uvicorn
from dependency_injector import providers

from src.backend.api.app import app
from src.backend.api.containers import Container, register_routes
from src.runner import Runner
from src.cli_argument_parser import CLIArgumentParser
from src.backend.enums.step_type import StepType


def main() -> None:
    cli_args_parser = CLIArgumentParser()
    args = cli_args_parser.parse()

    container: Container = app.container

    if args.steps and args.output:
        steps = [StepType(s) for s in args.steps]
        if steps[-1] is not StepType.SELECT:
            args.steps.append(StepType.SELECT.value)

        runner = Runner(args)
        runner.start_pipeline()
        container.pipeline_manager.override(providers.Object(runner.manager))

    register_routes(app)

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
