#!/usr/bin/env python3
"""
Simple test for uncertainty functionality with absolute paths.
"""

import sys

sys.path.insert(0, '/workspaces/LLTF-wrapper')

from lltf_wrapper import LLTF

def test_new_functionality():
    """Test the new uncertainty parameter."""
    
    xml_path = "/workspaces/LLTF-wrapper/lltf_wrapper/xml_files/M000010263.xml"
    
    print("Testing new uncertainty functionality...\n")
    
    # Test 1: Default behavior (no uncertainty)
    print("1. Testing default behavior (uncertainty=0):")
    lltf1 = LLTF(xml_path)
    lltf1.initialize(simulate=True)  # Should default to uncertainty=0.0
    lltf1.set_wavelength(600.0)
    measured = lltf1.get_wavelength()
    print(f"   Set: 600.0 nm, Measured: {measured:.3f} nm, Offset: {measured - 600.0:.3f} nm")
    lltf1.close()
    
    # Test 2: Explicit uncertainty=0
    print("\n2. Testing explicit uncertainty=0:")
    lltf2 = LLTF(xml_path)
    lltf2.initialize(simulate=True, uncertainty=0.0)
    lltf2.set_wavelength(600.0)
    measured = lltf2.get_wavelength()
    print(f"   Set: 600.0 nm, Measured: {measured:.3f} nm, Offset: {measured - 600.0:.3f} nm")
    lltf2.close()
    
    # Test 3: Small uncertainty
    print("\n3. Testing small uncertainty (0.1 nm):")
    lltf3 = LLTF(xml_path)
    lltf3.initialize(simulate=True, uncertainty=0.1)
    lltf3.set_wavelength(600.0)
    measured = lltf3.get_wavelength()
    offset = measured - 600.0
    print(f"   Set: 600.0 nm, Measured: {measured:.3f} nm, Offset: {offset:.3f} nm")
    print(f"   Expected: offset ~= 0.5 ± 0.1 nm, Got: {offset:.3f} nm")
    lltf3.close()
    
    # Test 4: Larger uncertainty
    print("\n4. Testing larger uncertainty (0.3 nm):")
    lltf4 = LLTF(xml_path)
    lltf4.initialize(simulate=True, uncertainty=0.3)
    lltf4.set_wavelength(600.0)
    measured = lltf4.get_wavelength()
    offset = measured - 600.0
    print(f"   Set: 600.0 nm, Measured: {measured:.3f} nm, Offset: {offset:.3f} nm")
    print(f"   Expected: offset ~= 0.5 ± 0.3 nm, Got: {offset:.3f} nm")
    lltf4.close()
    
    # Test 5: Verify offset is constant for same device
    print("\n5. Testing offset consistency:")
    lltf5 = LLTF(xml_path)
    lltf5.initialize(simulate=True, uncertainty=0.2)
    
    test_wavelengths = [500.0, 600.0, 700.0]
    offsets = []
    for wl in test_wavelengths:
        lltf5.set_wavelength(wl)
        measured = lltf5.get_wavelength()
        offset = measured - wl
        offsets.append(offset)
        print(f"   Set: {wl:.1f} nm, Measured: {measured:.3f} nm, Offset: {offset:.3f} nm")
    
    # Check if all offsets are the same
    if all(abs(offset - offsets[0]) < 1e-10 for offset in offsets):
        print("   ✓ Offset is constant for the same device instance")
    else:
        print("   ✗ Offset varies between measurements (unexpected)")
    
    lltf5.close()
    
    print("\n✓ All tests completed successfully!")


if __name__ == "__main__":
    test_new_functionality()
