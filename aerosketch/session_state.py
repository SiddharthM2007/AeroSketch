"""Simple in-memory session state to store the latest simulation results."""

_current_results = {}


def update_results(results):
    """Store the latest simulation results."""
    global _current_results
    _current_results = results


def get_results():
    """Retrieve the latest simulation results."""
    return _current_results
