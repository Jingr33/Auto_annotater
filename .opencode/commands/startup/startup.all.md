---
description: Start both frontend and backend simultaneously
---

Start both the backend API server and the React frontend concurrently.

## Backend

From the project root:

```bash
python src/backend/main_api.py --steps LOAD ANNOTATE SELECT --output ./workspace
```

## Frontend

```bash
cd src/frontend_pro && npm run dev
```

## Both

Run both commands in separate terminals.
