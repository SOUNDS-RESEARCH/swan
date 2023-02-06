import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("TkAgg")


class Plotter:
    def __init__(self):
        self.feature_keys = ["rms"] # When adding new features, add their keys to this list

        # Currently only creating one plot, which
        # will hold the MSC.
        self.fig, self.axs = plt.subplots(nrows=len(self.feature_keys))

        plt.ion()
        plt.show()

    def update(self, features):
        """Function which updates the plotter once new audio
        data arrives.

        Args:
            features (dict): dictionary where the keys are IP addresses
            and the values are dicts with keys being the feature names and
            values being their respective feature values.
        """
        
        self._update_rms(features)
        # Add new features plotting functions here.
        # You may use the _update_rms function as a template.

        self.fig.canvas.draw()
        # This will run the GUI event
        # loop until all UI events
        # currently waiting have been processed
        self.fig.canvas.flush_events()

    def _update_rms(self, features):
        device_ips = sorted(list(features.keys()))
        # print(device_ips)
        rms = [
            features[device_ip]["rms"]
            for device_ip in device_ips
        ]
        
        self.axs.clear()
        self.axs.set_title("RMS of each device")
        self.axs.bar(device_ips, rms)
