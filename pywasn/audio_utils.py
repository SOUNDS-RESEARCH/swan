import wave

import pyaudio

from pywasn.settings import CHANNELS, RATE, SAMPLE_SIZE_IN_BYTES, FORMAT, CHUNK


def frames_to_wav(frames, output_file_path):
    
    wf = wave.open(output_file_path, mode="wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(SAMPLE_SIZE_IN_BYTES)
    wf.setframerate(RATE)

    wf.writeframes(b''.join(frames))
    wf.close()


def create_audio_recorder(stream_callback):
    recorder = pyaudio.PyAudio()
    recorder.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
        stream_callback=stream_callback
    )

    return recorder