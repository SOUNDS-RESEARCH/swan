import argparse
import asyncio
import wave

import pyaudio

from socket_utils import get_ip
from settings import PORT, CHUNK, FORMAT, CHANNELS, RATE


async def client(server_address, port=PORT, output_file_path="output.wav"):
    if server_address is None:
        server_address = get_ip()

    reader, writer = await asyncio.open_connection(
        server_address, port)
    print(f"Connected to {server_address} on port {port}")

    audio = pyaudio.PyAudio()
    player = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        output=True,
                        frames_per_buffer=CHUNK)


    wf = wave.open(output_file_path, mode="wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)

    frames = []
    while True:
        try:
            data = await reader.read(CHUNK)
            print("playing...")
            #player.write(data)
            frames.append(data)
        except KeyboardInterrupt:
            wf.writeframes(b''.join(frames))
            wf.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Create client which sends microphone signals to a remote computer"
    )
    parser.add_argument(
                "--hostname",
                type=str,
                help="Address of the remote server. Defaults to the machine's IP address"
    )
    args = parser.parse_args()

    asyncio.run(client(args.hostname))
