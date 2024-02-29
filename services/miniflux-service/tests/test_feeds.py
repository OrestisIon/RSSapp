from fastapi.testclient import TestClient
import sys
from pathlib import Path
import httpx
from httpx import WSGITransport
# Append the parent directory to sys.path to find the app module
sys.path.append(str(Path(__file__).resolve().parents[1]))
from app.main import app  

client = httpx.Client(transport=WSGITransport(app=app))

def test_get_all_feeds():
    response = client.get("/api/v1/feeds/")
    assert response.status_code == 200

def test_get_feed():
    feed_id = 1  # Example feed_id, adjust as necessary
    response = client.get(f"/api/v1/feeds/{feed_id}")
    assert response.status_code == 200

def test_create_feed():
    response = client.post("/api/v1/feeds/", json={"url": "http://example.com/feed", "category_id": 1})
    assert response.status_code == 200

def test_update_feed():
    feed_id = 1  # Example feed_id, adjust as necessary
    response = client.put(f"/api/v1/{feed_id}", json={"title": "Updated Title"})
    assert response.status_code == 200

def test_delete_feed():
    feed_id = 1  # Example feed_id, adjust as necessary
    response = client.delete(f"/api/v1/{feed_id}")
    assert response.status_code == 200

def test_get_all_categories():
    response = client.get("/api/v1/categories")
    assert response.status_code == 200

def test_get_all_icons():
    response = client.get("/api/v1/icons")
    assert response.status_code == 200

def test_get_icon():
    icon_id = 1  # Example icon_id, adjust as necessary
    response = client.get(f"/api/v1/icons/{icon_id}")
    assert response.status_code == 200

def test_get_category():
    category_id = 1  # Example category_id, adjust as necessary
    response = client.get(f"/api/v1/categories/{category_id}")
    assert response.status_code == 200

def test_discover_feeds():
    response = client.post("/api/v1/discover", json={"url": "http://example.com"})
    assert response.status_code == 200