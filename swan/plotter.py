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
        self.fig, axs = plt.subplots(nrows=len(self.feature_keys))
        axs = axs if type(axs) == list else [axs]

        self.axs = {}
        for ax, key in zip(axs, self.feature_keys):
            self.axs[key] = ax

        self._init_rms()
        # initialize the plots for features here

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

        self.fig.canvas.draw()
        # This will run the GUI event
        # loop until all UI events
        # currently waiting have been processed
        self.fig.canvas.flush_events()

    def _init_rms(self):
        self.axs["rms"].set_title("RMS of each device")

    def _update_rms(self, features):
        RMS_FRAMES = 128
        feature_key = "rms"
        # update local data
        
        # maybe this can be abstracted, but it's very feature-dependent
        # self.feature_data[feature_key] = {}
        self.axs[feature_key].clear()
        for device_ip in self.device_ips.keys():
            if device_ip not in self.feature_data[feature_key]:
                self.feature_data[feature_key][device_ip] = [0]*RMS_FRAMES
            if device_ip in features and feature_key in features[device_ip]: # this might be slow, who knows, but it's just plotting, does it block the thread?
                self.feature_data[feature_key][device_ip].append(features[device_ip][feature_key])
                self.feature_data[feature_key][device_ip].pop(0)

            self.axs[feature_key].plot(self.feature_data[feature_key][device_ip], label=device_ip)
        
        self.axs[feature_key].legend()

        # update plots

    def update_ips(self, add, ip):
        if add == True:
            self.device_ips[ip] = True
        else:
            if ip in self.device_ips:
                del self.device_ips[ip]
