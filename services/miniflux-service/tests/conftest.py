import pytest
from fastapi.testclient import TestClient
import sys
# Append the parent directory to sys.path to find the app module
sys.path.append(str(Path(__file__).resolve().parents[1]))
from app.main import app  
from app.main import create_app



@pytest.fixture
def app():
    return create_app()


@pytest.fixture
def client(app):
    return TestClient(app)