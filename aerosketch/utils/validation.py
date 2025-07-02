"""Basic request validation utilities."""

from ..models import constants as C


def validate_simulation_params(data):
    defaults = {
        "shape": C.DEFAULT_SHAPE,
        "radius": C.DEFAULT_RADIUS,
        "velocity": C.DEFAULT_VELOCITY,
        "angle_of_attack": C.DEFAULT_ANGLE_OF_ATTACK,
        "fluid_density": C.DEFAULT_FLUID_DENSITY,
        "area": C.DEFAULT_AREA,
    }

    validated = {}
    for key, default in defaults.items():
        value = data.get(key, default)
        try:
            validated[key] = type(default)(value)
        except (TypeError, ValueError):
            validated[key] = default
    return validated
