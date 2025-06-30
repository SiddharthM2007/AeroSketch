from flask import Blueprint, jsonify

from ..services.simulation_engine import get_results

bp = Blueprint("results", __name__)


@bp.route("/get_results", methods=["GET"])
def results():
    result = get_results()
    return jsonify(result)
