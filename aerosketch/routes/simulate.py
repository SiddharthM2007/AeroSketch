from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest

from ..utils.validation import validate_simulation_params
from ..services.simulation_engine import run_simulation

bp = Blueprint("simulate", __name__)


@bp.route("/simulate", methods=["POST"])
def simulate():
    """Validate input, run the simulation, and return results."""
    try:
        params = validate_simulation_params(request.get_json() or {})
    except BadRequest as exc:
        return jsonify({"error": str(exc)}), 400

    result = run_simulation(params)
    return jsonify(result)
