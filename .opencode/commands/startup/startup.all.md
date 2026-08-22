Start both the backend API server and the React frontend concurrently.

## Backend

From the project root:

```bash
python main.py --steps LOAD ANNOTATE SELECT --output ./workspace
```

## Frontend

```bash
cd src/frontend_pro && npm run dev
```

## Both

Run both commands in separate terminals.
