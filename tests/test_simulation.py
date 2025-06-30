import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
from aerosketch.app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_valid_simulation(client):
    payload = {
        "shape": "airfoil",
        "velocity": 10.0,
        "fluid_density": 1.0,
        "area": 3.0,
        "angle_of_attack": 5.0,
    }
    resp = client.post('/simulate', json=payload)
    assert resp.status_code == 200
    data = resp.get_json()
    for key in ["lift_force", "drag_force", "CL", "CD", "vector_field", "pressure_map"]:
        assert key in data


def test_missing_field(client):
    payload = {
        "shape": "airfoil",
        "velocity": 10.0,
        "fluid_density": 1.0,
        # missing area
        "angle_of_attack": 0.0,
    }
    resp = client.post('/simulate', json=payload)
    assert resp.status_code == 400
