import paho.mqtt.client as mqtt
import pickle

from pywasn.database import Database
from pywasn.settings import (
    MQTT_BROKER_ADDRESS, MQTT_BROKER_PORT, MQTT_BROKER_KEEPALIVE_IN_SECS,
    WAV_FILENAME
)
from pywasn.settings import TOPIC


def subscriber(): 
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe(TOPIC)

    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):

        # Write message to "database" -- it could be an sqlite database for example.
        payload = pickle.loads(msg.payload)

        database.insert(payload["data"], payload["timestamp"], payload["sender_ip"])
        print(msg.topic, payload["timestamp"])


    database = Database()
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER_ADDRESS,
                   MQTT_BROKER_PORT,
                   MQTT_BROKER_KEEPALIVE_IN_SECS)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("Stopping subscriber...")
        database.to_wav(WAV_FILENAME)
