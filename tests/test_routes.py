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


def test_simulate(client):
    payload = {
        "shape": "circle",
        "velocity": 5.0,
        "fluid_density": 1.0,
        "area": 2.0,
        "angle_of_attack": 0.0,
    }
    resp = client.post('/simulate', json=payload)
    assert resp.status_code == 200
    json_data = resp.get_json()
    assert 'drag_force' in json_data
    assert 'lift_force' in json_data


def test_set_parameters(client):
    resp = client.post('/set_parameters', json={"shape": "square"})
    assert resp.status_code == 200
    assert resp.get_json()['status'] == 'parameters updated'


def test_get_results(client):
    resp = client.get('/get_results')
    assert resp.status_code == 200
    json_data = resp.get_json()
    assert 'pressure_map' in json_data
    assert 'velocity_field' in json_data


def test_suggest_optimization(client):
    resp = client.post('/suggest_optimization', json={})
    assert resp.status_code == 200
    assert 'suggestion' in resp.get_json()
