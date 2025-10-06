#!/usr/bin/env python3
"""
Test script for the new uncertainty functionality in LLTF wrapper.
"""

from lltf_wrapper import LLTF

def test_uncertainty_functionality():
    """Test the new uncertainty parameter in simulation mode."""
    
    print("Testing LLTF uncertainty functionality\n")
    
    # Test 1: No uncertainty (default behavior)
    print("=== Test 1: No uncertainty (default) ===")
    lltf1 = LLTF("lltf_wrapper/xml_files/M000010263.xml")
    lltf1.initialize(simulate=True)
    lltf1.set_wavelength(600.0)
    measured_wavelength = lltf1.get_wavelength()
    print("Set wavelength: 600.0 nm")
    print(f"Measured wavelength: {measured_wavelength:.3f} nm")
    print(f"Difference: {measured_wavelength - 600.0:.3f} nm")
    lltf1.close()
    print()
    
    # Test 2: Small uncertainty
    print("=== Test 2: Small uncertainty (0.1 nm) ===")
    lltf2 = LLTF("lltf_wrapper/xml_files/M000010263.xml")
    lltf2.initialize(simulate=True, uncertainty=0.1)
    lltf2.set_wavelength(600.0)
    measured_wavelength = lltf2.get_wavelength()
    print("Set wavelength: 600.0 nm")
    print(f"Measured wavelength: {measured_wavelength:.3f} nm")
    print(f"Difference: {measured_wavelength - 600.0:.3f} nm")
    lltf2.close()
    print()
    
    # Test 3: Larger uncertainty
    print("=== Test 3: Larger uncertainty (0.5 nm) ===")
    lltf3 = LLTF("lltf_wrapper/xml_files/M000010263.xml")
    lltf3.initialize(simulate=True, uncertainty=0.5)
    lltf3.set_wavelength(600.0)
    measured_wavelength = lltf3.get_wavelength()
    print("Set wavelength: 600.0 nm")
    print(f"Measured wavelength: {measured_wavelength:.3f} nm")
    print(f"Difference: {measured_wavelength - 600.0:.3f} nm")
    lltf3.close()
    print()
    
    # Test 4: Multiple measurements with same device (offset should be constant)
    print("=== Test 4: Multiple measurements (offset should be constant) ===")
    lltf4 = LLTF("lltf_wrapper/xml_files/M000010263.xml")
    lltf4.initialize(simulate=True, uncertainty=0.3)
    
    wavelengths_to_test = [500.0, 600.0, 700.0]
    for wl in wavelengths_to_test:
        lltf4.set_wavelength(wl)
        measured = lltf4.get_wavelength()
        offset = measured - wl
        print(f"Set: {wl:.1f} nm → Measured: {measured:.3f} nm → Offset: {offset:.3f} nm")
    
    lltf4.close()
    print()
    
    # Test 5: Multiple devices should have different offsets
    print("=== Test 5: Multiple devices (different offsets) ===")
    devices = []
    for i in range(3):
        lltf = LLTF("lltf_wrapper/xml_files/M000010263.xml")
        lltf.initialize(simulate=True, uncertainty=0.2)
        lltf.set_wavelength(600.0)
        measured = lltf.get_wavelength()
        offset = measured - 600.0
        print(f"Device {i + 1}: Offset = {offset:.3f} nm")
        devices.append(lltf)
    
    # Clean up
    for lltf in devices:
        lltf.close()


if __name__ == "__main__":
    test_uncertainty_functionality()
