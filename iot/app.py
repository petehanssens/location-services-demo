from datetime import datetime
import json
import os

import boto3

# Update this to match the name of your Tracker resource
TRACKER_NAME = "my-mobile"

"""
This Lambda function receives a payload from AWS IoT Core and publishes device updates to Amazon Location Service via the BatchUpdateDevicePosition API.

Parameter 'event' is the payload delivered from AWS IoT Core.

In this sample, we assume that the payload has a single top-level key 'payload' and a nested key
'location' with keys 'lat' and 'long'. We also assume that the name of the device is nested in
the payload as 'deviceid'. Finally, the timestamp of the payload is present as 'timestamp'. For
example:

>>> event
{ 'payload': { 'deviceid': 'thing123', 'timestamp': 1604940328,
  'location': { 'lat': 49.2819, 'long': -123.1187 } } }

If your data does not match this schema, you can either use the AWS IoT Core rules engine to
format the data before delivering it to this Lambda function, or you can modify the code below to
match it.
"""
def lambda_handler(event, context):
    print(f'event: {event}')
    # load the side-loaded Amazon Location Service model; needed during Public Preview
    os.environ["AWS_DATA_PATH"] = os.environ["LAMBDA_TASK_ROOT"]

    updates = [
        {
        "DeviceId": TRACKER_NAME,
        "SampleTime": datetime.fromtimestamp(event["tst"]).isoformat(),
        "Position": [
            event["lon"],
            event["lat"]
        ]
        }
    ]

    client = boto3.client("location")
    response = client.batch_update_device_position(TrackerName=TRACKER_NAME, Updates=updates)

    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }