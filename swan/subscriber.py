import paho.mqtt.client as mqtt
import pickle

from omegaconf.dictconfig import DictConfig

from swan.database import Database
from swan.feature_manager import FeatureManager
from swan.plotter import Plotter


class Subscriber:
    def __init__(self, config: DictConfig):
        """This function abstracts the functionality of a subscriber role.
        A subscriber listens to an MQTT server. Swan messages consist of a
        dictionary where the keys are the IP address of the sender and the values
        are the microphone signals.

        Once a message is received, features are computed from the signals (such as the
        Magnitude Squared Coherence). For more information, see feature_manager.py.

        A subscriber also keeps an interactive Matplotlib figure open, which is updated
        each time a new audio frame is received. See plotter.py for more info.

        Finally, the frames are saved into a relational database, so the recordings can be played later.

        Args:
            config (DictConfig): Subscriber configuration, such as the address of the MQTT server, etc.
        """
        self.config = config

        self.database = Database(config)
        self.feature_manager = FeatureManager(config)
        self.plotter = Plotter()

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        broker_address = config["network"]["broker_address"]
        self.client.connect(broker_address,
                    config["network"]["broker_port"],
                    config["network"]["broker_keepalive_in_secs"])
        print(f"Subscribed to receive microphone signals at {broker_address}...")
        
        # Blocking call that processes network traffic,
        # dispatches callbacks and handles reconnecting.
        try:
            self.client.loop_forever()
        except KeyboardInterrupt:
            print("Stopping subscriber...")
            # The commands below are not working...
            # self.database.to_wav()
            # stats = self.database.get_stats()
            # stats.to_csv(config["audio"]["stats_filename"])
            # print(stats)

    def on_connect(self, client, userdata, flags, rc):
        """The callback for when the client receives a CONNACK response from the server.
            Subscribing in on_connect() means that if we lose the connection and
            reconnect then subscriptions will be renewed."""
        
        client.subscribe(self.config["network"]["topic"])
    
    def on_message(self, client, userdata, msg):
        "The callback for when a PUBLISH message is received from the server."
        payload = pickle.loads(msg.payload)
        if payload["msg_type"] == "con":
            self.plotter.update_device_names(payload["connect"], payload["device_name"])
        if payload["msg_type"] == "data":
            features = self.feature_manager.update(payload)
            self.plotter.update(features)
            self.database.insert(payload["frame"], payload["timestamp"], payload["publisher_ip"])
