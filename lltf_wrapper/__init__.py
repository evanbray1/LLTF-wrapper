"""
LLTF Python Wrapper Package

A Python wrapper for the NKT Photonics Laser Line Tunable Filter (LLTF) DLL.
"""

from .lltf_wrapper import LLTF, LLTFError

__version__ = "1.0.0"
__author__ = "Evan Bray"

__all__ = ["LLTF", "LLTFError"]