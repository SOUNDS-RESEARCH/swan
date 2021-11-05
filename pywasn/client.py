from multiprocessing import Process

from pywasn.subscriber import subscriber
from pywasn.publisher import publisher

def client():
    try:
        subscriber_process = Process(target=subscriber, args=())
        publisher_process = Process(target=publisher, args=())

        subscriber_process.start()
        publisher_process.start()

        subscriber_process.join()
        publisher_process.join()
    except KeyboardInterrupt:
        print("Stopping client...")

if __name__ == "__main__":
    client()
