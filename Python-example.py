# 2020-10-23

import ctypes as ct
from ctypes import byref

lltflib = ct.CDLL("PE_Filter_SDK.dll","PE_Filter")
lltflib.PE_GetLibraryVersion();
path = "C:/Program Files (x86)/Photon etc/PHySpecV2/Devices/M000010XXX.xml";
path_c = path.encode('utf-8');   # important!!

# create a handle
h = ct.c_void_p;
handle=h(0);
lltflib.PE_Create(path_c,byref(handle));

# check number of devices
lltflib.PE_GetSystemCount(handle);

# open the device
systemname = 'LLTF Contrast M000010XXX';
systemname_c=systemname.encode('utf-8');
lltflib.PE_Open(handle,systemname_c);

# Get wavelength
wl=ct.c_double();
lltflib.PE_GetWavelength(handle,byref(wl))
wl.value

# Set wavelength
lltflib.PE_SetWavelength(handle,ct.c_double(450.0))