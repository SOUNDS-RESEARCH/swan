import hydra

from multiprocessing import Process
from omegaconf.dictconfig import DictConfig

from swan.subscriber import Subscriber
from swan.publisher import Publisher


class Client:
    """This class abstracts the main functionality performed by a device.
        A device can be a 'publisher', a 'subscriber' or both. A publisher sends their
        recorded microphone signals to a Mosquitto (MQTT) server, which in turn sends it to
        all 'subscriber' devices.

        Besides receiving the microphone signals additional functionality
        of subscribers consist of computing features based on the received signals and
        plotting them.
    """

    def __init__(self, config: DictConfig):
        """Create a new client.

        Args:
            config (DictConfig): dictionary-like structure containg the client configuration,
            such as whether they are a publisher and/or subscriber, the address of the MQTT server, etc.
        """
        
        try:

            processes = []
            if config["subscribe"]:
                processes.append(Process(target=Publisher, args=(config,)))
            if config["publish"]:
                processes.append(Process(target=Subscriber, args=(config,)))

            [p.start() for p in processes]
            [p.join() for p in processes]

        except KeyboardInterrupt:
            print("Stopping client...")


@hydra.main(config_path="config", config_name="config")
def main(config: DictConfig):
    Client(config)


if __name__ == "__main__":
    main()
