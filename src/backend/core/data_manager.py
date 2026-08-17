import os
import shutil
import sqlite3
from datetime import datetime, timezone
from typing import List, Optional

from backend.annotations.annotation_parser import AnnotationParser
from backend.annotations import Annotation
from backend.enums.annotation_label import AnnotationLabel
from backend.enums.image_prediction_status import ImagePredictionStatus


class DataManager:
    def __init__(self, workspace: str):
        self.workspace = os.path.abspath(workspace)
        os.makedirs(os.path.join(self.workspace, "items"), exist_ok=True)
        self._conn = sqlite3.connect(os.path.join(self.workspace, "items.db"), check_same_thread=False)
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._init_db()

    def _init_db(self) -> None:
        default_status = ImagePredictionStatus.PENDING.value
        self._conn.execute(f"""
            CREATE TABLE IF NOT EXISTS items (
                id TEXT PRIMARY KEY,
                status TEXT NOT NULL DEFAULT '{default_status}',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        self._conn.commit()

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def _item_path(self, item_id: str) -> str:
        return os.path.join(self.workspace, "items", item_id)

    def image_path(self, item_id: str) -> str:
        return os.path.join(self._item_path(item_id), "original.jpg")

    def import_image(self, source_path: str, item_id: Optional[str] = None) -> str:
        if item_id is None:
            item_id = os.path.splitext(os.path.basename(source_path))[0]
        item_dir = self._item_path(item_id)
        os.makedirs(item_dir, exist_ok=True)
        shutil.copy2(source_path, os.path.join(item_dir, "original.jpg"))
        now = self._now()
        self._conn.execute(
            "INSERT OR IGNORE INTO items (id, status, created_at, updated_at) VALUES (?, ?, ?, ?)",
            (item_id, ImagePredictionStatus.PENDING.value, now, now),
        )
        self._conn.commit()
        return item_id

    def save_annotation(self, item_id: str, annotations: List[Annotation], label: AnnotationLabel = AnnotationLabel.YOLO) -> str:
        path = os.path.join(self._item_path(item_id), f"{label.value}.txt")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(AnnotationParser.format_string(annotations))
        return path

    def load_annotation(self, item_id: str, label: AnnotationLabel = AnnotationLabel.YOLO) -> List[Annotation]:
        path = os.path.join(self._item_path(item_id), f"{label.value}.txt")
        return AnnotationParser.load(path)

    def set_status(self, item_id: str, status: ImagePredictionStatus) -> None:
        self._conn.execute(
            "UPDATE items SET status=?, updated_at=? WHERE id=?",
            (status.value, self._now(), item_id),
        )
        self._conn.commit()

    def get_items(self, status: Optional[ImagePredictionStatus] = None) -> List[dict]:
        if status:
            rows = self._conn.execute(
                "SELECT id, status, created_at, updated_at FROM items WHERE status=? ORDER BY created_at",
                (status.value,),
            )
        else:
            rows = self._conn.execute(
                "SELECT id, status, created_at, updated_at FROM items ORDER BY created_at"
            )
        return [dict(r) for r in rows.fetchall()]

    def close(self) -> None:
        self._conn.close()
