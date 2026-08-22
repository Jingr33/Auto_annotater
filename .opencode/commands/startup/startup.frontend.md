---
description: Start the React frontend via npm
---

Start the React development server. The frontend will open in your browser automatically (typically at http://localhost:5173).

## Prerequisites

Ensure npm dependencies are installed in `src/frontend_pro/`. If not, run `npm install` in that directory first.

## Usage

Run the script:

```bash
python scripts/start_frontend.py
```

No additional arguments are needed; the script runs `npm run dev` in the frontend directory.

## Clean Termination

The script handles SIGINT/SIGTERM signals and ensures the npm process and its children are properly terminated. No orphaned processes will be left running.

## Note

The frontend expects the backend API to be running at http://localhost:8000. Start the backend separately using `startup.backend` or start both with `startup.all`.