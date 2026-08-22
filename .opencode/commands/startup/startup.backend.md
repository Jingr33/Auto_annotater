Start the backend API server. The server will run on http://0.0.0.0:8000.

## Usage

Run in a new console window:

```bash
cmd /c start cmd /k "cd /d <PROJECT_DIR> && python main.py --steps LOAD ANNOTATE SELECT --output ./workspace"
```

### Parameters

- `--steps` — Pipeline steps in order (LOAD, ANNOTATE, SELECT)
- `--output` — Workspace folder for results
- `--source` — Dataset root (optional)
- `--model` — Model type: YOLO or MEDSAM2 (optional)
- `--model-path` — Path to model weights (optional)

### Example

```bash
cmd /c start cmd /k "cd /d C:\path\to\project && python main.py --steps LOAD ANNOTATE SELECT --source ./data --output ./workspace --model YOLO"
```
