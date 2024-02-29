from fastapi.testclient import TestClient
import sys
# Append the parent directory to sys.path to find the app module
sys.path.append(str(Path(__file__).resolve().parents[1]))
from app.main import app  
import pytest

@pytest.mark.asyncio
async def test_check_status(client):
  client.post("/", json={"set": True})
  assert client.get("/").json()['state']