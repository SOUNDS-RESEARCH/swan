import pickle
import pyaudio
import paho.mqtt.client as mqtt
import socket
import time

from pywasn.audio_utils import create_audio_recorder
from pywasn.settings import (
    MQTT_BROKER_ADDRESS, MQTT_BROKER_KEEPALIVE_IN_SECS, MQTT_BROKER_PORT,
    TOPIC
)


def publisher():
    client = mqtt.Client()

    client.connect(MQTT_BROKER_ADDRESS,
                   MQTT_BROKER_PORT,
                   MQTT_BROKER_KEEPALIVE_IN_SECS)

    def publish(in_data, frame_count, time_info, status):
        """This function is called every time a new audio frame is received.
           It proceeds to send the frame to all clients connected to this node
        """
        payload = {
            "data": in_data,
            "timestamp": time.time(),
            "sender_ip": _get_local_ip()
        }

        client.publish(TOPIC, pickle.dumps(payload))

        return (None, pyaudio.paContinue)

    create_audio_recorder(publish)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("Stopping publisher...")

def _get_local_ip():
    return socket.gethostbyname(socket.gethostname())