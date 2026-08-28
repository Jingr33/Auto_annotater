from dataclasses import dataclass

from src.backend.api.dto.annotation_item_dto import AnnotationItemDTO


@dataclass
class AnnotationItemListResponseDTO:
    items: list[AnnotationItemDTO]
    total: int
