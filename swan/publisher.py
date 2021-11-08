import pickle
import pyaudio
import paho.mqtt.client as mqtt
import time

from omegaconf.dictconfig import DictConfig

from swan.utils.audio import create_audio_recorder
from swan.utils.network import get_local_ip


def publisher(config: DictConfig):
    broker_address = config["network"]["broker_address"]
    client = mqtt.Client()

    client.connect(broker_address,
                   config["network"]["broker_port"],
                   config["network"]["broker_keepalive_in_secs"])
    
    print(f"Publishing microphone signals at {broker_address}...")

    def publish(in_data, frame_count, time_info, status):
        """This function is called every time a new audio frame is received.
           It proceeds to send the frame to all clients connected to this node
        """
        payload = {
            "data": in_data,
            "timestamp": time.time(),
            "publisher_ip": get_local_ip()
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
