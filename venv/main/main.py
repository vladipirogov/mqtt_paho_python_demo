# Simple MQTT Client publishing example
import datetime
import os
import time
import paho.mqtt.client as mqtt
import ssl
import logging
import uuid

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

project_id = 'mqtt_demo_cliend'
cloud_region = 'ua'
registry_id = 'registry_id'
device_id = 'device_id'
mqtt_hostname = '127.0.0.1'
mqtt_port = 8883
ca_certs_file = 'C:/mosquitto/certs/ca.crt'
cert_file = 'C:/mosquitto/certs/client.crt'
key_file = 'C:/mosquitto/certs/client.key'


# Typical MQTT callbacks
def error_str(rc):
    return '{}: {}'.format(rc, mqtt.error_string(rc))

def on_connect(client, userdata, flags, rc):
    print('on_connect', mqtt.connack_string(rc))
    client.subscribe([("/devices/#", 0), ("/command/topic", 2)])

def on_disconnect(client, userdata, rc):
    print('on_disconnect', error_str(rc))

def on_publish(client, userdata, mid):
    print('on_publish')

def on_message(client, userdata, message):
    print("Received message '" + str(message.payload) + "' on topic '"
        + message.topic + "' with QoS " + str(message.qos))

def main():
    # Publish to the events or state topic based on the flag.
    sub_topic = 'events'
    mqtt_topic = '/devices/{}/{}'.format(device_id, sub_topic)
    lwm = "Device gone Offline"  # Last will message

    client = mqtt.Client(
        client_id=str(uuid.uuid1()), clean_session=False)

    # Enable SSL/TLS support.
    client.tls_set(cert_reqs=ssl.CERT_NONE)

    # callback unused in this example:
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.will_set(mqtt_topic,lwm, qos=1,retain=False)
    client.enable_logger(logger)

    # Connect to the Google pub/sub
    client.connect(mqtt_hostname, mqtt_port, keepalive=60)

    # Publish num_messages mesages to the MQTT bridge once per second.
    for i in range(1, 3):
        payload = 'Hello World!: {}'.format(i)
        print('Publishing message\'{}\''.format(payload))
        client.publish(mqtt_topic, payload, qos=0, retain=True)
        time.sleep(1)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    client.loop_forever()

    client.disconnect()

if __name__ == '__main__':
    main()
