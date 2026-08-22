#!/usr/bin/env python3
"""
Wrapper script for starting the React frontend via npm.

Ensures clean termination of the npm process and its children.
"""

import os
import signal
import subprocess
from pathlib import Path
from types import FrameType

FRONTEND_DIR = Path(__file__).parent.parent / 'src' / 'frontend_pro'


def main() -> None:
    """Main entry point."""
    # Ensure we are in the frontend directory
    os.chdir(FRONTEND_DIR)

    # Start npm run dev
    npm = 'npm.cmd' if os.name == 'nt' else 'npm'
    cmd = [npm, 'run', 'dev']
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
