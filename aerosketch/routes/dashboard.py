from flask import Blueprint, render_template

from ..session_state import get_results

bp = Blueprint("dashboard", __name__)


@bp.route("/dashboard", methods=["GET"])
def dashboard():
    results = get_results()
    if not results:
        content = "<p>No results yet.</p>"
    else:
        table_rows = []
        for row in results.get("pressure_map", []):
            cells = "".join(f"<td>{value:.2f}</td>" for value in row)
            table_rows.append(f"<tr>{cells}</tr>")
        table_html = "<table>" + "".join(table_rows) + "</table>"
        content = (
            f"<p>Lift: {results['lift']:.2f} N</p>"
            f"<p>Drag: {results['drag']:.2f} N</p>"
            f"<p>CL: {results['lift_coefficient']:.3f}</p>"
            f"<p>CD: {results['drag_coefficient']:.3f}</p>"
            f"<h2>Pressure Map</h2>{table_html}"
        )
    return render_template("dashboard.html", content=content)
