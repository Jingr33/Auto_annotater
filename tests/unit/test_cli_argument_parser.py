import sys

from src.cli_argument_parser import CLIArgumentParser


def test_cli_parser_creates_parser() -> None:
    parser = CLIArgumentParser()
    assert parser.parser is not None


def test_cli_parser_has_steps_argument() -> None:
    parser = CLIArgumentParser()
    args = parser.parser.parse_args(['--steps', 'LOAD', 'ANNOTATE', '--source', '/data', '--output', '/output'])
    assert args.steps == ['LOAD', 'ANNOTATE']


def test_cli_parser_has_model_argument() -> None:
    parser = CLIArgumentParser()
    args = parser.parser.parse_args([
        '--steps', 'LOAD', 'ANNOTATE',
        '--source', '/data',
        '--output', '/output',
        '--model', 'YOLO',
    ])
    assert args.model == 'YOLO'


def test_cli_parser_has_ssh_arguments() -> None:
    parser = CLIArgumentParser()
    args = parser.parser.parse_args([
        '--steps', 'LOAD', 'ANNOTATE',
        '--source', '/data',
        '--output', '/output',
        '--ssh-host', 'example.com',
        '--ssh-port', '2222',
        '--ssh-user', 'admin',
    ])
    assert args.ssh_host == 'example.com'
    assert args.ssh_port == 2222
    assert args.ssh_user == 'admin'
