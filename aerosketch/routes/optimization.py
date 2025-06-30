from flask import Blueprint, request, jsonify

from ..services.simulation_engine import suggest_optimization

bp = Blueprint("optimization", __name__)


@bp.route("/suggest_optimization", methods=["POST"])
def suggest():
    data = request.get_json() or {}
    result = suggest_optimization(data)
    return jsonify(result)
