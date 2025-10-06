# LLTF Uncertainty Feature

## Overview

The LLTF wrapper now supports simulating measurement uncertainty when running in simulation mode. This feature adds an artificial offset to wavelength measurements to simulate real-world device behavior.

## Usage

```python
from lltf_wrapper import LLTF

# Initialize with uncertainty simulation
lltf = LLTF("path/to/device.xml")
lltf.initialize(simulate=True, uncertainty=0.1)  # 0.1 nm standard deviation

# Set a wavelength
lltf.set_wavelength(600.0)

# Get wavelength with simulated uncertainty
measured = lltf.get_wavelength()
print(f"Set: 600.0 nm, Measured: {measured:.3f} nm")
# Output: Set: 600.0 nm, Measured: 600.523 nm (example)
```

## Parameters

- `uncertainty` (float): Standard deviation for the artificial offset in nanometers
  - Default: 0.0 (no offset, maintains backward compatibility)
  - The offset is drawn from a normal distribution with mean=0.5nm and sigma=uncertainty
  - Each device instance gets a fixed offset that remains constant for all measurements

## Behavior

### When uncertainty=0.0 (default)
- No offset is applied
- `get_wavelength()` returns exactly the wavelength set by `set_wavelength()`
- Maintains backward compatibility with existing code

### When uncertainty>0.0
- A random offset is generated during `initialize()` 
- The offset follows: N(mean=0.5, sigma=uncertainty)
- The same offset is applied to all wavelength measurements for that device instance
- Different device instances will have different offsets

## Examples

### No uncertainty (default behavior)
```python
lltf = LLTF("device.xml")
lltf.initialize(simulate=True)  # uncertainty defaults to 0.0
lltf.set_wavelength(600.0)
print(lltf.get_wavelength())  # Output: 600.0
```

### Small uncertainty
```python
lltf = LLTF("device.xml")
lltf.initialize(simulate=True, uncertainty=0.1)  # 0.1nm standard deviation
lltf.set_wavelength(600.0)
print(lltf.get_wavelength())  # Output: ~600.5 ± 0.1 nm
```

### Multiple measurements (same device)
```python
lltf = LLTF("device.xml")
lltf.initialize(simulate=True, uncertainty=0.2)

for wavelength in [500.0, 600.0, 700.0]:
    lltf.set_wavelength(wavelength)
    measured = lltf.get_wavelength()
    offset = measured - wavelength
    print(f"Set: {wavelength}, Measured: {measured:.3f}, Offset: {offset:.3f}")

# All offsets will be identical for the same device instance
```

### Multiple devices (different offsets)
```python
devices = []
for i in range(3):
    lltf = LLTF("device.xml")
    lltf.initialize(simulate=True, uncertainty=0.15)
    lltf.set_wavelength(600.0)
    measured = lltf.get_wavelength()
    print(f"Device {i+1}: {measured:.3f} nm")
    devices.append(lltf)

# Each device will have a different offset
```

## Notes

- This feature only works in simulation mode (`simulate=True`)
- The offset is generated once during initialization and remains constant
- Real hardware mode is unaffected by this parameter
- The feature maintains full backward compatibility