import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("TkAgg")


class Plotter:
    device_ips: dict
    feature_data : dict
    def __init__(self):
        self.feature_keys = ["rms"] # When adding new features, add their keys to this list
        for feature_key in self.feature_keys:
            self.feature_data[feature_key] = {}
        # Currently only creating one plot, which
        # will hold the MSC.
        self.fig, self.axs = plt.subplots(nrows=len(self.feature_keys))
        self.axs.set_title("RMS of each device")

        plt.ion()
        plt.show()

    def update_data(self, features):
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
        if len(self.feature_keys) == 1:
            self.axs.clear()
            self.axs.bar(self.device_ips, self.feature_data[feature_key].values())
        else:
            for id, feature_key in enumerate(self.feature_keys):
                self.axs[id].clear()
                self.axs[id].bar(self.device_ips, self.feature_data[feature_key].values())

        self.fig.canvas.draw()
        # This will run the GUI event
        # loop until all UI events
        # currently waiting have been processed
        self.fig.canvas.flush_events()

    def _update_rms(self, features):
        # device_ips = sorted(list(features.keys()))
        # print(device_ips)
        for device_ip, features_ in features.items():
            for feature_key, value in features_.items():
                self.feature_data[feature_key][device_ip] = value

    def update_ips(self, add, ip):
        if add == True:
            self.device_ips[ip] = True
        else:
            del self.device_ips[ip]
