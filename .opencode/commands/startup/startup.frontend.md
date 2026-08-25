---
description: Start the React frontend via npm
---

Start the React development server. The frontend will open in your browser automatically (typically at http://localhost:5173).

## Prerequisites

Ensure npm dependencies are installed in `src/frontend_pro/`. If not, run `npm install` in that directory first.

## Usage

```bash
cd src/frontend_pro && npm run dev
```

## Note

The frontend expects the backend API to be running at http://localhost:8000. Start the backend separately using `startup.backend` or start both with `startup.all`.
