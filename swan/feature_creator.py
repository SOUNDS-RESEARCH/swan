import numpy as np

from scipy.signal import csd


from swan.utils.audio import AudioBuffer


class FeatureCreator:
    def __init__(self, buffer_size):
        self.buffer = AudioBuffer(buffer_size)

    def update_features(self, received_data):
        self.buffer.write(received_data)

        signals = self.buffer.read()

        features_per_publisher = {}
        for publisher_ip, signal in signals.items():
            signal = np.stack((signal[::2], signal[1::2]), axis=0)
            # Pyaudio sends channels interleaved.
            # When working with 2 channels, we must separate them.
            # See https://stackoverflow.com/questions/24974032/reading-realtime-audio-data-into-numpy-array

            features = {}
            features["num_channels"] = signal.shape
            features["msc"] = msc(signal)
            
            features_per_publisher[publisher_ip] = features
        
        return features_per_publisher


def msc(x):
    """
    Compute the Magnitude Square Coherence feature, defined as:

          |CSD(x1, x2)(f)|^2
    ------------------------------
    CSD(x1, x1)(f)*CSD(x2, x2)(f)'

    Where CSD(x1, x2) is the cross spectral density between signals x1 and x2.

    """

    f12, csd12 = csd(x[0], x[1])
    f11, csd11 = csd(x[0], x[0])
    f22, csd22 = csd(x[1], x[1])

    numerator = csd12*csd12.conj()
    denominator = csd11*csd22.conj()

    msc_values = (numerator/denominator).real
    return msc_values.mean()
