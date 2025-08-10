"""
The :class:`Device` class aggregates individual :class:`~myscaps.layer.Layer`
objects into a complete solar cell stack. It also stores global
simulation settings such as temperature and spatial meshing options. A
simple validation routine ensures that the layers are arranged in a
physically sensible order.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List, Optional, Dict, Any
import warnings

from .layer import Layer


@dataclass
class Device:
    """Represent a complete solar cell structure.

    Parameters
    ----------
    layers : Iterable[Layer]
        List of :class:`Layer` instances forming the device stack. The
        order should be from front (illumination side) to back. A
        typical perovskite cell uses an electron transport layer (ETL),
        followed by the absorber, then a hole transport layer (HTL).
    T : float, default ``300``
        Device temperature in Kelvin.
    mesh_points : int, default ``200``
        Number of spatial points used in the drift‑diffusion solver. A
        uniform mesh is constructed across the total device thickness.

    Attributes
    ----------
    results : Dict[str, Any]
        Placeholder for simulation outputs such as voltage and current
        arrays. Populated by :func:`~myscaps.solver.solve`.
    """

    layers: Iterable[Layer]
    T: float = 300.0
    mesh_points: int = 200
    results: Dict[str, Any] = field(default_factory=dict, init=False)

    def __post_init__(self) -> None:
        # Ensure layers is a list for iteration and indexing
        self.layers: List[Layer] = list(self.layers)
        if len(self.layers) < 2:
            raise ValueError("A device must consist of at least two layers")
        self._validate_order()
        # Precompute cumulative thicknesses for meshing
        self.total_thickness = sum(layer.thickness for layer in self.layers)
        # Precompute interface positions (in meters)
        self.interfaces = []
        pos = 0.0
        for layer in self.layers:
            pos += layer.thickness
            self.interfaces.append(pos)

    def _validate_order(self) -> None:
        """Check that the provided layers follow a sensible stack order.

        The first layer should be n‑type (ETL), the last should be
        p‑type (HTL), and there must be at least one intrinsic or
        lightly doped absorber layer in between. If these conditions are
        not met, a warning is emitted and the simulation proceeds. This
        flexible behaviour allows users to explore unusual stacks while
        still receiving feedback.
        """
        if not self.layers:
            return
        first = self.layers[0]
        last = self.layers[-1]
        # Check doping type of first layer
        if not first.is_n_type():
            warnings.warn(
                "First layer does not appear to be n‑type; expected electron transport layer (ETL)",
                RuntimeWarning,
            )
        # Check doping type of last layer
        if not last.is_p_type():
            warnings.warn(
                "Last layer does not appear to be p‑type; expected hole transport layer (HTL)",
                RuntimeWarning,
            )
        # Check for absorber in between
        if len(self.layers) > 2:
            mid_layers = self.layers[1:-1]
            found_absorber = any(l.intrinsic() or (l.Na > 0 and l.Nd > 0) for l in mid_layers)
            if not found_absorber:
                warnings.warn(
                    "No intrinsic or lightly doped absorber layer found between transport layers",
                    RuntimeWarning,
                )

    def build_mesh(self) -> List[float]:
        """Construct a one‑dimensional spatial mesh across the device.

        The mesh divides the total device thickness into ``mesh_points``
        evenly spaced segments. This simple uniform mesh suffices for
        coarse simulations; more advanced meshing strategies could be
        implemented as needed.

        Returns
        -------
        mesh : List[float]
            Positions in meters from the front surface to the back
            surface, inclusive.
        """
        import numpy as np

        mesh = np.linspace(0.0, self.total_thickness, self.mesh_points)
        return mesh.tolist()
