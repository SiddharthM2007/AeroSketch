"""Simulation engine using basic physics approximations."""

from typing import Dict

from ..models.constants import shape_coefficients
from ..session_state import session_state


def run_simulation(params: Dict[str, float]) -> Dict[str, float]:
    """Run a simple aerodynamic simulation.

    Parameters
    ----------
    params: dict
        Validated simulation parameters.

    Returns
    -------
    dict
        Computed lift/drag forces and coefficients.
    """
    shape = params["shape"]
    velocity = params["velocity"]
    fluid_density = params["fluid_density"]
    area = params["area"]
    angle = params["angle_of_attack"]

    coeffs = shape_coefficients.get(shape)
    if coeffs is None:
        raise ValueError(f"Unknown shape: {shape}")

    cl = coeffs["CL"]
    cd = coeffs["CD"]

    # adjust coefficients based on angle of attack (2% per degree)
    factor = 1 + 0.02 * angle
    cl *= factor
    cd *= factor

    dynamic_pressure = 0.5 * fluid_density * velocity ** 2
    lift = dynamic_pressure * area * cl
    drag = dynamic_pressure * area * cd

    result = {
        "lift_force": lift,
        "drag_force": drag,
        "CL": cl,
        "CD": cd,
        "vector_field": [[0.0]],
        "pressure_map": [[0.0]],
    }

    session_state.update({"input": params, "output": result})
    return result


def set_parameters(params):
    """Placeholder for parameter updates."""
    return {"status": "parameters updated"}


def get_results():
    """Placeholder for returning results."""
    return {"pressure_map": [1, 2, 3], "velocity_field": [4, 5, 6]}


def suggest_optimization(params):
    """Placeholder for optimization suggestion."""
    return {"suggestion": "Decrease angle of attack by 5°"}
