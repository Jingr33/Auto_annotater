#!/usr/bin/env python3
"""
Wrapper script for starting both backend and frontend simultaneously.

Ensures clean termination of all child processes.
"""

import signal
import subprocess
import sys
from pathlib import Path
from types import FrameType


def main() -> None:
    """Main entry point."""
    # Start backend
    backend_cmd = [sys.executable, str(Path(__file__).parent / 'start_backend.py')]
    backend = subprocess.Popen(backend_cmd)

    # Start frontend
    frontend_cmd = [sys.executable, str(Path(__file__).parent / 'start_frontend.py')]
    frontend = subprocess.Popen(frontend_cmd)

    # Signal handler to terminate both children
    def signal_handler(signum: int, frame: FrameType) -> None:
        backend.terminate()
        frontend.terminate()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Wait for both processes
    try:
        backend.wait()
        frontend.wait()
    except KeyboardInterrupt:
        backend.terminate()
        frontend.terminate()
        backend.wait()
        frontend.wait()


if __name__ == '__main__':
    main()
