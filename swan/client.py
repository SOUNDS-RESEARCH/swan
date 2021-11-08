from multiprocessing import Process

from omegaconf.dictconfig import DictConfig

from swan.subscriber import subscriber
from swan.publisher import publisher


def client(config: DictConfig):
    try:
        processes = []
        if config["subscribe"]:
            processes.append(Process(target=subscriber, args=(config,)))
        if config["publish"]:
            processes.append(Process(target=publisher, args=(config,)))

        [p.start() for p in processes]
        [p.join() for p in processes]

    except KeyboardInterrupt:
        print("Stopping client...")

if __name__ == "__main__":
    client()
