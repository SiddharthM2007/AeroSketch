"""Request validation utilities for simulation parameters."""

from typing import Any, Dict
from werkzeug.exceptions import BadRequest


def validate_simulation_params(data: Dict[str, Any]) -> Dict[str, float]:
    """Validate simulation parameters from a request body.

    Parameters
    ----------
    data: dict
        Input dictionary from the request JSON.

    Returns
    -------
    dict
        Normalized and validated parameters.

    Raises
    ------
    BadRequest
        If required fields are missing or values are out of range.
    """
    required_fields = ["shape", "velocity", "fluid_density", "area", "angle_of_attack"]
    for field in required_fields:
        if field not in data:
            raise BadRequest(f"Missing field: {field}")

    try:
        shape = str(data["shape"])
        velocity = float(data["velocity"])
        fluid_density = float(data["fluid_density"])
        area = float(data["area"])
        angle_of_attack = float(data["angle_of_attack"])
    except (TypeError, ValueError) as exc:
        raise BadRequest("Invalid parameter types") from exc

    if velocity <= 0:
        raise BadRequest("velocity must be greater than 0")
    if not -30 <= angle_of_attack <= 30:
        raise BadRequest("angle_of_attack must be between -30 and 30")

    return {
        "shape": shape,
        "velocity": velocity,
        "fluid_density": fluid_density,
        "area": area,
        "angle_of_attack": angle_of_attack,
    }
