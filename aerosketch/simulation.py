"""Mock simulation utilities for AeroSketch."""

from __future__ import annotations

import base64
import io
from dataclasses import dataclass
from typing import Tuple

import numpy as np


@dataclass
class SimulationParameters:
    """Parameters describing the simulation setup."""

    shape: str = "circle"
    radius: float = 1.0
    velocity: float = 1.0
    angle_of_attack: float = 0.0


def run_mock_simulation(params: SimulationParameters) -> Tuple[str, str]:
    """Return mocked pressure and velocity fields.

    Args:
        params: User-provided simulation parameters.

    Returns:
        Tuple of base64 encoded pressure field and velocity field arrays.
    """
    # Create fake pressure and velocity arrays using random data
    pressure = np.random.rand(64, 64)
    velocity = np.random.rand(64, 64)

    # Serialize arrays to bytes and encode with base64
    buf = io.BytesIO()
    np.save(buf, pressure)
    pressure_b64 = base64.b64encode(buf.getvalue()).decode()

    buf = io.BytesIO()
    np.save(buf, velocity)
    velocity_b64 = base64.b64encode(buf.getvalue()).decode()

    return pressure_b64, velocity_b64
