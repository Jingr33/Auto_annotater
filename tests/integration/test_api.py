import os
import tempfile

from fastapi.testclient import TestClient

from backend.api.app import create_app
from backend.api.containers import Container
from backend.pipeline_engine.data_manager import DataManager
from backend.pipeline_engine.pipeline_manager import PipelineManager


def _create_test_client(tmpdir: str) -> tuple[TestClient, DataManager, PipelineManager]:
    workspace = os.path.join(tmpdir, 'workspace')
    dm = DataManager(workspace)

    for i in range(2):
        img_path = os.path.join(tmpdir, f'img{i}.jpg')
        with open(img_path, 'w') as f:
            f.write(f'fake image {i}')
        dm.import_image(img_path)
    dm.close()

    manager = PipelineManager(
        source_step=None,
        pipeline_steps=[],
        workspace=workspace,
        with_frontend=True,
        only_pending=False,
    )

    app = create_app()
    app.container = Container(pipeline_manager=manager)
    app.include_router(
        app.container.pipeline_controller().router,
        prefix='/api',
    )

    client = TestClient(app)
    return client, dm, manager


def test_api_get_items_empty() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        client, dm, manager = _create_test_client(tmpdir)
        response = client.get('/api/items')
        assert response.status_code == 200
        data = response.json()
        assert 'items' in data
        assert data['total'] == 2
        manager.finalize()


def test_api_get_pipeline_status() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        client, dm, manager = _create_test_client(tmpdir)
        response = client.get('/api/pipeline/status')
        assert response.status_code == 200
        data = response.json()
        assert 'is_waiting' in data
        assert 'is_finished' in data
        assert 'total' in data
        manager.finalize()


def test_api_accept_without_item() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        client, dm, manager = _create_test_client(tmpdir)
        manager.start()
        manager.wait()
        manager.accept()
        response = client.post('/api/pipeline/accept')
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        manager.finalize()


def test_api_reject_without_item() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        client, dm, manager = _create_test_client(tmpdir)
        manager.start()
        manager.wait()
        manager.reject()
        response = client.post('/api/pipeline/reject')
        assert response.status_code == 200
        data = response.json()
        assert data['success'] is True
        manager.finalize()
