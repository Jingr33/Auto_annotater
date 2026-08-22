---
description: Start both frontend and backend simultaneously
---

Start both the backend API server and the React frontend concurrently. This is the recommended way to launch the full application.

## License Configuration

The backend license mode is read from `.opencode/license_mode` (default `open`). You can override it by passing `--license-mode open|pro` as the first argument.

## Usage

Run the script with optional license mode:

```bash
python scripts/start_all.py [--license-mode open|pro]
```

Any additional arguments after `--license-mode` are forwarded to the backend script. The frontend does not accept additional arguments.

## Clean Termination

The script handles SIGINT/SIGTERM signals and ensures both the backend and frontend processes (and their children) are properly terminated. No orphaned processes will be left running.

## Example

```bash
python scripts/start_all.py --license-mode pro
```

This starts the backend with pro license and the React frontend. The frontend will open in your browser automatically.