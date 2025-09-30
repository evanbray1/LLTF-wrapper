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

1. Clone this repository:
   ```bash
   git clone https://github.com/evanbray1/LLTF-tools.git
   cd LLTF-tools
   ```

2. **Install PE_Filter SDK**: You must install the PE_Filter SDK provided by Photon Etc. This includes the `PE_Filter_SDK.dll` library that must be accessible to your Python environment (either in your system PATH or in the same directory as `lltf_wrapper.py`).

3. **Place XML Configuration**: Place your device's XML configuration file in the `xml_files/` directory:
   - Your XML file should be named with your device's serial number (e.g., `M000010263.xml`)
   - This file is provided by NKT Photonics and contains critical device specifications
   - The wrapper will automatically detect XML files in the `xml_files/` directory

## Quick Start

### Basic Usage

```python
from lltf_wrapper import LLTF, LLTFError

# Initialize LLTF (automatically finds XML file in xml_files/ directory)
lltf = LLTF()

# Connect to device
lltf.initialize()

# Set wavelength (auto-selects appropriate grating)
lltf.set_wavelength(550)  # nm

# Get current wavelength
current_wl = lltf.get_wavelength()
print(f"Current wavelength: {current_wl} nm")

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
    print(f"Set to: {wavelength} nm")
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

## Demo Scripts

### Basic Demo
For quick start with minimal code:

```bash
python examples/demo_basic.py
```

### Advanced Demo
For comprehensive examples and features:

```bash
python examples/demo_advanced.py
```

The demo scripts demonstrate:
- Basic initialization and connection
- Wavelength setting with automatic grating selection
- Manual grating selection
- Error handling for invalid wavelengths
- Context manager usage
- Simulation mode

## Requirements

- Python 3.6+
- Windows (required for PE_Filter_SDK.dll)
- PE_Filter SDK from Photon Etc (includes PE_Filter_SDK.dll)
- Device XML configuration file (placed in xml_files/ directory)

## Grating Selection Logic

The LLTF has two internal gratings, each covering different wavelength ranges:

1. **Automatic Selection** (default): The wrapper automatically chooses the grating based on your target wavelength and the ranges defined in your device's XML file.

2. **Manual Selection**: You can force a specific grating using the `grating` parameter:
   ```python
   lltf.set_wavelength(600, grating=0)  # Force grating 0
   ```

3. **Range Validation**: The wrapper validates wavelengths against both regular and extended ranges, issuing warnings for extended range usage.

## Troubleshooting

### "No XML configuration files found"
- Ensure your device's XML file is in the `xml_files/` directory
- Check that the file has a `.xml` extension

### "Failed to load PE_Filter_SDK.dll"
- Ensure you have installed the PE_Filter SDK from Photon Etc
- Make sure `PE_Filter_SDK.dll` is in your system PATH or in the same directory as `lltf_wrapper.py`
- Verify you're running on Windows (DLL requirement)

### "Wavelength X nm not supported"
- Check your device's specifications using `get_grating_ranges()`
- Verify the wavelength is within your device's capabilities