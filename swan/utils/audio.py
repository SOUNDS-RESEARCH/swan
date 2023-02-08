import numpy as np
import pyaudio
import wave

from numpy_ringbuffer import RingBuffer

FORMAT = pyaudio.paInt16


class AudioBuffer:
    def __init__(self, buffer_size):
        self.buffer_size = buffer_size

        self.ring_buffers = {}

    def write(self, data):
        device_name = data["device_name"]
        
        # Create an empty buffer for the publisher
        if device_name not in self.ring_buffers:
            self.ring_buffers[device_name] = RingBuffer(capacity=self.buffer_size,
                                                      dtype=np.int16)
            self.ring_buffers[device_name].extend(np.zeros(self.buffer_size, dtype=np.int16))
        
        self.ring_buffers[device_name].extend(np.frombuffer(data["frame"], dtype=np.int16))
    
    def read(self):
        frames = {
            device_name: np.array(buffer)
            for device_name, buffer in self.ring_buffers.items()
        }
        return frames


def frames_to_wav(frames, audio_config, output_file_path):
    wf = wave.open(output_file_path, mode="wb")
    wf.setnchannels(audio_config["channels"])
    wf.setsampwidth(audio_config["sample_size_in_bytes"])
    wf.setframerate(audio_config["sr"])

    wf.writeframes(b''.join(frames))
    wf.close()


def create_audio_recorder(stream_callback, audio_config):
    recorder = pyaudio.PyAudio()
    
    if audio_config["sample_size_in_bytes"] != 2:
        raise NotImplementedError("The only currently available sample size is 2")

    recorder.open(
        format=FORMAT,
        channels=audio_config["channels"],
        rate=audio_config["sr"],
        input_device_index=audio_config["device_id"],
        input=True,
        frames_per_buffer=audio_config["frame_size_in_bytes"],
        stream_callback=stream_callback
    )

    return recorder

def get_audio_devices():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')

    for i in range(0, numdevices):
        dev_input_channels = p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')
        if (dev_input_channels) > 0:
            print("Input Device id :", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'), " - ", dev_input_channels, " channel(s)")
