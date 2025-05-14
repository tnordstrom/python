# Tony Nordstrom
# December 13 2023
# BACnet Object Creation
# Open Wireshark, filter ip.addr == 192.168.20.4
# Using the BAC0 library for BACnet communications
# See https://bac0.readthedocs.io/en/latest/index.html
# History
###################################

import BAC0
import time

# Logging level being one of 'debug, info, warning, error'
BAC0.log_level(stdout = 'debug')
# The more verbose the logging level, the slower the program runs

from bacpypes.primitivedata import Real, BitString, Date, OctetString, Unsigned, Enumerated, Date, Null, CharacterString, ObjectIdentifier, Boolean
#from bacpypes.app import DeviceObject
from bacpypes.object import DeviceObject
from BAC0.core.proprietary_objects.object import create_proprietary_object

RCCDeviceObject = {
	"name": "RCC_DeviceObject",
	"vendor_id": 35,
	"objectType": "device",
	"bacpypes_type": DeviceObject,
	"properties": {
		"ObjInstSupp": {"obj_id": 1347, "datatype": Unsigned, "mutable": False},
	},
}

create_proprietary_object(RCCDeviceObject)

# Connect to R&D LAN IP address / Subnet mask in # bits
bacnet = BAC0.connect(ip='192.168.17.186/21')

# Define a device (or multiple devices) device IP address: UDP port, Device ID, interface, poll rate
device1 = BAC0.device('192.168.20.134:47345', 9191, bacnet, poll=60)
#device2 = BAC0.device('192.168.20.79:47345', 7000, bacnet, poll=60)
#device3 = BAC0.device('192.168.20.71:47345', 50000, bacnet, poll=60)
#device4 = BAC0.device('192.168.17.189:47345', 100000, bacnet, poll=60)

#bacnet.devices
#bacnet.registered_devices

#print(device1.points)

_rpm = {'address': '192.168.20.134:47345',
        'objects': {
            #'device:9191': ['@prop_1347'],
            'device:9191': ['all'],
            }
        }

#BAC0.core.io.Read.readMultiple
#BAC0.core.devices.create_objects.create_object(
bacnet.create_object(analog_value, device1, "TEST1", "Did this just get created?", presentValue=1.0, commandable=True)	# AttributeError: 'Lite' object has no attribute 'create_object'
#bacnet.create_AV(oid=1,pv=123,name='AVx',units=Volts,pv_writable=True)
#bacnet.readMultiple(device1, request_dict=_rpm, vendor_id=35)	# bacpypes.errors.DecodingError: too many cast components

# Future enhancement: compare received dict with previous, see if there's any differences.
# https://bac0.readthedocs.io/en/latest/read.html
# https://bac0.readthedocs.io/en/latest/histories.html # Histories shows historical data

# Future enhancement 2: write values to all writable properties, read back, see if the writes worked.