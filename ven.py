import asyncio
from datetime import timedelta
from openleadr import OpenADRClient, enable_default_logging

enable_default_logging()

async def collect_report_value():
    # This callback is called when you need to collect a value for your Report
    return 1.23

async def handle_event(event):
    # This callback receives an Event dict.
    # You should include code here that sends control signals to your resources.
    return 'optIn'

# Create the client object
client = OpenADRClient(ven_name='ven_123',
                       vtn_url='https://192.168.17.186:8080/OpenADR2/Simple',
                       debug=1,
                       ven_id='TH_VEN',
                       #cert='C:/Temp/dummy_ven.crt',
                       #key='C:/Temp/dummy_ven.key',
                       cert='C:/Temp/ven-ecc-testcert.pem',
                       key='C:/Temp/ven-ecc-testkey.der.pem',
                       #cert='C:/Temp/cert-ecc.pem',
                       #key='C:/Temp/private-key.pem',
                       #passphrase='openadr',
                       vtn_fingerprint='57:5D:9F:C8:EA:06:C6:52:3C:02')

# Add the report capability to the client
client.add_report(callback=collect_report_value,
                  resource_id='device001',
                  measurement='voltage',
                  sampling_rate=timedelta(seconds=10))

# Add event handling capability to the client
client.add_handler('on_event', handle_event)

# Run the client in the Python AsyncIO Event Loop
loop = asyncio.get_event_loop()
loop.create_task(client.run())
loop.run_forever()