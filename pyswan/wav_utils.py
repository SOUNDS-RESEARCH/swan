import wave
import pyaudio

from settings import CHANNELS, FORMAT, RATE

def write(frames, output_file_name):
    wf = wave.open(output_file_name, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
