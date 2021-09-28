import argparse
import asyncio

import pyaudio

from settings import PORT,FORMAT, CHANNELS, RATE, CHUNK
from socket_utils import get_ip


async def handle_client(reader, writer):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
    # player = audio.open(format=FORMAT,
    #                             channels=CHANNELS,
    #                             rate=RATE,
    #                             output=True,
    #                             frames_per_buffer=CHUNK)

    while True:
        data = stream.read(CHUNK)
        writer.write(data)
        await writer.drain()
        #player.write(data)
        
    # print("Close the connection")
    # writer.close()

async def main(server_address, port=PORT):
    if server_address is None:
        server_address = get_ip()

    server = await asyncio.start_server(
        handle_client, server_address, port)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {server_address}, port {port}')

    async with server:
        await server.serve_forever()

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

    asyncio.run(main(args.hostname))