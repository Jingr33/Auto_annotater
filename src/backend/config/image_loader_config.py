from dataclasses import dataclass
from typing import Optional

from backend.enums.model_type import ModelType


@dataclass
class ImageLoaderConfig:
    source_path: str
    output_path: str
    model_type: Optional[ModelType] = None
