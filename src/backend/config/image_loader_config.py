from dataclasses import dataclass

from src.backend.enums.model_type import ModelType


@dataclass
class ImageLoaderConfig:
    source_path: str
    output_path: str
    model_type: ModelType | None = None
