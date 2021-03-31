from datetime import datetime
import json
import os

import boto3
from phue import Bridge

SQS_QUEUE='Sydney-summit'

def lambda_handler(event, context):
    print(f'event: {event}')
    # load the side-loaded Amazon Location Service model; needed during Public Preview
    os.environ["AWS_DATA_PATH"] = os.environ["LAMBDA_TASK_ROOT"]

    sqs = boto3.resource('sqs',region_name='ap-northeast-1')

    # Get the queue
    queue = sqs.get_queue_by_name(QueueName=SQS_QUEUE)

    queue_length = len(queue.receive_messages())
    print(f'queue_length: {queue_length}')
    # Process messages by printing out body and optional author name
    for message in queue.receive_messages():
        # Print out the body
        response = message.body
        # print(f'Hello, {response}')
        dict_type = json.loads(response)
        # print(f'dict_type, {dict_type}')
        event_type = dict_type['detail']['EventType']
        print(f'event_type, {event_type}')


        b = Bridge('<enter ip address here>',"<enter username token from philips hue bridge here>")
        b.connect()
        # If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
        # Saves your bridge and its info to the variable 'b'
        # Attempts a connection, if this is your first time using this
        # on a hue configuration you will be prompted to press the link
        # button on your hue bridge.
        # print(b.get_api())
        # This will return a huge dump of all the states of your hue lights.
        # If this happens your hue is connected properly and you can remove
        # this line of code.
        offGroupLightState = {'transitiontime' : 2, 'on': False}
        onGroupLightState = {'bri': 240, 'sat': 0, 'transitiontime' : 2, 'on': True}
        if event_type == 'ENTER':
            print('turning lights on!')
            b.set_group('Living', onGroupLightState)
        elif event_type == 'EXIT':
            print('turning lights off!')
            b.set_group('Living', offGroupLightState)
        else:
            print('nothing to do here!')

        # Let the queue know that the message is processed
        message.delete()
        return {
            "statusCode": 200,
            "body": json.dumps(event_type)
        }