from dataclasses import dataclass


@dataclass
class AnnotationItemDTO:
    id: str
    status: str
    created_at: str
    updated_at: str
