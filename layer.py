"""
This module defines the :class:`Layer` class used to describe a
single layer within a planar solar cell. Each layer contains basic
material and geometrical parameters such as thickness, doping, bandgap
energy and dielectric properties. Default values are provided for
mobility and lifetime when not specified.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Layer:
    """Represent a single layer within a solar cell stack.

    Parameters
    ----------
    name : str
        Human-readable identifier for the material.
    thickness : float
        Physical thickness of the layer in meters.
    Na : Optional[float], default ``0.0``
        Acceptor concentration (p-type doping) in cm⁻³. For undoped or
        intrinsic layers this can be left as zero.
    Nd : Optional[float], default ``0.0``
        Donor concentration (n-type doping) in cm⁻³. For undoped or
        intrinsic layers this can be left as zero.
    Eg : Optional[float], default ``1.5``
        Band gap energy in electron volts.
    chi : Optional[float], default ``4.0``
        Electron affinity in eV.
    epsr : Optional[float], default ``10.0``
        Relative permittivity (dimensionless). Vacuum permittivity is
        handled internally by the solver.
    mu_n : Optional[float], default ``1e-4``
        Electron mobility in m²/(V·s). Typical values vary widely; a
        small default is provided here.
    mu_p : Optional[float], default ``1e-4``
        Hole mobility in m²/(V·s).
    tau_n : Optional[float], default ``1e-6``
        Minority carrier lifetime for electrons in seconds.
    tau_p : Optional[float], default ``1e-6``
        Minority carrier lifetime for holes in seconds.

    Notes
    -----
    Units for all parameters follow SI unless explicitly stated. Doping
    concentrations use cm⁻³, which is common in semiconductor physics,
    but are internally converted to m⁻³ when necessary.
    """

    name: str
    thickness: float
    Na: float = 0.0
    Nd: float = 0.0
    Eg: float = 1.5
    chi: float = 4.0
    epsr: float = 10.0
    mu_n: float = 1e-4
    mu_p: float = 1e-4
    tau_n: float = 1e-6
    tau_p: float = 1e-6

    def __post_init__(self) -> None:
        # Basic validation to ensure non‑negative thickness and sensible doping
        if self.thickness <= 0:
            raise ValueError(f"Layer thickness must be positive, got {self.thickness}")
        if self.Na < 0 or self.Nd < 0:
            raise ValueError("Doping concentrations must be non‑negative")
        # Convert doping from cm^-3 to m^-3 for internal use
        self.Na_m3 = self.Na * 1e6  # cm⁻³ → m⁻³
        self.Nd_m3 = self.Nd * 1e6

    def is_p_type(self) -> bool:
        """Return ``True`` if the layer is p‑type (acceptor doped)."""
        return self.Na > self.Nd

    def is_n_type(self) -> bool:
        """Return ``True`` if the layer is n‑type (donor doped)."""
        return self.Nd > self.Na

    def intrinsic(self) -> bool:
        """Return ``True`` if the layer has no intentional doping."""
        return self.Na == 0 and self.Nd == 0

    def __repr__(self) -> str:
        return (f"Layer(name={self.name!r}, thickness={self.thickness:g} m, "
                f"Na={self.Na:g} cm^-3, Nd={self.Nd:g} cm^-3, Eg={self.Eg:g} eV, "
                f"chi={self.chi:g} eV, epsr={self.epsr:g})")
