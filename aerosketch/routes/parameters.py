from flask import Blueprint, request, jsonify

from ..services.simulation_engine import set_parameters

bp = Blueprint("parameters", __name__)


@bp.route("/set_parameters", methods=["POST"])
def set_params():
    data = request.get_json() or {}
    result = set_parameters(data)
    return jsonify(result)
