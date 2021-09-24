"""
This file defines the MicrophoneReceiver class, which is able to connect to a 
remote computer using a socket and play the signals coming from it.
"""

import argparse
import pyaudio
import socket

from settings import (
    FORMAT, CHANNELS, RATE, CHUNK, PORT,
    SOCKET_ADDRESS_FAMILY, SOCKET_KIND
)


class MicrophoneReceiver:
    def __init__(self, sender_address=None):
        # Initialize network
        if not sender_address:
            hostname = socket.gethostname()
            sender_address = socket.gethostbyname(hostname)
        self.receiver_socket = socket.socket(SOCKET_ADDRESS_FAMILY, SOCKET_KIND)
        self.receiver_socket.connect((sender_address, int(PORT)))
        
        # Initialize audio (optional, for playback)
        self.audio = pyaudio.PyAudio()
        self.playback_stream = self.audio.open(format=FORMAT,
                                      channels=CHANNELS,
                                      rate=RATE,
                                      output=True,
                                      frames_per_buffer=CHUNK)

    def receive(self):
        data = self.receiver_socket.recv(CHUNK)
        self.callback(data)

    def callback(self, data):
        "Edit this function to your needs. Currently plays received audio"
        self.playback_stream.write(data)

    def close(self):     
        print('Shutting down')
        self.receiver_socket.close()
        self.playback_stream.close()
        self.audio.terminate()


def main(sender_address):
    microphone_receiver = MicrophoneReceiver(sender_address)

    while True:
        microphone_receiver.receive()


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Create client which receives microphone signals from a remote computer")
    parser.add_argument("--sender_address", type=str)
    args = parser.parse_args()

    main(args.sender_address)
