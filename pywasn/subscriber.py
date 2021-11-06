from omegaconf.dictconfig import DictConfig
import paho.mqtt.client as mqtt
import pickle

from pywasn.database import Database


def subscriber(config: DictConfig): 
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe(config["network"]["topic"])

    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):

        # Write message to "database" -- it could be an sqlite database for example.
        payload = pickle.loads(msg.payload)

        database.insert(payload["data"], payload["timestamp"], payload["sender_ip"])
        print(msg.topic, payload["timestamp"])


    database = Database(config)
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(config["network"]["mqtt_broker_address"],
                   config["network"]["mqtt_broker_port"],
                   config["network"]["mqtt_broker_keepalive_in_secs"])

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("Stopping subscriber...")
        database.to_wav(config["audio"]["wav_filename"])
