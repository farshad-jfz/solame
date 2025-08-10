"""Plotting utilities for the solame simulator.

These functions leverage :mod:`matplotlib` to visualise simulation
results. Each helper accepts a :class:`~solame.device.Device` and
produces standard plots for the J–V curve and generation profile.
"""

from __future__ import annotations

from typing import Optional, Tuple
import numpy as np
import matplotlib.pyplot as plt

from .device import Device


def plot_jv(device: Device, *, ax: Optional[plt.Axes] = None, units: str = "A/m^2") -> Tuple[plt.Figure, plt.Axes]:
    """Plot the current density as a function of voltage.

    Parameters
    ----------
    device : Device
        Device with simulation results available in its ``results`` dict.
    ax : matplotlib.axes.Axes, optional
        Existing axes to plot on. If not provided, a new figure and
        axes are created.
    units : {"A/m^2", "mA/cm^2"}, default ``"A/m^2"``
        Units for the current density. If ``"mA/cm^2"`` is chosen, the
        data are scaled accordingly (1 A/m^2 = 0.1 mA/cm^2).

    Returns
    -------
    fig, ax : (matplotlib.figure.Figure, matplotlib.axes.Axes)
        Figure and axes objects containing the plot.
    """
    if "voltage" not in device.results or "current" not in device.results:
        raise RuntimeError("No J–V data found in device results; run solve() first.")
    V = np.array(device.results["voltage"])
    J = np.array(device.results["current"])
    if units == "mA/cm^2":
        J = J * 1e3 / 1e4  # convert A/m^2 to mA/cm^2 (1 A/m^2 = 0.1 mA/cm^2)
        ylabel = "Current density (mA/cm$^2$)"
    else:
        ylabel = "Current density (A/m$^2$)"
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.figure
    ax.plot(V, J, label="J–V curve")
    ax.set_xlabel("Voltage (V)")
    ax.set_ylabel(ylabel)
    ax.grid(True)
    ax.legend()
    return fig, ax


def plot_generation(device: Device, *, ax: Optional[plt.Axes] = None) -> Tuple[plt.Figure, plt.Axes]:
    """Plot the generation profile G(x) versus depth.

    Parameters
    ----------
    device : Device
        Device with a generation profile stored in its results.
    ax : matplotlib.axes.Axes, optional
        Existing axes to plot on. If not provided, a new figure and
        axes are created.

    Returns
    -------
    fig, ax : (matplotlib.figure.Figure, matplotlib.axes.Axes)
        Figure and axes objects containing the plot.
    """
    if "generation_profile" not in device.results or "mesh" not in device.results:
        raise RuntimeError("No generation data found in device results; run solve() first.")
    mesh = np.array(device.results["mesh"])
    G = np.array(device.results["generation_profile"])
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.figure
    ax.plot(mesh * 1e9, G)
    ax.set_xlabel("Depth (nm)")
    ax.set_ylabel("Generation rate (pairs m$^{-3}$ s$^{-1}$)")
    ax.grid(True)
    return fig, ax
