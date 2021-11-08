import wave

import pyaudio


def frames_to_wav(frames, audio_config, output_file_path):
    
    wf = wave.open(output_file_path, mode="wb")
    wf.setnchannels(audio_config["channels"])
    wf.setsampwidth(audio_config["sample_size_in_bytes"])
    wf.setframerate(audio_config["rate"])

    wf.writeframes(b''.join(frames))
    wf.close()


def create_audio_recorder(stream_callback, audio_config):
    recorder = pyaudio.PyAudio()
    
    format = pyaudio.paInt16
    if audio_config["sample_size_in_bytes"] != 2:
        raise NotImplementedError("The only currently available sample size is 2")

    recorder.open(
        format=format,
        channels=audio_config["channels"],
        rate=audio_config["rate"],
        input=True,
        frames_per_buffer=audio_config["chunk"],
        stream_callback=stream_callback
    )

    return recorder