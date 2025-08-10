"""High‑level solver wrapper for Solame solar cell simulator to tie the optical and electrical models. 

:func:`solve` function computes the generation profile using
``optical.compute_generation_profile`` and then invokes
``dd_solver.simulate_current_voltage`` to obtain the current–voltage
characteristics. 

Results are stored in the provided :class:`Device`
instance for later inspection or plotting.
"""

from __future__ import annotations

from typing import Optional

from .device import Device
from . import optical, dd_solver


def solve(device: Device, *, ideality_factor: float = 1.0) -> None:
    """Simulate the device by running optical and electrical models.

    This function computes the spatial generation profile and uses it
    within a simplified drift–diffusion solver to produce the
    current–voltage characteristics. The results are stored as
    attributes on the ``device`` argument. No value is returned.

    Parameters
    ----------
    device : Device
        The device to simulate. Its ``results`` attribute will be
        populated.
    ideality_factor : float, default ``1.0``
        Ideality factor ``n`` used in the diode equation.
    """
    # Compute photogeneration rate G(x)
    generation_profile = optical.compute_generation_profile(device)
    # Run single‑diode electrical simulation
    voltage, current, voc, jsc, ff, eta = dd_solver.simulate_current_voltage(
        device, generation_profile, n=ideality_factor
    )
    # Populate results dictionary
    device.results = {
        "voltage": voltage,
        "current": current,
        "voc": voc,
        "jsc": jsc,
        "ff": ff,
        "efficiency": eta,
        "generation_profile": generation_profile,
        "mesh": device.build_mesh(),
    }
