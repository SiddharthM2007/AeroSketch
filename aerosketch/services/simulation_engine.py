"""Simplified physics-based simulation engine."""

import math
import numpy as np

from ..session_state import session_state


def _generate_flow_field(radius, velocity, angle_deg, fluid_density, grid=20):
    """Compute velocity and pressure fields around a circle using basic
    potential flow theory."""
    alpha = math.radians(angle_deg)
    x = np.linspace(-2 * radius, 2 * radius, grid)
    y = np.linspace(-2 * radius, 2 * radius, grid)
    X, Y = np.meshgrid(x, y)

    pressure_map = np.zeros((grid, grid))
    velocity_field = [[(0.0, 0.0) for _ in range(grid)] for _ in range(grid)]

    for i in range(grid):
        for j in range(grid):
            x_pt = X[i][j]
            y_pt = Y[i][j]

            xr = x_pt * math.cos(alpha) + y_pt * math.sin(alpha)
            yr = -x_pt * math.sin(alpha) + y_pt * math.cos(alpha)

            r = math.hypot(xr, yr)
            if r < radius:
                r = radius
            theta = math.atan2(yr, xr)

            Vr = velocity * math.cos(theta) * (1 - (radius ** 2) / (r ** 2))
            Vt = -velocity * math.sin(theta) * (1 + (radius ** 2) / (r ** 2))

            u = Vr * math.cos(theta) - Vt * math.sin(theta)
            v = Vr * math.sin(theta) + Vt * math.cos(theta)

            velocity_field[i][j] = (u, v)
            speed = math.hypot(u, v)
            pressure_map[i][j] = 0.5 * fluid_density * (velocity ** 2 - speed ** 2)

    return pressure_map, velocity_field


def _compute_forces(velocity, angle_deg, area, density):
    alpha = math.radians(angle_deg)
    CL = 2 * math.pi * alpha
    CD = 0.01 + 0.1 * abs(alpha)
    q = 0.5 * density * velocity ** 2
    lift = CL * q * area
    drag = CD * q * area
    return lift, drag, CL, CD


def run_simulation(params):
    shape = params.get("shape", "circle")
    radius = float(params.get("radius", 1.0))
    velocity = float(params.get("velocity", 1.0))
    angle = float(params.get("angle_of_attack", 0.0))
    density = float(params.get("fluid_density", 1.225))
    area = float(params.get("area", math.pi * radius ** 2))

    pressure_map, velocity_field = _generate_flow_field(radius, velocity, angle, density)
    lift, drag, CL, CD = _compute_forces(velocity, angle, area, density)

    result = {
        "lift_force": lift,
        "drag_force": drag,
        "CL": CL,
        "CD": CD,
        "pressure_map": pressure_map,
        "velocity_field": velocity_field,
    }

    session_state["output"] = result
    return result


def set_parameters(params):
    return {"status": "parameters updated"}


def get_results():
    return session_state.get("output", {}) or {}


def suggest_optimization(params):
    return {"suggestion": "Decrease angle of attack by 5\u00b0"}
