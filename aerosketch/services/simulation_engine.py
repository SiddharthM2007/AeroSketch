"""Dummy simulation engine returning canned responses."""


def run_simulation(params):
    return {"drag_coefficient": 0.65, "lift_coefficient": 1.2}


def set_parameters(params):
    return {"status": "parameters updated"}


def get_results():
    return {"pressure_map": [1, 2, 3], "velocity_field": [4, 5, 6]}


def suggest_optimization(params):
    return {"suggestion": "Decrease angle of attack by 5\u00b0"}
