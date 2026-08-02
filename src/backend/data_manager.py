import os
import shutil
import sqlite3
from datetime import datetime, timezone
from typing import List, Optional

from backend.annotation_parser import format_annotations_string, load_annotations
from backend.annotations import Annotation


class DataManager:
    def __init__(self, workspace: str):
        self.workspace = os.path.abspath(workspace)
        os.makedirs(os.path.join(self.workspace, "items"), exist_ok=True)
        self._conn = sqlite3.connect(os.path.join(self.workspace, "items.db"))
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._init_db()

    def _init_db(self) -> None:
        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id TEXT PRIMARY KEY,
                status TEXT NOT NULL DEFAULT 'pending',
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
            "INSERT OR IGNORE INTO items (id, status, created_at, updated_at) VALUES (?, 'pending', ?, ?)",
            (item_id, now, now),
        )
        self._conn.commit()
        return item_id

    def save_annotation(self, item_id: str, annotations: List[Annotation], label: str = "yolo") -> str:
        path = os.path.join(self._item_path(item_id), f"{label}.txt")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(format_annotations_string(annotations))
        return path

    def load_annotation(self, item_id: str, label: str = "yolo") -> List[Annotation]:
        path = os.path.join(self._item_path(item_id), f"{label}.txt")
        return load_annotations(path)

    def set_status(self, item_id: str, status: str) -> None:
        self._conn.execute(
            "UPDATE items SET status=?, updated_at=? WHERE id=?",
            (status, self._now(), item_id),
        )
        self._conn.commit()

    def get_items(self, status: Optional[str] = None) -> List[dict]:
        if status:
            rows = self._conn.execute(
                "SELECT id, status, created_at, updated_at FROM items WHERE status=? ORDER BY created_at",
                (status,),
            )
        else:
            rows = self._conn.execute(
                "SELECT id, status, created_at, updated_at FROM items ORDER BY created_at"
            )
        return [dict(r) for r in rows.fetchall()]

    def get_item(self, item_id: str) -> Optional[dict]:
        row = self._conn.execute(
            "SELECT id, status, created_at, updated_at FROM items WHERE id=?", (item_id,)
        ).fetchone()
        return dict(row) if row else None

    def remove_item(self, item_id: str) -> None:
        item_dir = self._item_path(item_id)
        if os.path.isdir(item_dir):
            shutil.rmtree(item_dir)
        self._conn.execute("DELETE FROM items WHERE id=?", (item_id,))
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()
