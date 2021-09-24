import pyaudio
import socket

from settings import (
    FORMAT, CHANNELS, RATE, CHUNK, PORT, ADDRESS,
    SOCKET_ADDRESS_FAMILY, SOCKET_KIND
)


class MicrophoneReceiver:
    def __init__(self):
        # Initialize network
        self.receiver_socket = socket.socket(SOCKET_ADDRESS_FAMILY, SOCKET_KIND)
        self.receiver_socket.connect((ADDRESS, int(PORT)))
        
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


def main():

    microphone_receiver = MicrophoneReceiver()

    try:
        while True:
            microphone_receiver.receive()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
