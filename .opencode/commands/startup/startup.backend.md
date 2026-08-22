---
description: Start the backend API server with optional parameters and license mode
---

Start the backend API server. The server will run on http://0.0.0.0:8000.

## License Configuration

Before starting, the script reads the license mode from `.opencode/license_mode` (if exists) or uses the default `open` mode. You can override the license mode by passing `--license-mode open` or `--license-mode pro`.

## Usage

Run the script with optional arguments that are forwarded to `main_api.py`:

```bash
python scripts/start_backend.py [--license-mode open|pro] [MAIN_API_ARGS...]
```

If no arguments are provided, the backend starts with default parameters (`--steps SELECT --output ./workspace`).

## Clean Termination

The script handles SIGINT/SIGTERM signals and ensures the child process is properly terminated. No orphaned processes will be left running.

## Example

```bash
python scripts/start_backend.py --license-mode pro --steps LOAD ANNOTATE SELECT --source ./dataset --output ./workspace
```
