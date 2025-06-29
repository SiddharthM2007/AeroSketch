"""Flask application providing the AeroSketch API."""

from __future__ import annotations

from flask import Flask, jsonify, request

from .simulation import SimulationParameters, run_mock_simulation

app = Flask(__name__)


@app.route("/simulate", methods=["POST"])
def simulate() -> tuple[str, int]:
    """Handle a simulation request with mocked results."""
    data = request.get_json(force=True) or {}
    params = SimulationParameters(**{k: data.get(k, v) for k, v in SimulationParameters().__dict__.items()})

    pressure_b64, velocity_b64 = run_mock_simulation(params)

    return jsonify({"pressure": pressure_b64, "velocity": velocity_b64})


if __name__ == "__main__":
    app.run(debug=True)
