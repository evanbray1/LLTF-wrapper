"""
LLTF Python Wrapper

A Python wrapper for the NKT Photonics Laser Line Tunable Filter (LLTF) DLL.
This module provides a class-based interface to control LLTF devices with
automatic grating selection and error handling.

Author: Evan Bray
Date: 2025
"""

import ctypes as ct
from ctypes import byref
import os
import glob
import xml.etree.ElementTree as ET
from typing import Optional, List
import warnings


class LLTFError(Exception):
    """Custom exception for LLTF-related errors."""
    pass


class LLTF:
    """
    Python wrapper for NKT Photonics LLTF (Laser Line Tunable Filter).
    
    This class provides a high-level interface to control LLTF devices,
    with automatic grating selection based on wavelength ranges defined
    in the device's XML configuration file.
    """
    
    # PE_STATUS constants from PE_Filter.h
    PE_SUCCESS = 0
    PE_INVALID_HANDLE = 1
    PE_FAILURE = 2
    PE_MISSING_CONFIGFILE = 3
    PE_INVALID_CONFIGURATION = 4
    PE_INVALID_WAVELENGTH = 5
    PE_MISSSING_HARMONIC_FILTER = 6
    PE_INVALID_FILTER = 7
    PE_UNKNOWN = 8
    PE_INVALID_GRATING = 9
    PE_INVALID_BUFFER = 10
    PE_INVALID_BUFFER_SIZE = 11
    PE_UNSUPPORTED_CONFIGURATION = 12
    PE_NO_FILTER_CONNECTED = 13
    
    def __init__(self, xml_config_path: Optional[str] = None):
        """
        Initialize LLTF wrapper.
        
        Args:
            xml_config_path: Path to device XML configuration file.
                           If None, will search for XML files in current directory.
        """
        self.dll = None
        self.handle = None
        self.xml_path = xml_config_path
        self.grating_ranges = []
        self.system_name = None
        self.simulate_mode = False
        self.simulated_wavelength = 550.0  # Default starting wavelength for simulation
        
        # Load XML configuration
        self._load_xml_config()
        
    def _load_xml_config(self) -> None:
        """Load and parse XML configuration file."""
        if self.xml_path is None:
            # Search for XML files in xml_files directory
            xml_files = glob.glob("xml_files/*.xml")
            if not xml_files:
                raise LLTFError("No XML configuration files found. Please provide xml_config_path or place XML file in xml_files directory.")
            elif len(xml_files) > 1:
                warnings.warn(f"Multiple XML files found: {xml_files}. Using {xml_files[0]}")
                self.xml_path = xml_files[0]
            else:
                self.xml_path = xml_files[0]
        
        if not os.path.exists(self.xml_path):
            raise LLTFError(f"XML configuration file not found: {self.xml_path}")
            
        # Parse XML to extract grating information
        try:
            tree = ET.parse(self.xml_path)
            root = tree.getroot()
            
            # Extract system name from Component Id
            component = root.find('.//Component[@Type="Filter"]')
            if component is not None:
                self.system_name = component.get('Id')
            else:
                raise LLTFError("Could not find Filter component in XML configuration")
            
            # Extract grating ranges
            gratings = root.findall('.//Grating')
            for i, grating in enumerate(gratings):
                range_elem = grating.find('Range')
                if range_elem is not None:
                    reg_lower = float(range_elem.find('RegLower').text)
                    reg_upper = float(range_elem.find('RegUpper').text)
                    ext_lower = float(range_elem.find('ExtLower').text)
                    ext_upper = float(range_elem.find('ExtUpper').text)
                    
                    grating_info = {
                        'index': i,
                        'regular_range': (reg_lower, reg_upper),
                        'extended_range': (ext_lower, ext_upper)
                    }
                    self.grating_ranges.append(grating_info)
                    
        except ET.ParseError as e:
            raise LLTFError(f"Failed to parse XML configuration: {e}")
        except Exception as e:
            raise LLTFError(f"Error reading XML configuration: {e}")
    
    def _load_dll(self) -> None:
        """Load the PE_Filter_SDK.dll library."""
        if self.simulate_mode:
            return  # Skip DLL loading in simulation mode
            
        try:
            self.dll = ct.CDLL("PE_Filter_SDK.dll", "PE_Filter")
        except OSError as e:
            raise LLTFError(f"Failed to load PE_Filter_SDK.dll: {e}")
    
    def _check_status(self, status: int, operation: str) -> None:
        """
        Check PE_STATUS return value and raise exception if error.
        
        Args:
            status: PE_STATUS return value
            operation: Description of operation for error message
        """
        if status != self.PE_SUCCESS:
            error_msg = f"{operation} failed with status {status}"
            
            # Map common error codes to descriptive messages
            error_descriptions = {
                self.PE_INVALID_HANDLE: "Invalid handle",
                self.PE_FAILURE: "Instrument communication failure", 
                self.PE_MISSING_CONFIGFILE: "Configuration file missing",
                self.PE_INVALID_CONFIGURATION: "Configuration file corrupted",
                self.PE_INVALID_WAVELENGTH: "Wavelength out of bounds",
                self.PE_INVALID_GRATING: "Invalid grating specified",
                self.PE_NO_FILTER_CONNECTED: "No filter connected"
            }
            
            if status in error_descriptions:
                error_msg += f": {error_descriptions[status]}"
                
            raise LLTFError(error_msg)
    
    def _select_grating_for_wavelength(self, wavelength: float) -> int:
        """
        Select appropriate grating based on wavelength.
        
        Args:
            wavelength: Target wavelength in nanometers
            
        Returns:
            Grating index (0 or 1)
            
        Raises:
            LLTFError: If wavelength is not supported by any grating
        """
        for grating in self.grating_ranges:
            reg_min, reg_max = grating['regular_range']
            if reg_min <= wavelength <= reg_max:
                return grating['index']
        
        # Check extended ranges if not in regular range
        for grating in self.grating_ranges:
            ext_min, ext_max = grating['extended_range']
            if ext_min <= wavelength <= ext_max:
                warnings.warn(f"Wavelength {wavelength} nm is in extended range for grating {grating['index']}")
                return grating['index']
        
        # Build error message with available ranges
        ranges_str = []
        for grating in self.grating_ranges:
            reg_min, reg_max = grating['regular_range']
            ranges_str.append(f"Grating {grating['index']}: {reg_min}-{reg_max} nm")
        
        raise LLTFError(f"Wavelength {wavelength} nm not supported. Available ranges: {', '.join(ranges_str)}")
    
    def initialize(self, simulate: bool = False) -> None:
        """
        Initialize connection to LLTF device.
        
        Args:
            simulate: If True, create virtual device for development/testing
        """
        self.simulate_mode = simulate
        
        if simulate:
            # Create a dummy handle for simulation mode
            self.handle = ct.c_void_p(1)  # Non-null handle for simulation
            print("LLTF: Initialized in simulation mode")
            return
            
        # Load DLL and create handle
        self._load_dll()
        
        # Create handle
        h = ct.c_void_p
        self.handle = h(0)
        
        # Create resource with XML config
        xml_path_c = self.xml_path.encode('utf-8')
        status = self.dll.PE_Create(xml_path_c, byref(self.handle))
        self._check_status(status, "PE_Create")
        
        # Open device
        if self.system_name:
            system_name_c = self.system_name.encode('utf-8')
            status = self.dll.PE_Open(self.handle, system_name_c)
            self._check_status(status, "PE_Open")
    
    def get_connected_device_count(self) -> int:
        """
        Get number of connected LLTF devices.
        
        Returns:
            Number of connected devices
        """
        if self.simulate_mode:
            return 1
            
        if self.handle is None:
            raise LLTFError("Device not initialized. Call initialize() first.")
            
        count = self.dll.PE_GetSystemCount(self.handle)
        return count
    
    def get_wavelength(self) -> float:
        """
        Get current wavelength setting.
        
        Returns:
            Current wavelength in nanometers
        """
        if self.simulate_mode:
            # Return the currently simulated wavelength
            return self.simulated_wavelength
            
        if self.handle is None:
            raise LLTFError("Device not initialized. Call initialize() first.")
            
        wavelength = ct.c_double()
        status = self.dll.PE_GetWavelength(self.handle, byref(wavelength))
        self._check_status(status, "PE_GetWavelength")
        
        return wavelength.value
    
    def set_wavelength(self, wavelength: float, grating: Optional[int] = None) -> None:
        """
        Set target wavelength with automatic or manual grating selection.
        
        Args:
            wavelength: Target wavelength in nanometers
            grating: Optional grating index (0 or 1). If None, will auto-select
        """
        if self.handle is None:
            raise LLTFError("Device not initialized. Call initialize() first.")
        
        # Auto-select grating if not specified
        if grating is None:
            grating = self._select_grating_for_wavelength(wavelength)
        
        # Validate grating index
        if grating not in [0, 1]:
            raise LLTFError(f"Invalid grating index: {grating}. Must be 0 or 1.")
            
        if self.simulate_mode:
            self.simulated_wavelength = wavelength
            print(f"LLTF: Set wavelength to {wavelength} nm (simulation)")
            return
            
        # Set wavelength on specific grating
        status = self.dll.PE_SetWavelengthOnGrating(self.handle, grating, ct.c_double(wavelength))
        self._check_status(status, f"PE_SetWavelengthOnGrating(grating={grating})")
    
    def get_grating_ranges(self) -> List[dict]:
        """
        Get wavelength ranges for all gratings.
        
        Returns:
            List of dictionaries containing grating information
        """
        return self.grating_ranges.copy()
    
    def close(self) -> None:
        """Close connection to LLTF device."""
        if self.simulate_mode:
            print("LLTF: Closed simulation connection")
            return
            
        if self.handle is not None:
            status = self.dll.PE_Close(self.handle)
            try:
                self._check_status(status, "PE_Close")
            except LLTFError:
                pass  # Continue cleanup even if close fails
            
            # Destroy handle
            if self.dll:
                self.dll.PE_Destroy(self.handle)
            
            self.handle = None
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - ensures proper cleanup."""
        self.close()