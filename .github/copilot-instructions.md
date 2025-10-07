# GitHub Copilot Instructions for LLTF-wrapper

## Project Overview

This project provides a Python wrapper for the NKT Photonics Laser Line Tunable Filter (LLTF) DLL. The wrap4. Handle ctypes conversion for parameters
5. Add error checking with `_check_status()`
6. Implement simulation behavior
7. Add to `examples/demo_basic.py` or `examples/demo_advanced.py` for testing
8. Update README.md documentationbstracts the low-level C DLL interface into a clean Python API with automatic grating selection and comprehensive error handling.

## Architecture

### Core Components

1. **`lltf_wrapper/lltf_wrapper.py`** - Main wrapper module
   - `LLTF` class: Primary interface for device control
   - `LLTFError` exception: Custom exception for device errors
   - XML parsing for device configuration
   - Simulation mode for development/testing

2. **`lltf_wrapper/__init__.py`** - Package initialization
   - Exports main classes: `LLTF`, `LLTFError`
   - Package metadata and version information

3. **`examples/`** - Demo and example scripts
   - `demo_basic.py`: Minimal usage example for getting started
   - `demo_advanced.py`: Comprehensive feature demonstration
   - Shows both simulation and real device usage patterns
   - Includes error handling examples

4. **`setup.py`** - Package installation configuration
   - Enables `pip install .` for local development
   - Includes package metadata and dependencies
   - Handles XML file inclusion via package_data

3. **External Dependencies**
   - `PE_Filter_SDK.dll` - NKT Photonics proprietary DLL
   - Device XML files - Contain grating specifications and calibration data

### Key Design Patterns

- **Context Manager**: LLTF class supports `with` statements for automatic cleanup
- **Auto-discovery**: XML configuration files are automatically detected
- **Graceful Degradation**: Simulation mode allows development without hardware
- **Type Safety**: Full type hints throughout the codebase

## Development Guidelines

### When Adding New Features

1. **Follow Existing Patterns**
   - Use type hints for all function parameters and return values
   - Add comprehensive docstrings following the existing format
   - Include both simulation and real hardware code paths
   - Add proper error checking with `_check_status()`

2. **Error Handling**
   - Always check PE_STATUS return values from DLL calls
   - Use `_check_status()` helper method consistently
   - Provide meaningful error messages that include context
   - Map PE_STATUS codes to descriptive messages where possible

3. **Testing Considerations**
   - All new functionality should work in simulation mode
   - Add test cases to `examples/demo_basic.py` or `examples/demo_advanced.py` for new features
   - Consider edge cases and invalid inputs
   - Test with both automatic and manual grating selection

### Code Conventions

```python
# Function signatures should include type hints
def new_method(self, param: float, optional_param: Optional[int] = None) -> str:
    """
    Brief description of what the method does.
    
    Args:
        param: Description of the parameter
        optional_param: Description of optional parameter
        
    Returns:
        Description of return value
        
    Raises:
        LLTFError: When this error occurs
    """
    
    # Check initialization
    if self.handle is None:
        raise LLTFError("Device not initialized. Call initialize() first.")
    
    # Handle simulation mode early
    if self.simulate_mode:
        # Simulation logic here
        return "simulated_result"
    
    # Real hardware implementation
    status = self.dll.SomeFunction(self.handle, param)
    self._check_status(status, "SomeFunction")
    
    return result
```

### DLL Interface Patterns

When adding new DLL function wrappers:

1. **Input Parameters**: Convert Python types to ctypes
   ```python
   # Strings
   string_param_c = string_param.encode('utf-8')
   
   # Numeric outputs
   result = ct.c_double()
   status = self.dll.Function(self.handle, byref(result))
   return result.value
   ```

2. **Error Checking**: Always check status codes
   ```python
   status = self.dll.PE_SomeFunction(self.handle, parameters)
   self._check_status(status, "PE_SomeFunction")
   ```

3. **Buffer Management**: For string outputs
   ```python
   buffer_size = 256
   buffer = ct.create_string_buffer(buffer_size)
   status = self.dll.PE_GetString(self.handle, buffer, buffer_size)
   self._check_status(status, "PE_GetString")
   return buffer.value.decode('utf-8')
   ```

### XML Configuration Handling

When extending XML parsing:

1. **Use ElementTree**: Continue using `xml.etree.ElementTree`
2. **Handle Missing Elements**: Always check if elements exist before accessing
3. **Provide Context**: Include XML file path in error messages
4. **Validate Data**: Convert and validate numeric values from XML

```python
try:
    element = root.find('.//SomeElement')
    if element is not None:
        value = float(element.text)
    else:
        raise LLTFError("Required element 'SomeElement' not found in XML")
except ValueError as e:
    raise LLTFError(f"Invalid numeric value in XML: {e}")
```

### Testing New Features

1. **Simulation First**: Implement and test simulation mode behavior
2. **Demo Integration**: Add examples to `examples/demo_basic.py` or `examples/demo_advanced.py`
3. **Error Scenarios**: Test invalid inputs and error conditions
4. **Documentation**: Update README.md with new functionality

### Common DLL Functions to Wrap

If extending the wrapper, consider these PE_Filter.h functions:

- `PE_GetGratingCount()` - Number of gratings
- `PE_GetGratingName()` - Grating identification  
- `PE_GetGratingWavelengthRange()` - Wavelength ranges
- `PE_SetWavelengthOnGrating()` - Grating-specific wavelength setting
- `PE_GetGrating()` - Current active grating
- `PE_SetBroadband()` / `PE_IsBroadband()` - Broadband mode control

### Backwards Compatibility

- Maintain existing method signatures
- Add new optional parameters with sensible defaults
- Don't remove or rename public methods without deprecation
- Keep simulation mode working for all existing functionality

## Common Development Tasks

### Adding a New DLL Function Wrapper

1. Identify the C function signature in `PE_Filter.h`
2. Create corresponding Python method with type hints
3. Handle ctypes conversion for parameters
4. Add error checking with `_check_status()`
5. Implement simulation behavior
6. Add to `demo.py` for testing
7. Update README.md documentation

### Extending XML Configuration Support

1. Examine XML structure for new elements
2. Add parsing logic to `_load_xml_config()`
3. Store parsed data in instance variables
4. Create getter methods to access the data
5. Handle missing or invalid XML gracefully

### Adding New Error Conditions

1. Add new PE_STATUS constants if needed
2. Update `error_descriptions` in `_check_status()`
3. Create specific exception handling where appropriate
4. Test error scenarios in simulation mode

## Performance Considerations

- XML parsing happens once during initialization
- DLL calls are synchronous - consider this for UI applications
- Simulation mode should be fast for development workflows
- Cache device information to avoid repeated DLL calls

## Security Notes

- XML files come from trusted sources (NKT Photonics)
- No user input is directly passed to DLL without validation
- Simulation mode doesn't access real hardware
- Always validate wavelength ranges against device specifications

## Future Enhancement Ideas

- Async/await support for long operations
- Device discovery and auto-connection
- Wavelength scanning utilities
- Configuration validation tools
- Multiple device support
- Logging integration
- Unit test framework
- Package installation support