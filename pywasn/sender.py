import pyaudio
import socket
import select

from settings import (
    FORMAT, CHANNELS, RATE, CHUNK, ADDRESS, PORT,
    SOCKET_ADDRESS_FAMILY, SOCKET_KIND
)


class MicrophoneSender:
    def __init__(self):

        # Initialize network
        self.server_socket = socket.socket(SOCKET_ADDRESS_FAMILY, SOCKET_KIND)
        self.server_socket.bind((ADDRESS, PORT))
        self.server_socket.listen(5)
        self.read_list = [self.server_socket]

        # Initialize microphone
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=FORMAT,
                                      channels=CHANNELS,
                                      rate=RATE,
                                      input=True,
                                      frames_per_buffer=CHUNK,
                                      stream_callback=self.callback)
        
        print("Recording...")
    
    def listen_and_send(self):
        readable, writable, errored = select.select(self.read_list, [], [])
        for s in readable:
            if s is self.server_socket:
                (clientsocket, address) = self.server_socket.accept()
                self.read_list.append(clientsocket)
                print("Connection from", address)
            else:
                data = s.recv(1024)
                if not data:
                    self.read_list.remove(s)
        
    def callback(self, in_data, frame_count, time_info, status):
        for s in self.read_list[1:]:
            s.send(in_data)
        return (None, pyaudio.paContinue)
    
    def close(self):
        
        self.server_socket.close()
        # stop Recording
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

        print("Finished recording")


def main():
    microphone_sender = MicrophoneSender()

    try:
        while True:
            microphone_sender.listen_and_send()

    except KeyboardInterrupt:
        pass

    microphone_sender.close()

if __name__ == "__main__":
    main()
