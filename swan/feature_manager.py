import numpy as np

from omegaconf.dictconfig import DictConfig
from scipy.signal import csd

from swan.utils.audio import AudioBuffer
from swan.utils.silero_vad import SileroVAD

EPS = 1e-7

class FeatureManager:
    """Each subscriber has a FeatureManager, which is a class responsible for
    processing the audio signals into features.

    In turn, a feature manager has an AudioBuffer so that features can be computed with
    more than a single audio frame.
    """

    def __init__(self, config: DictConfig):
        self.buffer = AudioBuffer(
            config["audio"]["feature_buffer_size_in_bytes"])

        self.vad = SileroVAD(sr=config["audio"]["sr"])
        self.noise_floor = float()
        self.vad_thr = config["vad"]["vad_decision_threshold"]

    def update(self, received_data: dict) -> dict:
        """This function is called by the subscriber every time
        new data is received, triggering the recomputation of the features.

        Args:
            received_data (dict): dictionary where keys are IP addresses and values
            are audio signals in binary format.

        Returns:
            dict: dictionary where the key is the publisher's IP address
                  and the values are a secondary dict with the name of the feature
                  and it's corresponding value.
        """

        # 1. Add data to the end of the buffer
        self.buffer.write(received_data)

        # 2. Read the entire buffer
        signals = self.buffer.read()

        features_per_publisher = {}

        # Compute features for all received signals
        for device_name, signal in signals.items():
            
            # signal = np.stack((signal[::2], signal[1::2]), axis=0)
            # Pyaudio sends channels interleaved.
            # When working with 2 channels, we must separate them.
            # See https://stackoverflow.com/questions/24974032/reading-realtime-audio-data-into-numpy-array

            features = {}
            #features["num_channels"] = signal.shape
            # features["msc"] = msc(signal)
            features["vad"] = self.vad.get_speech_probability_for_frame(signal)
            features["rms"] = rms(signal)
            self.noise_floor, features["snr"] = snr(signal, features["vad"], self.vad_thr, self.noise_floor)
            features["noise_floor"] = self.noise_floor
            features_per_publisher[device_name] = features
        
        return features_per_publisher


def msc(x):
    """
    Compute the (Mean) Magnitude Square Coherence feature, defined as:

         |CSD(x1, x2)(f)|^2
    ------------------------------
    CSD(x1, x1)(f)*CSD(x2, x2)(f)'

    Averaged across all frequencies, where CSD(x1, x2) is the cross spectral density between signals x1 and x2.

    """

    # Only use the last frame of data
    N_SAMPLES_TO_USE = 4096
    x = x[-N_SAMPLES_TO_USE:]  

    f12, csd12 = csd(x[0], x[1])
    f11, csd11 = csd(x[0], x[0])
    f22, csd22 = csd(x[1], x[1])

    numerator = csd12*csd12.conj()
    denominator = csd11*csd22.conj()

    msc_values = (numerator/(denominator + EPS)).real
    return msc_values.mean()


def rms(x):
    """
    Compute the Root Mean Square, defined as:

    """
    # Only use the last frame of data
    N_SAMPLES_TO_USE = 4096
    x = x[-N_SAMPLES_TO_USE:].astype(np.float32)/32767.0

    return np.sqrt(np.square(x).sum())

def snr(x, vad_scores, thr, n_floor):
    """
    Compute the Root Mean Square, defined as:

    """
    # Only use the last frame of data
    N_SAMPLES_TO_USE = 4096

    def energy():
        return np.square(x[-N_SAMPLES_TO_USE:].astype(np.float32)/32767.0).sum()
    def update_nf():
        return (n_floor + energy()) / 2

    # Select unvoiced frames and update the noise floor
    if vad_scores < thr: n_floor = update_nf()

    # Compute SNR
    en = energy()
    # print("n_floor:{} --- en:{}\n".format(n_floor,en))

    return n_floor, 10*np.log10(en/n_floor)