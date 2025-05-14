# Tony Nordstrom
# Oct 17 2023
# BACnet Test
# Open Wireshark, filter ip.addr == 192.168.20.65
# Using the BAC0 library for BACnet communications
# See https://bac0.readthedocs.io/en/latest/index.html

import BAC0
import time

# Logging level being one of 'debug, info, warning, error'
BAC0.log_level(stdout = 'debug')
# The more verbose the logging level, the slower the program runs

from bacpypes.primitivedata import Real, BitString, Unsigned, Enumerated, Date, Null
#from bacpypes.app import DeviceObject
from bacpypes.object import DeviceObject
from BAC0.core.proprietary_objects.object import create_proprietary_object

RCCDeviceObject = {
	"name": "RCC_DeviceObject",
	"vendor_id": 35,
	"objectType": "device",
	"bacpypes_type": DeviceObject,
	"properties": {
		"ObjectList": {"obj_id": 1113, "datatype": Unsigned, "mutable": False},
		"ScanRate": {"obj_id": 2048, "datatype": Real, "mutable": False},
	},
}

create_proprietary_object(RCCDeviceObject)

# Connect to R&D LAN IP address / Subnet mask in # bits
bacnet = BAC0.connect(ip='192.168.17.186/21')

# Define a device (or multiple devices) device IP address: UDP port, Device ID, interface, poll rate
device1 = BAC0.device('192.168.20.4:47345', 1000, bacnet, poll=60)
#device2 = BAC0.device('192.168.20.79:47345', 7000, bacnet, poll=60)
#device3 = BAC0.device('192.168.20.71:47345', 50000, bacnet, poll=60)
#device4 = BAC0.device('192.168.17.189:47345', 100000, bacnet, poll=60)

#bacnet.devices
bacnet.registered_devices

print(device1.points)

# How do you specify proprietary properties?
# Read property multiple, data (depends on # of objects defined on the device)
_rpm = {'address': '192.168.20.4:47345',
        'objects': {
            #'device:1000': ['localTime', 'localDate', 'objectList', 'systemStatus', 'utcOffset', 'deviceAddressBinding', '@prop_1113'],
            #'device:1000': ['all', '@prop_1113'],
            'device:1000': ['@prop_1113', '@prop_2048'],
            #'analogInput:2': ['objectName', 'presentValue', 'statusFlags', 'units','description']
            #'analogInput:2': ['all']
            }
        }

# Main loop: repeatedly send a readMultiple request:

i = 0
while ( True ):
	print('test #', i)
	i = i + 1
	bacnet.readMultiple(device1, request_dict=_rpm, vendor_id=35)
	# time.sleep(1) # Optional throttling in # seconds

# Future enhancement: compare received dict with previous, see if there's any differences.
# https://bac0.readthedocs.io/en/latest/read.html
# https://bac0.readthedocs.io/en/latest/histories.html # Histories shows historical data

# Future enhancement 2: write values to all writable properties, read back, see if the writes worked.