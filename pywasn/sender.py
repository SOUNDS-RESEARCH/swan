"""
This file contains the MicrophoneSender class,
which defines a server socket which accepts connections
from other computers and sends them the audio signals recorded by it.
""" 

import argparse
import pyaudio
import socket

from settings import (
    FORMAT, CHANNELS, RATE, CHUNK, PORT,
    SOCKET_ADDRESS_FAMILY, SOCKET_KIND
)


class MicrophoneSender:
    def __init__(self, address=None):
        # Initialize network
        self.server_socket = socket.socket(SOCKET_ADDRESS_FAMILY, SOCKET_KIND)
        if not address:
            hostname = socket.gethostname()
            address = socket.gethostbyname(hostname)

        self.server_socket.bind((address, PORT))
        self.server_socket.listen()
        #self.read_list = [self.server_socket]
        self.client_sockets = []

        # Initialize microphone
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=FORMAT,
                                      channels=CHANNELS,
                                      rate=RATE,
                                      input=True,
                                      frames_per_buffer=CHUNK,
                                      stream_callback=self.send_new_audio_frame_to_clients)

        print("Recording...")
    
    def add_client(self):
        
        # I think the following function blocks the entire code until a message is received
        client_socket, address = self.server_socket.accept()
        print("Connected to", address)
        self.client_sockets.append(client_socket)
        
    def send_new_audio_frame_to_clients(self, in_data, frame_count, time_info, status):
        """This function is called every time a new audio frame is received.
           It proceeds to send the frame to all clients connected to this node
        """

        for client in self.client_sockets: 
            client.send(in_data)
        return (None, pyaudio.paContinue)
    
    def close(self):
        self.server_socket.close()

        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

        print("Finished recording")


def main(address):
    microphone_sender = MicrophoneSender(address)

    try:
        while True:
            microphone_sender.add_client()

    except KeyboardInterrupt:
        pass

    microphone_sender.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Create server which sends microphone signals to a remote computer")
    parser.add_argument("--address", type=str, help="Address of this server. Defaults to the machine's IP address")
    args = parser.parse_args()

    main(args.address)
