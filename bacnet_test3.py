# Tony Nordstrom
# Oct 17 2023
# BACnet Test
# Open Wireshark, filter ip.addr == 192.168.20.4
# Using the BAC0 library for BACnet communications
# See https://bac0.readthedocs.io/en/latest/index.html
# History
# Oct 19 2023 - bacnet_test.py - got two proprietary properties to display on the debug response output
# Oct 26 2023 - bacnet_test2.py	- five different RPM asking for "all" properties from various objects
# Oct xx 2023 - bacnet_test3.py - TBD
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
		"ObjectList": {"obj_id": 1113, "datatype": Unsigned, "mutable": False, 'identifier': 'RCC_ObjectList'},
		"ScanRate": {"obj_id": 2048, "datatype": Real, "mutable": False},
		"CustomUnits": {"obj_id": 1085, "datatype": CharacterString, "mutable": False},
		"NewMasterPassword": {"obj_id":	1120, "datatype": CharacterString, "mutable": False},
		"UserPasswords": {"obj_id":	1118, "datatype": CharacterString, "mutable": False},
		"MstpMacAddress": {"obj_id": 1042, "datatype": Unsigned, "mutable": False}, 
		"SystemName": {"obj_id": 1041, "datatype": CharacterString, "mutable": False},
		"DiagDbMemUsage": {"obj_id": 2067, "datatype": Null, "mutable": False},
		"DiagNvMemUsage": {"obj_id": 2068, "datatype": Null, "mutable": False},
		#"AdvancedFeatureSupport": {"obj_id": 1036, "datatype": Null, "mutable": False},
		"SerialNumber": {"obj_id": 1033, "datatype": CharacterString, "mutable": False},
		"ModelBits": {"obj_id": 1103, "datatype": BitString, "mutable": False},
		"SntpEnable": {"obj_id": 1155, "datatype": Boolean, "mutable": False},
		"SntpServer": {"obj_id": 1156, "datatype": CharacterString, "mutable": False},
		"MacAddress": {"obj_id": 1095, "datatype": OctetString, "mutable": False},
		"MaxModbusEntries": {"obj_id": 1236, "datatype": Unsigned, "mutable": False},
		"PanelConfiguration": {"obj_id": 1117, "datatype": OctetString, "mutable": False},
		"RtcCalibration": {"obj_id": 1105, "datatype": Unsigned, "mutable": False},  # Signed type in fact
		"RtcCalibrationFreq": {"obj_id": 1377, "datatype": Unsigned, "mutable": False},
		"BacnetInCount": {"obj_id": 1104, "datatype": Unsigned, "mutable": False},
		"BacnetInMax": {"obj_id": 1106, "datatype": Unsigned, "mutable": False},
		"BacnetOutCount": {"obj_id": 1086, "datatype": Unsigned, "mutable": False},
		"BacnetOutMax": {"obj_id": 1107, "datatype": Unsigned, "mutable": False},
		"NetOutMaxFreq": {"obj_id": 1176, "datatype": Enumerated, "mutable": False}, 
		"ClientAddrBindCount": {"obj_id": 1168, "datatype": Unsigned, "mutable": False}, 
		"ClientAddrBindMax": {"obj_id": 1169, "datatype": Unsigned, "mutable": False},
		"DstStart": {"obj_id": 1108, "datatype": OctetString, "mutable": False},
		"DstEnd": {"obj_id": 1109, "datatype": OctetString, "mutable": False},
		"DiagChangelist": {"obj_id": 2070, "datatype": CharacterString, "mutable": False},
		"DiagNumPowerCycles": {"obj_id": 2056, "datatype": Unsigned, "mutable": False},
		"DiagReset": {"obj_id": 2071, "datatype": Boolean, "mutable": False},
		#"DiagTimeOfReset": {"obj_id": 2072, "datatype": Date, "mutable": False}, # DateTime in fact
		"HardwareDependencies": {"obj_id": 1044, "datatype": CharacterString, "mutable": False},
		"MppVersionStrings": {"obj_id": 1045, "datatype": CharacterString, "mutable": False},
		#"UtcTimeSyncRecipients": {"obj_id": 1028, "datatype": Null, "mutable": False}, # Complex in fact
		"BackupRestorePwdReqd": {"obj_id": 1029, "datatype": Boolean, "mutable": False},
		#"MstpNetworks": {"obj_id": 1039, "datatype": Null, "mutable": False}, # Array of unsigned16 in fact
		"BtlStrict": {"obj_id": 1136, "datatype": Boolean, "mutable": False},
		"TemplateName": {"obj_id": 1215, "datatype": CharacterString, "mutable": False},
		"ParentDevice": {"obj_id": 1216, "datatype": Unsigned, "mutable": False},
		"CovNotificationMode": {"obj_id": 1360, "datatype": Enumerated, "mutable": False},
		"NetInErrorCount": {"obj_id": 1362, "datatype": Unsigned, "mutable": False},
		"NetOutErrorCount": {"obj_id": 1363, "datatype": Unsigned, "mutable": False},
		"TimeChangeLogDeadband": {"obj_id": 1384, "datatype": Unsigned, "mutable": False},
		# End of list of proprietary properties for the Device object
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
#bacnet.registered_devices

