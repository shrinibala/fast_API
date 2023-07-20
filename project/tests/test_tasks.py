from worker import create_task
from unittest.mock import patch
import json

def test_home(test_app):
    response = test_app.get("/")
    assert response.status_code == 200


def test_task():
    assert create_task.run(1)
    assert create_task.run(2)
    assert create_task.run(3)

@patch("worker.create_task.run")
def test_mock_task(mock_run):
    assert create_task.run(1)
    create_task.run.assert_called_once_with(1)

    assert create_task.run(2)
    assert create_task.run.call_count == 2

    assert create_task.run(3)
    assert create_task.run.call_count == 3

def test_task_status(test_app):
    response = test_app.post(
        "/tasks",
        data=json.dumps({"type": 1})
    )
    assert response.status_code == 200  # Ensure the response status is 200 OK
    content = response.json()
    task_id = content.get("task_id")  # Use .get() to handle cases when "task_id" might be missing
    assert task_id is not None  # Check that "task_id" is present and not None

    response = test_app.get(f"tasks/{task_id}")
    content = response.json()
    assert content == {"task_id": task_id, "task_status": "PENDING", "task_result": None}
    assert response.status_code == 200

    while content["task_status"] == "PENDING":
        response = test_app.get(f"tasks/{task_id}")
        content = response.json()
    assert content == {"task_id": task_id, "task_status": "SUCCESS", "task_result": True}