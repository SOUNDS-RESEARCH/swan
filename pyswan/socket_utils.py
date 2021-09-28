import socket

def get_ip():
    hostname = socket.gethostname()
    hostname = socket.gethostbyname(hostname)
    return hostname
