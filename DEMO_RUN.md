# Auto-Annotater

## Spuštění

```bash
python main.py --steps STEP1 [STEP2 ...] --output WORKSPACE [parametry]
```

## Pipeline steps

| Step | Význam |
|---|---|
| `LOAD` | Načte obrázky ze zdroje do workspace |
| `ANNOTATE` | Spustí model (YOLO/MedSAM2) |
| `SELECT` | Otevře GUI pro výběr |

## Parametry

### Povinné

| Parametr | Popis |
|---|---|
| `--steps` | Pipeline kroky v pořadí (např. `LOAD ANNOTATE SELECT`) |
| `--output` | Workspace složka pro výsledky (`items/` + `items.db`) |

### Volitelné — model

| Parametr | Popis | Default |
|---|---|---|
| `--source` | Dataset root (`images/` + `labels/`) nebo složka s obrázky | — |
| `--model` | Typ modelu (`YOLO`, `MEDSAM2`) | — |
| `--model-path` | Cesta k vahám modelu | hardcoded |

### Volitelné — SSH (pro remote běh)

| Parametr | Popis | Default |
|---|---|---|
| `--ssh-host` | SSH host | — |
| `--ssh-port` | SSH port | `22` |
| `--ssh-user` | SSH uživatel | — |
| `--ssh-key-path` | Cesta k SSH klíči | — |
| `--remote-work-dir` | Pracovní složka na serveru | `/tmp/medsam2` |
| `--remote-model-path` | Cesta k modelu na serveru | — |
| `--remote-python` | Python na serveru | `python3` |

## Příklady použití

### Batch anotace (YOLO)

```bash
python main.py --steps LOAD ANNOTATE \
    --source ./dataset \
    --output ./workspace \
    --model YOLO
```

### Anotace + výběr v reálném čase

```bash
python main.py --steps LOAD ANNOTATE SELECT \
    --source ./dataset \
    --output ./workspace \
    --model YOLO
```

### Jen výběr z existujícího workspace

```bash
python main.py --steps SELECT --output ./workspace
```

### MedSAM2 remote

```bash
python main.py --steps LOAD ANNOTATE SELECT \
    --source ./dataset \
    --output ./workspace \
    --model MEDSAM2 \
    --ssh-host 192.168.1.100 \
    --ssh-user lab \
    --ssh-key-path ~/.ssh/id_rsa \
    --remote-python /opt/venv/medsam/bin/python3
```

### MedSAM2 remote s vlastními vahami

```bash
python main.py --steps LOAD ANNOTATE SELECT \
    --source ./dataset \
    --output ./workspace \
    --model MEDSAM2 \
    --model-path ./modely/medsam2.pth \
    --ssh-host 192.168.1.100 \
    --ssh-user lab \
    --ssh-key-path ~/.ssh/id_rsa \
    --remote-work-dir /data/tmp \
    --remote-model-path /models/medsam2.pth \
    --remote-python /opt/venv/medsam/bin/python3
```

## Workspace struktura

```
<output>/
├── items/
│   └── <item_id>/
│       ├── original.jpg
│       ├── yolo.txt
│       └── sam_polygon.txt
└── items.db
```

## Dataset formáty

### YOLO (plochý)

```
dataset/
├── img001.jpg
├── img002.jpg
└── ...
```

### MedSAM2 (images/ + labels/)

```
dataset/
├── images/
│   ├── img001.jpg
│   └── img002.jpg
└── labels/
    ├── img001.txt
    └── img002.txt
```

## Klávesové zkratky (SELECT)

| Klávesa | Akce |
|---|---|
| `D` | Accept |
| `A` | Reject |
| `S` | Skip |
| `W` | Back |
| `Escape` | Konec |
