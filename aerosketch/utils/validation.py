"""Basic request validation utilities."""

def validate_simulation_params(data):
    defaults = {
        "shape": "circle",
        "radius": 1.0,
        "velocity": 1.0,
        "angle_of_attack": 0.0,
        "density": 1.225,
    }

    validated = {}
    for key, default in defaults.items():
        value = data.get(key, default)
        try:
            validated[key] = type(default)(value)
        except (TypeError, ValueError):
            validated[key] = default
    return validated
