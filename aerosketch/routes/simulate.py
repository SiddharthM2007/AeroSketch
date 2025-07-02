from flask import Blueprint, request, jsonify

from ..utils.validation import validate_simulation_params
from ..services.simulation_engine import run_simulation
from ..session_state import session_state

bp = Blueprint("simulate", __name__)


@bp.route("/simulate", methods=["POST"])
def simulate():
    params = validate_simulation_params(request.get_json() or {})
    session_state["input"] = params
    result = run_simulation(params)
    return jsonify(result)
