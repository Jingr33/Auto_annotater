#!/usr/bin/env python3
"""
Wrapper script for starting the backend API server.

Handles license configuration and ensures clean termination.
"""

import argparse
import signal
import subprocess
import sys
from pathlib import Path
from types import FrameType

LICENSE_CONFIG_PATH = Path(__file__).parent.parent / 'license_config.py'
LICENSE_MODE_PATH = Path(__file__).parent.parent / '.opencode' / 'license_mode'


def read_license_mode() -> str:
    """Read license mode from configuration file, default to 'open'."""
    if LICENSE_MODE_PATH.exists():
        mode = LICENSE_MODE_PATH.read_text().strip().lower()
        if mode in ('open', 'pro'):
            return mode
    return 'open'


def write_license_config(mode: str) -> None:
    """Write license configuration to license_config.py."""
    pro_license = mode == 'pro'
    content = f"""# license_config.py
# Temporary configuration file for licensing
# TODO: Remove this file when real licensing is implemented

PRO_LICENSE = {pro_license}  # Set to False to test unlicensed behavior
"""
    LICENSE_CONFIG_PATH.write_text(content)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description='Start the backend API server with license configuration.')
    parser.add_argument(
        '--license-mode',
        choices=['open', 'pro'],
        default=None,
        help='License mode (overrides config file)',
    )
    # Forward remaining arguments to main_api.py
    args, remaining = parser.parse_known_args()
    args.remaining = remaining
    return args


def main() -> None:
    """Main entry point."""
    args = parse_args()

    # Determine license mode
    mode = args.license_mode or read_license_mode()
    write_license_config(mode)

    # Build command to start the backend API server
    cmd = [sys.executable, 'main_api.py'] + args.remaining

    # Start child process
    child = subprocess.Popen(cmd)

    # Signal handler to forward termination signals to child
    def signal_handler(signum: int, frame: FrameType) -> None:
        child.terminate()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        child.wait()
    except KeyboardInterrupt:
        child.terminate()
        child.wait()


if __name__ == '__main__':
    main()
