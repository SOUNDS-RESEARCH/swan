from multiprocessing import Process

from omegaconf.dictconfig import DictConfig

from pywasn.subscriber import subscriber
from pywasn.publisher import publisher

def client(config: DictConfig):
    try:
        subscriber_process = Process(target=subscriber, args=(config,))
        publisher_process = Process(target=publisher, args=(config,))

        subscriber_process.start()
        publisher_process.start()

        subscriber_process.join()
        publisher_process.join()
    except KeyboardInterrupt:
        print("Stopping client...")

if __name__ == "__main__":
    client()
