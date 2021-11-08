from omegaconf.dictconfig import DictConfig
import paho.mqtt.client as mqtt
import pickle

from pywasn.database import Database


def subscriber(config: DictConfig): 
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, rc):
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe(config["network"]["topic"])

    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        payload = pickle.loads(msg.payload)
        database.insert(payload["data"], payload["timestamp"], payload["publisher_ip"])
        

    database = Database(config)
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    broker_address = config["network"]["broker_address"]
    client.connect(broker_address,
                   config["network"]["broker_port"],
                   config["network"]["broker_keepalive_in_secs"])
    print(f"Subscribed to receive microphone signals at {broker_address}...")
    # Blocking call that processes network traffic,
    # dispatches callbacks and handles reconnecting.
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("Stopping subscriber...")
        database.to_wav()
        stats = database.get_stats()
        stats.to_csv(config["audio"]["stats_filename"])
        print(stats)
