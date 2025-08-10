"""
This module contains a small collection of common materials used in
perovskite solar cells along with typical parameters. It is intended
for convenience when building a device. Users can access the
``MATERIALS`` dictionary or call :func:`get_material` to retrieve a
predefined :class:`~solame.layer.Layer` instance with reasonable
defaults. The thickness should be specified by the user when
instantiating a device; the thickness values here serve only as
examples.
"""

from __future__ import annotations

from typing import Dict
from .layer import Layer


# A dictionary mapping material names to default parameters. The keys
# are lowercase for case‑insensitive lookup.
_PREDEFINED: Dict[str, Dict] = {
    "tio2": {
        "Eg": 3.2,
        "chi": 4.0,
        "epsr": 9.0,
        "Nd": 1e19,
        "Na": 0.0,
    },
    "mapbi3": {
        "Eg": 1.55,
        "chi": 3.9,
        "epsr": 25.0,
        "Na": 1e15,
        "Nd": 1e15,
    },
    "spiro-ometad": {
        "Eg": 3.0,
        "chi": 2.2,
        "epsr": 3.0,
        "Na": 1e19,
        "Nd": 0.0,
    },
    "ptaa": {
        "Eg": 2.8,
        "chi": 2.1,
        "epsr": 3.0,
        "Na": 1e17,
        "Nd": 0.0,
    },
    "cigs": {
        "Eg": 1.1,
        "chi": 4.5,
        "epsr": 13.6,
        "Na": 1e15,
        "Nd": 1e15,
    },
}


def get_material(name: str, thickness: float) -> Layer:
    """Return a :class:`Layer` instance for a predefined material.

    Parameters
    ----------
    name : str
        Identifier of the material. Matching is case‑insensitive.
    thickness : float
        Thickness of the layer in metres. This value is not stored in
        the database and must be provided by the caller.

    Returns
    -------
    Layer
        A layer configured with properties from the materials database.

    Raises
    ------
    KeyError
        If the material is not found in the database.
    """
    key = name.strip().lower()
    if key not in _PREDEFINED:
        raise KeyError(f"Material '{name}' not found in database")
    params = _PREDEFINED[key]
    return Layer(name=name, thickness=thickness, **params)


def list_materials() -> Dict[str, Dict]:
    """Return a copy of the materials dictionary for inspection."""
    return {k: v.copy() for k, v in _PREDEFINED.items()}
