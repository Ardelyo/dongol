#!/usr/bin/env python3
"""Test DONGOL API"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from api.server import app
from fastapi.testclient import TestClient
import json

client = TestClient(app)

print("=== Testing DONGOL API ===\n")

# Test root
print("GET /")
r = client.get("/")
print(f"  Status: {r.status_code}")
print(f"  Response: {r.json()}\n")

# Test stats
print("GET /stats")
r = client.get("/stats")
print(f"  Status: {r.status_code}")
print(f"  Response: {json.dumps(r.json(), indent=2)}\n")

# Test create task
print("POST /tasks")
r = client.post("/tasks", json={
    "name": "API Test",
    "content": "Testing the DONGOL API",
    "auto_chunk": True,
    "chunk_size": 100,
    "parallel": True
})
print(f"  Status: {r.status_code}")
task = r.json()
task_id = task["id"]
print(f"  Created task: {task_id}")
print(f"  Chunks: {task['chunk_count']}\n")

# Test list tasks
print("GET /tasks")
r = client.get("/tasks")
print(f"  Status: {r.status_code}")
print(f"  Total tasks: {len(r.json())}\n")

# Test execute
print(f"POST /tasks/{task_id[:8]}.../execute")
r = client.post(f"/tasks/{task_id}/execute")
print(f"  Status: {r.status_code}")
result = r.json()
print(f"  Duration: {result['duration_ms']:.2f}ms")
print(f"  Status: {result['status']}\n")

print("=== API Tests Complete ===")
