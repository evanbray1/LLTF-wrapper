#!/usr/bin/env python3
"""
LLTF Basic Demo

Minimal example showing the essential LLTF wrapper usage:
1. Initialize device (real or simulated)
2. Get wavelength ranges
3. Set and get wavelengths

This is the simplest way to get started with the LLTF wrapper.
"""

import sys
import os
try:
    from lltf_wrapper import LLTF
except ImportError:
    # Add parent directory to path to import lltf_wrapper in case you are running this file from within the repo without installing
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from lltf_wrapper import LLTF

print("=== LLTF Basic Demo ===\n")

# Initialize LLTF (uses automatic XML detection or specify path)
# lltf = LLTF(xml_config_path="/path/to/xml/file")
lltf = LLTF()


# Initialize in simulation mode (set to False for real hardware)
lltf.initialize(simulate=True)
print("LLTF initialized")

# Get available wavelength ranges
ranges = lltf.get_grating_ranges()
print("\nAvailable wavelength ranges:")
for grating in ranges:
    reg_range = grating['regular_range']
    print(f"  Grating {grating['index']}: {reg_range[0]}-{reg_range[1]} nm")

# Get current wavelength
current = lltf.get_wavelength()
print(f"\nCurrent wavelength: {current} nm")

# Set some test wavelengths
test_wavelengths = [450, 600, 800]
print("\nTesting wavelengths:")

for wavelength in test_wavelengths:
    lltf.set_wavelength(wavelength)
    actual = lltf.get_wavelength()

print("\nDemo complete!")

# Close the LLTF connection
lltf.close()