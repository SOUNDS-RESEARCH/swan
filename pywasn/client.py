from multiprocessing import Process

from omegaconf.dictconfig import DictConfig

from pywasn.subscriber import subscriber
from pywasn.publisher import publisher


def client(config: DictConfig):
    try:
        processes = []
        if config["is_publisher"]:
            processes.append(Process(target=subscriber, args=(config,)))
        if config["is_subscriber"]:
            processes.append(Process(target=publisher, args=(config,)))

        [p.start() for p in processes]
        [p.join() for p in processes]

    except KeyboardInterrupt:
        print("Stopping client...")

if __name__ == "__main__":
    client()