#print(device1.points)

# How do you specify proprietary properties?
# Read property multiple, data (depends on # of objects defined on the device)
_rpm = {'address': '192.168.20.4:47345',
        'objects': {
            'device:1000': ['@prop_1113', '@prop_2048', '@prop_1120', '@prop_1042', '@prop_1041', '@prop_2067', '@prop_2068', '@prop_1033', '@prop_1103', '@prop_1155', '@prop_1156', '@prop_1095', '@prop_1236', '@prop_1117', '@prop_1105', '@prop_1377', '@prop_1104', '@prop_1106', '@prop_1086', '@prop_1107', '@prop_1176', '@prop_1168', '@prop_1169', '@prop_1108', '@prop_1109', '@prop_2070', '@prop_2056', '@prop_2071', '@prop_1044', '@prop_1045', '@prop_1029', '@prop_1136', '@prop_1215', '@prop_1216', '@prop_1360', '@prop_1362', '@prop_1363', '@prop_1384'],
            'device:1000': ['all'],
            }
        }

_rp2 = {'address': '192.168.20.4:47345',
        'objects': {
            'analogValue:1': ['all'],
            'analogValue:2': ['all'],
            'analogValue:3': ['all'],
            'analogValue:4': ['all'],
            'analogValue:5': ['all'],
            'binaryValue:6': ['all'],
            'analogValue:7': ['all'],
            }
        }

_rp3 = {'address': '192.168.20.4:47345',
        'objects': {
            'program:1': ['all'],
            'program:2': ['all'],
            'program:3': ['all'],
            'program:4': ['all'],
            'program:5': ['all'],
            'program:6': ['all'],
            'program:7': ['all'],
            'program:8': ['all'],
            'program:9': ['all'],
            'program:10': ['all'],
            }
        }

_rp4 = {'address': '192.168.20.4:47345',
        'objects': {
            'trendLog:1': ['all'],
            'trendLog:2': ['all'],
            'trendLog:3': ['all'],
            'trendLog:4': ['all'],
            'trendLog:5': ['all'],
            'trendLog:6': ['all'],
            'trendLog:7': ['all'],
            'trendLog:8': ['all'],
            'trendLog:9': ['all'],
            'trendLog:10': ['all'],
            'trendLog:11': ['all'],
            'trendLog:12': ['all'],
            'trendLog:13': ['all'],
            }
        }

_rp5 = {'address': '192.168.20.4:47345',
        'objects': {
            'loop:1': ['all'],
            'loop:2': ['all'],
            'loop:3': ['all'],
            'loop:4': ['all'],
            'loop:5': ['all'],
            'loop:6': ['all'],
            'loop:7': ['all'],
            'loop:8': ['all'],
            'loop:9': ['all'],
            'loop:10': ['all'],
            }
        }

# Main loop: repeatedly send a readMultiple request:

i = 0
#while ( True ):
print('test #', i)
i = i + 1
bacnet.readMultiple(device1, request_dict=_rp2, vendor_id=35)
bacnet.readMultiple(device1, request_dict=_rp3, vendor_id=35)
bacnet.readMultiple(device1, request_dict=_rp4, vendor_id=35)
bacnet.readMultiple(device1, request_dict=_rp5, vendor_id=35)
bacnet.readMultiple(device1, request_dict=_rpm, vendor_id=35)
# time.sleep(1) # Optional throttling in # seconds

# Future enhancement: compare received dict with previous, see if there's any differences.
# https://bac0.readthedocs.io/en/latest/read.html
# https://bac0.readthedocs.io/en/latest/histories.html # Histories shows historical data

# Future enhancement 2: write values to all writable properties, read back, see if the writes worked.