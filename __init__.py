"""
This package exposes the main classes and functions used to build and
simulate planar perovskite (or similar) solar cells. It aims to provide
an intuitive API inspired by SCAPS but implemented in pure Python.

Users typically import the ``Layer``, ``Device`` and ``solve`` helpers
directly from this package:

.. code-block:: python

    from solame import Layer, Device, solve

    etl = Layer(name="TiO2", thickness=50e-9, Nd=1e19, Eg=3.2, chi=4.0, epsr=9)
    absorber = Layer(name="MAPbI3", thickness=500e-9, Na=1e15, Eg=1.55, chi=3.9, epsr=25)
    htl = Layer(name="Spiro-OMeTAD", thickness=200e-9, Na=1e19, Eg=3.0, chi=2.2, epsr=3)

    device = Device([etl, absorber, htl], T=300)
    solve(device)

    # Access results
    voltages = device.results['voltage']
    currents = device.results['current']

"""

from .layer import Layer
from .device import Device
from .solver import solve
from .plots import plot_jv, plot_generation

__all__ = [
    "Layer",
    "Device",
    "solve",
    "plot_jv",
    "plot_generation",
]
