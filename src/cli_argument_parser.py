import argparse

from backend.enums.model_type import ModelType
from backend.enums.step_type import StepType


class CLIArgumentParser:
    def __init__(self):
        self.parser = self._build_parser()

    def parse(self):
        return self.parser.parse_args()

    def _build_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            prog='main.py',
            description='Auto-annotater: annotate images with YOLO or MedSAM2, then review results.',
        )

        parser.add_argument(
            '--steps',
            nargs='+',
            required=True,
            choices=[e.value for e in StepType],
            help='Pipeline steps in order (e.g. IMAGE_LOADER ANNOTATE SELECT)',
        )

        parser.add_argument(
            '--source', default=None, help='Dataset root (images/ + labels/) or folder with images directly'
        )
        parser.add_argument('--output', required=True, help='Workspace folder for results (items/ + items.db)')

        parser.add_argument(
            '--model', choices=[e.value for e in ModelType], default=None, help='Model type for annotate step'
        )
        parser.add_argument('--model-path', default=None, help='Path to model weights (default: hardcoded per model)')

        parser.add_argument('--ssh-host', default=None, help='SSH host for remote inference')
        parser.add_argument('--ssh-port', type=int, default=22, help='SSH port (default: 22)')
        parser.add_argument('--ssh-user', default=None, help='SSH username')
        parser.add_argument('--ssh-key-path', default=None, help='Path to SSH private key')
        parser.add_argument(
            '--force-ssh-credentials',
            action='store_true',
            help='Always open Windows Credential Manager for SSH credentials',
        )
        parser.add_argument('--remote-work-dir', default='/tmp/medsam2', help='Working directory on remote server')
        parser.add_argument('--remote-model-path', default=None, help='Model path on remote server')
        parser.add_argument(
            '--remote-python', default='python3', help='Python executable on remote server (default: python3)'
        )
        parser.add_argument(
            '--inference-script', default=None, help='Path to custom inference script (default: built-in)'
        )

        parser.add_argument(
            '--only-pending',
            action='store_true',
            default=True,
            help='Show only pending items in SELECT step (default: True)',
        )

        return parser
