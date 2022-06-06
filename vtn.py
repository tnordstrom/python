import asyncio
from datetime import datetime, timezone, timedelta
from openleadr import OpenADRServer, enable_default_logging
from functools import partial
import logging

enable_default_logging(level=logging.DEBUG)

async def on_create_party_registration(registration_info):
    """
    Inspect the registration info and return a ven_id and registration_id.
    """
    if registration_info['ven_name'] == 'ven_123':
        ven_id = 'TH_VEN'
        registration_id = 'reg_id_123'
        print("VEN registered ok!")
        return ven_id, registration_id
    else:
        print(f"VEN did not register {registration_info['ven_name']} ")
        return False

async def on_register_report(ven_id, resource_id, measurement, unit, scale,
                             min_sampling_interval, max_sampling_interval):
    """
    Inspect a report offering from the VEN and return a callback and sampling interval for receiving the reports.
    """
    print("On register report called!")
    callback = partial(on_update_report, ven_id=ven_id, resource_id=resource_id, measurement=measurement)
    sampling_interval = min_sampling_interval
    return callback, sampling_interval

async def on_update_report(data, ven_id, resource_id, measurement):
    """
    Callback that receives report data from the VEN and handles it.
    """
    print("On update report called!")
    for time, value in data:
        print(f"Ven {ven_id} reported {measurement} = {value} at time {time} for resource {resource_id}")

async def event_response_callback(ven_id, event_id, opt_type):
    """
    Callback that receives the response from a VEN to an Event.
    """
    print(f"VEN {ven_id} responded to Event {event_id} with: {opt_type}")

def ven_lookup(ven_id):
    # Look up the information about this VEN.
    ven_info = database.lookup('vens').where(ven_id=ven_id) # Pseudo code
    if ven_info:
        return {'ven_id': ven_info['ven_id'],
                'ven_name': ven_info['ven_name'],
                'fingerprint': ven_info['fingerprint'],
                'registration_id': ven_info['registration_id']}
    else:
        return {}
                                

# Create the server object
server = OpenADRServer( vtn_id='TH_VTN',
                        http_host='192.168.17.186',
                        http_path_prefix='/OpenADR2/Simple',
                        #cert='C:/Temp/dummy_vtn.crt',
                        #key='C:/Temp/dummy_vtn.key',
                        cert='C:/Temp/vtn-root-cert.pem',
                        key='C:/Temp/ven-ecc-testkey.der.key',
                        #cert='C:/Temp/cert-ecc.pem',
                        #key='C:/Temp/private-key.pem',
                        #passphrase='openadr',
                        #http_cert='C:/Temp/dummy_ca.crt',
                        #http_key='C:/Temp/dummy_ca.key',
                        #http_key_passphrase='openadr',
                        requested_poll_freq=timedelta(seconds=5),
                        fingerprint_lookup=ven_lookup)
"""
server = OpenADRServer( vtn_id='TH_VTN',
                        http_host='192.168.17.186',
                        http_path_prefix='/OpenADR2/Simple')
"""

# Add the handler for client (VEN) registrations
server.add_handler('on_create_party_registration', on_create_party_registration)

# Add the handler for report registrations from the VEN
server.add_handler('on_register_report', on_register_report)

server.add_handler('on_update_report', on_update_report)

# Add a prepared event for a VEN that will be picked up when it polls for new messages.
server.add_event(ven_id='TH_VEN',
                 signal_name='simple',
                 signal_type='level',
                 intervals=[{'dtstart': datetime(2021, 12, 6, 11, 0, 4, tzinfo=timezone.utc),
                             'duration': timedelta(minutes=10),
                             'signal_payload': 1}],
                 callback=event_response_callback)

# Run the server on the asyncio event loop
loop = asyncio.get_event_loop()
loop.create_task(server.run())
loop.run_forever()