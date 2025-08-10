"""Drift–diffusion solver (simplified) for Solame.

This module implements a very basic electrical response calculation for
planar solar cells using a single‑diode model. While full drift–
diffusion modelling requires solving coupled Poisson and continuity
equations (e.g., using the `sesame` package), this simplified
implementation provides reasonable current–voltage characteristics for
demonstration purposes.
"""

from __future__ import annotations

from typing import Tuple, List
import numpy as np

from .device import Device

try:
    import scipy.constants as scipy_const  # type: ignore
    class const:  # type: ignore
        """Namespace for physical constants used by the solver."""

        # Boltzmann constant (J/K)
        k = getattr(scipy_const, "k", 1.380649e-23)
        # Elementary charge (C). SciPy uses 'e' or 'elementary_charge'
        q = getattr(scipy_const, "elementary_charge", getattr(scipy_const, "e", 1.602176634e-19))
except Exception:
    # Provide minimal constants if scipy is not available
    class const:
        k = 1.380649e-23
        q = 1.602176634e-19


def simulate_current_voltage(device: Device, generation_profile: List[float], n: float = 1.0) -> Tuple[np.ndarray, np.ndarray, float, float, float, float]:
    """Compute current–voltage characteristics using a single‑diode model.

    Parameters
    ----------
    device : Device
        The device under study.
    generation_profile : List[float]
        Photogeneration rate G(x) in pairs per m³ per s at each mesh
        point.
    n : float, default ``1.0``
        Ideality factor for the diode equation.

    Returns
    -------
    voltage : numpy.ndarray
        Array of voltage points in volts.
    current : numpy.ndarray
        Array of current densities in A/m² corresponding to the voltage points.
    voc : float
        Open‑circuit voltage in volts.
    jsc : float
        Short‑circuit current density (positive value) in A/m².
    ff : float
        Fill factor (0–1).
    eta : float
        Power conversion efficiency (0–1).
    """
    # Convert generation profile to total short‑circuit current density
    G = np.array(generation_profile)
    # Integrate generation over the device thickness: pairs per m^2 per s
    # Multiply by elementary charge to get current density (A/m^2)
    total_pairs = np.trapz(G, np.linspace(0.0, device.total_thickness, len(G)))
    q = const.q
    jsc = q * total_pairs  # short‑circuit current density (positive)

    # Estimate reverse saturation current density J0. Use a simple
    # heuristic based on doping levels: higher doping reduces J0.
    # Sum dopant densities (m^-3) across layers
    total_doping = sum(max(layer.Na_m3, layer.Nd_m3) for layer in device.layers)
    # Avoid division by zero
    total_doping = total_doping if total_doping > 0 else 1e14
    # Set a baseline J00 typical for perovskite solar cells (A/m^2)
    J00 = 1e-12
    J0 = J00 * (1e24 / total_doping)

    # Thermal voltage
    Vt = const.k * device.T / q
    # Compute open‑circuit voltage
    if J0 > 0:
        voc = Vt * n * np.log(jsc / J0 + 1.0)
    else:
        voc = 0.0
    # Generate voltage sweep from 0 to Voc with 200 points
    voltage = np.linspace(0.0, voc, 200)
    # Compute diode current
    diode_current = J0 * (np.exp(voltage / (Vt * n)) - 1.0)
    # Photocurrent is constant (negative because current flows out)
    photocurrent = -jsc * np.ones_like(voltage)
    # Net current density (A/m^2)
    current = diode_current + photocurrent

    # Compute fill factor using standard approximation
    if voc > 0 and jsc > 0:
        voc_n = voc / (Vt * n)
        ff = (voc_n - np.log(voc_n + 0.72)) / (voc_n + 1.0)
        ff = max(0.0, min(1.0, ff))
    else:
        ff = 0.0
    # Power conversion efficiency: Pmax / Pin
    Pin = 1000.0  # incident power density (W/m^2)
    pmax = voc * jsc * ff
    eta = pmax / Pin

    return voltage, current, voc, jsc, ff, eta
