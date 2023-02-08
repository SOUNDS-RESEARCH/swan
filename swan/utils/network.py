import platform

import socket

def get_local_ip():
    system = platform.system()

    if system == "Windows":
        return socket.gethostbyname(socket.gethostname())
    else:
        return socket.gethostbyname(socket.gethostname())

def get_network_ip(broker_address):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((broker_address, 1883))
    return s.getsockname()[0]