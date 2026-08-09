from dataclasses import dataclass
from datetime import datetime


@dataclass
class ItemDTO:
    id: str
    status: str
    created_at: str
    updated_at: str


@dataclass
class ItemListResponseDTO:
    items: list[ItemDTO]
    total: int
