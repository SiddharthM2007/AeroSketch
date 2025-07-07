"""Lightweight aerodynamic simulation engine."""

import math

from ..session_state import update_results, get_results as _get_results
from ..models.constants import DEFAULT_DENSITY


def run_simulation(params):
    """Run a simple potential flow simulation around a circular body."""
    shape = params.get("shape", "circle")
    radius = float(params.get("radius", 1.0))
    velocity = float(params.get("velocity", 1.0))
    angle_deg = float(params.get("angle_of_attack", 0.0))
    density = float(params.get("density", DEFAULT_DENSITY))

    alpha = math.radians(angle_deg)

    # Thin airfoil theory for lift coefficient
    cl = 2.0 * math.pi * alpha
    # Simple drag coefficient approximation
    cd = 0.01 + (cl ** 2) / (math.pi * 2.0)

    area = math.pi * radius * radius
    dynamic_pressure = 0.5 * density * velocity ** 2

    lift = dynamic_pressure * area * cl
    drag = dynamic_pressure * area * cd

    # Generate pressure and velocity fields on a square grid
    grid_size = 20
    grid_range = [(-3 * radius) + (6 * radius) * i / (grid_size - 1) for i in range(grid_size)]

    pressure_map = []
    velocity_field = []

    gamma = 4 * math.pi * radius * velocity * math.sin(alpha)

    for y in grid_range:
        p_row = []
        v_row = []
        for x in grid_range:
            r = math.hypot(x, y)
            if r < radius:
                V = 0.0
            else:
                theta = math.atan2(y, x)
                ur = velocity * (1 - (radius ** 2) / (r ** 2)) * math.cos(theta - alpha)
                ut = (
                    -velocity * (1 + (radius ** 2) / (r ** 2)) * math.sin(theta - alpha)
                    + gamma / (2 * math.pi * r)
                )
                V = math.sqrt(ur ** 2 + ut ** 2)
            cp = 1 - (V / velocity) ** 2 if velocity != 0 else 1.0
            p_row.append(cp)
            v_row.append(V)
        pressure_map.append(p_row)
        velocity_field.append(v_row)

    result = {
        "lift_coefficient": cl,
        "drag_coefficient": cd,
        "lift": lift,
        "drag": drag,
        "pressure_map": pressure_map,
        "velocity_field": velocity_field,
    }
    update_results(result)
    return result


def set_parameters(params):
    """Currently just a stub to acknowledge parameter updates."""
    return {"status": "parameters updated"}


def get_results():
    """Return the latest simulation results from session state."""
    return _get_results()


def suggest_optimization(params):
    """Provide a trivial optimization suggestion based on angle of attack."""
    angle = float(params.get("angle_of_attack", 0.0))
    suggestion = (
        "Decrease angle of attack by 5°" if angle > 5 else "Increase angle of attack by 5°"
    )
    return {"suggestion": suggestion}
