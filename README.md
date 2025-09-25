# LLTF Python Wrapper

A Python wrapper for the NKT Photonics Laser Line Tunable Filter (LLTF) DLL. This wrapper provides a clean, class-based interface for controlling LLTF devices with automatic grating selection and comprehensive error handling.

## Features

- **Automatic Grating Selection**: Automatically selects the appropriate grating (0 or 1) based on the target wavelength and device specifications
- **Error Handling**: Comprehensive error checking with meaningful Python exceptions
- **Simulation Mode**: Virtual device support for development and testing without hardware
- **Type Hints**: Full type annotation support for better IDE integration
- **Context Manager**: Supports `with` statement for automatic resource cleanup
- **XML Configuration**: Reads device specifications directly from manufacturer-provided XML files

## Installation

1. Clone this repository to a system-locatable directory:
   ```bash
   git clone https://github.com/evanbray1/LLTF-tools.git
   cd LLTF-tools
   ```

2. **Important**: Place your device's XML configuration file in the same directory as the Python files. 
   - Your XML file should be named with your device's serial number (e.g., `M000010263.xml`)
   - This file is provided by NKT Photonics and contains critical device specifications
   - The wrapper will automatically detect XML files in the current directory

3. Ensure the following files are present:
   - `PE_Filter_SDK.dll` - NKT Photonics DLL library
   - `lltf_wrapper.py` - Main wrapper module
   - Your device's `.xml` configuration file

## Quick Start

### Basic Usage

```python
from lltf_wrapper import LLTF, LLTFError

# Initialize LLTF (automatically finds XML file)
lltf = LLTF()

# Connect to device
lltf.initialize()

# Set wavelength (auto-selects appropriate grating)
lltf.set_wavelength(550)  # nm

# Get current wavelength
current_wl = lltf.get_wavelength()
print(f"Current wavelength: {current_wl}nm")

# Close connection
lltf.close()
```

### Using Context Manager (Recommended)

```python
from lltf_wrapper import LLTF

with LLTF() as lltf:
    lltf.initialize()
    lltf.set_wavelength(650)
    wavelength = lltf.get_wavelength()
    print(f"Set to: {wavelength}nm")
# Connection automatically closed
```

### Simulation Mode (for Development)

```python
from lltf_wrapper import LLTF

lltf = LLTF()
lltf.initialize(simulate=True)  # No hardware required

# All methods work the same way
lltf.set_wavelength(750)
current = lltf.get_wavelength()
lltf.close()
```

## API Reference

### LLTF Class

#### `__init__(xml_config_path=None)`
Initialize the LLTF wrapper.
- `xml_config_path` (optional): Path to XML config file. If None, searches current directory.

#### `initialize(simulate=False)`
Establish connection to the LLTF device.
- `simulate`: If True, creates virtual device for testing.

#### `get_wavelength()`
Returns the current wavelength setting in nanometers.

#### `set_wavelength(wavelength, grating=None)`
Set the target wavelength.
- `wavelength`: Target wavelength in nanometers
- `grating` (optional): Force specific grating (0 or 1). If None, auto-selects.

#### `get_connected_device_count()`
Returns the number of connected LLTF devices.

#### `get_grating_ranges()`
Returns list of dictionaries containing grating specifications:
```python
[
    {
        'index': 0,
        'regular_range': (400.0, 650.0),
        'extended_range': (350.0, 700.0)
    },
    {
        'index': 1, 
        'regular_range': (650.0, 1000.0),
        'extended_range': (550.0, 1100.0)
    }
]
```

#### `close()`
Close connection and cleanup resources.

### Error Handling

The wrapper raises `LLTFError` exceptions for device-related errors:

```python
from lltf_wrapper import LLTF, LLTFError

try:
    lltf = LLTF()
    lltf.initialize()
    lltf.set_wavelength(1500)  # Out of range
except LLTFError as e:
    print(f"Error: {e}")
```

## File Structure

Your working directory should contain:

```
your-project/
├── lltf_wrapper.py          # Main wrapper module
├── demo.py                  # Example usage script
├── PE_Filter_SDK.dll        # NKT Photonics DLL
├── PE_Filter.h              # C header (reference)
├── M000010XXX.xml           # Your device's XML config file
└── README.md                # This file
```

## XML Configuration File Placement

**Critical**: Your device's XML configuration file must be placed in the same directory as the Python wrapper files. 

- The XML file contains essential device specifications including grating wavelength ranges
- Without this file, the wrapper cannot determine valid wavelength ranges for your specific device
- The file is typically named with your device's serial number (e.g., `M000010263.xml`)
- If multiple XML files are present, the wrapper will use the first one found and issue a warning

## Demo Script

Run the included demo to test functionality:

```bash
python demo.py
```

The demo script demonstrates:
- Basic initialization and connection
- Wavelength setting with automatic grating selection
- Manual grating selection
- Error handling for invalid wavelengths
- Context manager usage
- Simulation mode

## Grating Selection Logic

The LLTF has two internal gratings, each covering different wavelength ranges:

1. **Automatic Selection** (default): The wrapper automatically chooses the grating based on your target wavelength and the ranges defined in your device's XML file.

2. **Manual Selection**: You can force a specific grating using the `grating` parameter:
   ```python
   lltf.set_wavelength(600, grating=0)  # Force grating 0
   ```

3. **Range Validation**: The wrapper validates wavelengths against both regular and extended ranges, issuing warnings for extended range usage.

## Requirements

- Python 3.6+
- Windows (required for PE_Filter_SDK.dll)
- Device XML configuration file
- NKT Photonics PE_Filter_SDK.dll

## Troubleshooting

### "No XML configuration files found"
- Ensure your device's XML file is in the same directory as `lltf_wrapper.py`
- Check that the file has a `.xml` extension

### "Failed to load PE_Filter_SDK.dll"
- Ensure `PE_Filter_SDK.dll` is in the same directory as `lltf_wrapper.py`
- Make sure you're running on Windows (DLL requirement)

### "Wavelength X nm not supported"
- Check your device's specifications using `get_grating_ranges()`
- Verify the wavelength is within your device's capabilities

## Development

For development without hardware, use simulation mode:

```python
lltf = LLTF()
lltf.initialize(simulate=True)
# Develop and test your code
```

## License

This wrapper is provided as-is for use with NKT Photonics LLTF devices. The underlying PE_Filter_SDK.dll is proprietary to NKT Photonics.

## Support

For issues with this wrapper, please open an issue on the GitHub repository.
For hardware or DLL-related issues, contact NKT Photonics support.