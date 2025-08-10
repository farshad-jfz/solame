"""Simple optical model for generation rate calculation.

This module implements a rudimentary optical model to compute the
photogeneration profile inside a planar solar cell. It uses a very
simplified approximation of the solar spectrum and absorption within
each layer instead of a full transfer matrix method. The intent is to
provide a reasonable generation profile for demonstration when the
external :mod:`tmm` package is not available.

One could extend this module to perform a proper transfer matrix calculation. This version provides a
placeholder implementation that scales with the device layer
properties.
"""

from __future__ import annotations

from typing import List
import numpy as np

from .device import Device


def compute_generation_profile(device: Device) -> List[float]:
    """Compute the photogeneration rate throughout the device.

    A simplified model is used to approximate the number of electron–
    hole pairs generated per unit volume and time. It assumes a
    homogeneous photon flux that decays exponentially with depth into
    the absorbing layers based on their bandgap energies. The model
    neglects interference effects and wavelength dependence.

    Parameters
    ----------
    device : Device
        The solar cell device for which to compute the generation profile.

    Returns
    -------
    generation : List[float]
        Photogeneration rate G(x) in pairs per m³ per s at each mesh
        point. The length of this list matches ``device.mesh_points``.
    """
    # Build the spatial mesh
    mesh = np.array(device.build_mesh())
    G = np.zeros_like(mesh)

    # Approximate total photon flux corresponding to 1000 W/m^2 solar
    # irradiance with average photon energy of 1.5 eV
    q = 1.602176634e-19  # elementary charge (C)
    avg_photon_energy_j = 1.5 * q  # approximate average photon energy
    # Scale down the raw photon flux to yield realistic current densities
    # Typical solar cells exhibit short‑circuit currents around 20 mA/cm^2.
    # Without scaling, the simplistic model often produces unrealistic
    # values; a factor of ~1/3 brings results in line with experiments.
    photon_flux = (1000.0 / avg_photon_energy_j) * 0.33  # photons per m^2 per s

    # Distribute generation based on bandgap: lower bandgap absorbs more
    # of the spectrum. Define absorption factors for each layer.
    # A simple heuristic: absorption factor = max(0, 2 - Eg) for Eg <= 2 eV
    # so Eg=1.5 → 0.5, Eg=1 → 1.0, Eg=2 → 0.
    absorption_factors = []
    for layer in device.layers:
        factor = max(0.0, 2.0 - layer.Eg)
        absorption_factors.append(factor)

    # Normalise absorption factors so that the sum equals one, avoiding
    # division by zero. If no layer absorbs, all factors remain zero and
    # generation stays zero.
    total_factor = sum(absorption_factors)
    if total_factor > 0:
        absorption_factors = [f / total_factor for f in absorption_factors]

    # Determine exponential attenuation coefficient for each layer based
    # on its bandgap: smaller bandgap → higher absorption coefficient.
    # Use base coefficient alpha0 as 1e7 m^-1 for Eg=1 eV and scale
    # inversely with Eg.
    alpha0 = 1e7
    alphas = []
    for layer in device.layers:
        # Avoid division by zero: if Eg is zero, use Eg=0.5 eV for scaling
        Eg_for_alpha = layer.Eg if layer.Eg > 0.5 else 0.5
        alphas.append(alpha0 / Eg_for_alpha)

    # Loop over mesh points and assign generation depending on the layer
    # the point belongs to. For each layer we integrate the decaying
    # photon flux across the layer thickness: G_layer(x) = phi * factor
    # * alpha * exp(-alpha * distance_into_layer).
    # Determine layer boundaries from cumulative thicknesses.
    layer_boundaries = [0.0] + device.interfaces
    for i, layer in enumerate(device.layers):
        x_start = layer_boundaries[i]
        x_end = layer_boundaries[i + 1]
        # Indices within this layer
        indices = np.where((mesh >= x_start) & (mesh <= x_end))[0]
        alpha = alphas[i]
        factor = absorption_factors[i]
        if factor == 0.0:
            continue
        # Compute distance into layer for each mesh point in this layer
        distances = mesh[indices] - x_start
        # Generation per unit volume at each point
        G_layer = photon_flux * factor * alpha * np.exp(-alpha * distances)
        # Convert photons per m^2 per s to pairs per m^3 per s by
        # dividing by absorption length; here alpha accounts for that.
        G[indices] = G_layer
    return G.tolist()
