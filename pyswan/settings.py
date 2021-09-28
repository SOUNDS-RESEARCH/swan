import pyaudio
import socket

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 4096
PORT = 4444

SOCKET_ADDRESS_FAMILY = socket.AF_INET # IPv4
SOCKET_KIND = socket.SOCK_STREAM # TCP
