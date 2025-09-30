#!/usr/bin/env python3
"""
LLTF Wrapper Advanced Demo

This script demonstrates comprehensive usage of the LLTF Python wrapper.
It shows initialization, error handling, context managers, XML configuration,
automatic grating selection, and various usage patterns.

For basic usage, see demo_basic.py instead.
Run with simulation mode to test without actual hardware.
"""

import sys
import os
try:
    from lltf_wrapper import LLTF, LLTFError
except ImportError:
    # Add parent directory to path to import lltf_wrapper
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from lltf_wrapper import LLTF, LLTFError


def demo_basic_usage():
    """Demonstrate basic LLTF wrapper usage."""
    print("=== LLTF Wrapper Demo ===\n")

    try:
        # Initialize LLTF wrapper (specify XML path relative to parent directory)
        lltf = LLTF(xml_config_path="../xml_files/M000010263.xml")
        print(f"✓ LLTF wrapper initialized with config: {lltf.xml_path}")
        print(f"  System name: {lltf.system_name}")
        print(f"  Found {len(lltf.grating_ranges)} gratings")

        # Display grating information
        print("\nGrating Information:")
        for grating in lltf.grating_ranges:
            reg_range = grating['regular_range']
            ext_range = grating['extended_range']
            print(f"  Grating {grating['index']}: {reg_range[0]}-{reg_range[1]} nm "
                  f"(extended: {ext_range[0]}-{ext_range[1]} nm)")

        # Initialize in simulation mode
        print("\n=== Initializing in Simulation Mode ===")
        lltf.initialize(simulate=True)

        # Check connected devices
        device_count = lltf.get_connected_device_count()
        print(f"✓ Connected devices: {device_count}")

        # Get current wavelength
        current_wl = lltf.get_wavelength()
        print(f"✓ Current wavelength: {current_wl} nm")

        # Demonstrate wavelength setting with automatic grating selection
        print("\n=== Testing Wavelength Control ===")

        test_wavelengths = [450, 550, 650, 750, 850]

        for wl in test_wavelengths:
            try:
                # Determine which grating would be used
                grating_idx = lltf._select_grating_for_wavelength(wl)
                lltf.set_wavelength(wl)
                print(f"  ✓ Successfully set to {wl} nm with grating {grating_idx}")
            except LLTFError as e:
                print(f"  ✗ Failed to set {wl} nm: {e}")

        # Test manual grating selection
        print("\n=== Testing Manual Grating Selection ===")
        try:
            print("Setting 600 nm on grating 0 (manual selection)")
            lltf.set_wavelength(600, grating=0)
            print("  ✓ Successfully set with manual grating selection")
        except LLTFError as e:
            print(f"  ✗ Manual grating selection failed: {e}")

        # Test invalid wavelength
        print("\n=== Testing Error Handling ===")
        try:
            print("Attempting to set invalid wavelength (1500 nm)")
            lltf.set_wavelength(1500)
        except LLTFError as e:
            print(f"  ✓ Correctly caught error: {e}")

        # Close connection
        print("\n=== Closing Connection ===")
        lltf.close()
        print("✓ Connection closed successfully")

    except LLTFError as e:
        print(f"✗ LLTF Error: {e}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")


def demo_context_manager():
    """Demonstrate using LLTF wrapper as context manager."""
    print("\n=== Context Manager Demo ===")

    try:
        # Use LLTF as context manager for automatic cleanup
        with LLTF(xml_config_path="../xml_files/M000010263.xml") as lltf:
            lltf.initialize(simulate=True)
            print("✓ LLTF initialized with context manager")

            # Set a few wavelengths
            for wl in [500, 700]:
                lltf.set_wavelength(wl)
                current = lltf.get_wavelength()
                print(f"  Set {wl} nm, current: {current} nm")

        print("✓ Context manager automatically closed connection")

    except LLTFError as e:
        print(f"✗ LLTF Error: {e}")


def demo_xml_path_specification():
    """Demonstrate specifying XML path explicitly."""
    print("\n=== Custom XML Path Demo ===")

    try:
        # Specify XML file explicitly
        xml_path = "../xml_files/M000010263.xml"
        lltf = LLTF(xml_config_path=xml_path)
        print(f"✓ LLTF initialized with explicit XML path: {xml_path}")

        lltf.initialize(simulate=True)

        # Show configuration details
        ranges = lltf.get_grating_ranges()
        print("Grating ranges from XML:")
        for grating in ranges:
            print(f"  Grating {grating['index']}: {grating['regular_range']}")

        lltf.close()

    except LLTFError as e:
        print(f"✗ LLTF Error: {e}")


if __name__ == "__main__":
    # Run all demos
    demo_basic_usage()
    demo_context_manager()
    demo_xml_path_specification()

    print("\n=== Demo Complete ===")
    print("The LLTF wrapper is ready for use!")