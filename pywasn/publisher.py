import pickle
from omegaconf.dictconfig import DictConfig
import pyaudio
import paho.mqtt.client as mqtt
import socket
import time

from pywasn.utils.audio import create_audio_recorder


def publisher(config: DictConfig):
    client = mqtt.Client()

    client.connect(config["network"]["mqtt_broker_address"],
                   config["network"]["mqtt_broker_port"],
                   config["network"]["mqtt_broker_keepalive_in_secs"])

    def publish(in_data, frame_count, time_info, status):
        """This function is called every time a new audio frame is received.
           It proceeds to send the frame to all clients connected to this node
        """
        payload = {
            "data": in_data,
            "timestamp": time.time(),
            "sender_ip": _get_local_ip()
        }

        client.publish(config["network"]["topic"], pickle.dumps(payload))

        return (None, pyaudio.paContinue)

    create_audio_recorder(publish, config["audio"])

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("Stopping publisher...")

def _get_local_ip():
    return socket.gethostbyname(socket.gethostname())