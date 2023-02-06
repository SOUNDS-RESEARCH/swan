import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("TkAgg")


class Plotter:
    def __init__(self):
        self.feature_keys = ["rms"] # When adding new features, add their keys to this list
        self.device_ips = {}
        self.feature_data = {}
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
        for feature_key in self.feature_keys:
            self.feature_data[feature_key] = {}
            for device_ip in self.device_ips.keys():
                if device_ip in features and feature_key in features[device_ip]:
                    self.feature_data[feature_key][device_ip] = features[device_ip][feature_key]
                else:
                    self.feature_data[feature_key][device_ip] = np.nan

        # self._update_rms(features)
        # Add new features plotting functions here.
        # You may use the _update_rms function as a template.
        if len(self.feature_keys) == 1:
            self.axs.clear()
            self.axs.bar(self.feature_data[feature_key].keys(), self.feature_data[self.feature_keys[0]].values())
        else:
            for id, feature_key in enumerate(self.feature_keys):
                self.axs[id].clear()
                self.axs[id].bar(self.feature_data[feature_key].keys(), self.feature_data[feature_key].values())

        self.fig.canvas.draw()
        # This will run the GUI event
        # loop until all UI events
        # currently waiting have been processed
        self.fig.canvas.flush_events()

    def _update_rms(self, features):
        # device_ips = sorted(list(features.keys()))
        # print(device_ips)
        # for device_ip, features_ in features.items():
        #     for feature_key, value in features_.items():
        #         self.feature_data[feature_key][device_ip] = value
        pass

    def update_ips(self, add, ip):
        # print("pepe")
        if add == True:
            self.device_ips[ip] = True
        else:
            if ip in self.device_ips:
                del self.device_ips[ip]
