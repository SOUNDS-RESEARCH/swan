import paho.mqtt.client as mqtt
import pickle
import pyaudio
import time

from omegaconf.dictconfig import DictConfig

from swan.utils.audio import create_audio_recorder
from swan.utils.network import get_ip_address


class Publisher:
    def __init__(self, config: DictConfig):
        """This function abstracts the functionality
        of a publisher. A publisher is connected to an
        MQTT server as well as to the device's microphones.
        
        Args:
            config (DictConfig): configuration of the publisher, such as the IP address of the MQTT
            server to use. 

        """

        self.config = config
        self.publisher_ip = get_ip_address(config["network"]["broker_address"])

        # 1. Connect to a MQTT server to publish signals at
        broker_address = config["network"]["broker_address"]
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect(broker_address,
                                 config["network"]["broker_port"],
                                 config["network"]["broker_keepalive_in_secs"])
        print(f"Publishing microphone signals at {broker_address}...")

        # 2. Create an audio recorder which calls the "publish" function
        # every time a frame is received
        create_audio_recorder(self.publish, config["audio"])

        # 3. Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        try:
            self.mqtt_client.loop_forever()
        except KeyboardInterrupt:
            print("Stopping publisher...")
            

    def publish(self, in_data, frame_count, time_info, status):
        """This function is called every time a new audio frame is received.
        It proceeds to send the frame to all clients connected to this node
        """
        payload = {
            "frame": in_data,
            "timestamp": time.time(),
            "publisher_ip": self.publisher_ip
        }

        self.mqtt_client.publish(
            self.config["network"]["topic"],
            pickle.dumps(payload)
        )

        return (None, pyaudio.paContinue)
