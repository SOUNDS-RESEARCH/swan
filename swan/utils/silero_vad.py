import numpy as np
import torch


class SileroVAD:
    def __init__(self, sr=16000):
        self.model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                            model='silero_vad',
                            force_reload=False,
                            onnx=False)

        (self.get_speech_timestamps,
        self.save_audio,
        self.read_audio,
        _,
        self.collect_chunks) = utils

        self.sr = sr

    def get_speech_probability_for_frame(self, frame, pcm=True):
        if isinstance(frame, np.ndarray):
            frame = torch.from_numpy(frame)
        
        if pcm:
            frame = frame.float() / 32768.0
        
        if len(frame.shape) == 2:
            # More than one channel, choose a single one
            frame = frame[0]

        speech_prob = self.model(frame, self.sr)
        return speech_prob.item()
