import platform

import socket


def get_local_ip():
    system = platform.system()

    if system == "Windows":
        return socket.gethostbyname(socket.gethostname())
    else:
        return socket.gethostbyname_ex(socket.getfqdn())[2][0]
