from fastapi.testclient import TestClient
from main import app, queue
# import pytest

client = TestClient(app)

def test_webhook_adds_to_queue():
    # 1. Define the mock GitHub webhook payload
    payload = {
        "issue": {
            "title": "Test Issue",
            "body": "This is a test malware rule."
        }
    }
    
    # 2. Check the queue size before
    initial_queue_size = len(queue.tasks)
    
    # 3. Hit the webhook endpoint
    response = client.post(
        "/webhookpr",
        json=payload,
        headers={"x-github-event": "issues"}
    )
    
    # 4. Assert the endpoint succeeded
    assert response.status_code == 200
    assert response.json() == {"message": "Task queued", "task_id": initial_queue_size + 1}
    
    # 5. Assert the queue actually grew
    assert len(queue.tasks) == initial_queue_size + 1
    assert queue.tasks[-1].issue_txt == "Title: Test Issue\nBody:\nThis is a test malware rule."