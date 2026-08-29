from dataclasses import dataclass, field

from config import WORKSPACE_DIR


@dataclass
class FrameDTO:
    item_id: str
    workspace: str = field(default=WORKSPACE_DIR)
