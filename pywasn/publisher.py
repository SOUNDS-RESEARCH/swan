import pickle
from omegaconf.dictconfig import DictConfig
import pyaudio
import paho.mqtt.client as mqtt
import time

from pywasn.utils.audio import create_audio_recorder
from pywasn.utils.network import get_local_ip


def publisher(config: DictConfig):
    broker_address = config["network"]["mqtt_broker_address"]
    client = mqtt.Client()

    client.connect(broker_address,
                   config["network"]["mqtt_broker_port"],
                   config["network"]["mqtt_broker_keepalive_in_secs"])
    
    print(f"Publishing microphone signals at {broker_address}...")

    def publish(in_data, frame_count, time_info, status):
        """This function is called every time a new audio frame is received.
           It proceeds to send the frame to all clients connected to this node
        """
        payload = {
            "data": in_data,
            "timestamp": time.time(),
            "sender_ip": get_local_ip()
        }

        client.publish(
            config["network"]["topic"],
            pickle.dumps(payload)
        )

        return (None, pyaudio.paContinue)

    create_audio_recorder(publish, config["audio"])
    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("Stopping publisher...")
