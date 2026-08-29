from backend.pipeline_engine.frame_dto import FrameDTO


def test_frame_dto_creation() -> None:
    dto = FrameDTO(item_id='test_item', workspace='/workspace')
    assert dto.item_id == 'test_item'
    assert dto.workspace == '/workspace'


def test_frame_dto_equality() -> None:
    dto1 = FrameDTO(item_id='item1', workspace='/ws1')
    dto2 = FrameDTO(item_id='item1', workspace='/ws1')
    assert dto1 == dto2


def test_frame_dto_inequality() -> None:
    dto1 = FrameDTO(item_id='item1', workspace='/ws1')
    dto2 = FrameDTO(item_id='item2', workspace='/ws1')
    assert dto1 != dto2
