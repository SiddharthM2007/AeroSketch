from flask import Blueprint, render_template, send_file
import io
import matplotlib.pyplot as plt

from ..session_state import session_state

bp = Blueprint("dashboard", __name__)


@bp.route("/dashboard", methods=["GET"])
def dashboard():
    data = session_state.get("output")
    return render_template("dashboard.html", data=data)


@bp.route("/visualize", methods=["GET"])
def visualize():
    data = session_state.get("output") or {}
    pressure = data.get("pressure_map")
    if pressure is None:
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, "No Data", ha="center", va="center")
    else:
        fig, ax = plt.subplots()
        ax.imshow(pressure, origin="lower", cmap="viridis")
        ax.set_title("Pressure Map")
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return send_file(buf, mimetype="image/png")
