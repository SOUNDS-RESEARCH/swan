import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import time

matplotlib.use("TkAgg")

COLORMAP = plt.get_cmap("Dark2")


class Plotter:
    def __init__(self):
        self.delta_t = 0.05
        self.last_update = time.time()

        self.feature_keys = ["vad", "rms", "snr"] # When adding new features, add their keys to this list
        self.device_names = {}
        self.feature_data = {}
        self.device_colors = {}
        
        for feature_key in self.feature_keys:
            self.feature_data[feature_key] = {}

        self.fig, axs = plt.subplots(nrows=len(self.feature_keys))
        
        axs = axs if isinstance(axs, np.ndarray) else [axs]

        self.axs = {}
        for ax, key in zip(axs, self.feature_keys):
            self.axs[key] = ax

        self._init_rms()
        # initialize the plots for features here

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

        current_time = time.time()
        if (current_time-self.last_update) < self.delta_t:
            return
        
        for ip in features:
            self.update_device_names(True, ip)

        # self._update_msc(features)
        self._update_vad(features)
        self._update_rms(features)
        self._update_snr(features)
        # Add new features plotting functions here.
        # You may use the _update_msc function as a template.

        self.fig.tight_layout()
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
        for device_ip in self.device_names.keys():
            if device_ip not in self.feature_data[feature_key]:
                self.feature_data[feature_key][device_ip] = [0]*RMS_FRAMES
            if device_ip in features and feature_key in features[device_ip]: # this might be slow, who knows, but it's just plotting, does it block the thread?
                self.feature_data[feature_key][device_ip].append(features[device_ip][feature_key])
                self.feature_data[feature_key][device_ip].pop(0)

            self.axs[feature_key].plot(self.feature_data[feature_key][device_ip], label=device_ip, color=self.device_colors[device_ip])
        
        self.axs[feature_key].legend()

    def _init_snr(self):
        self.axs["snr"].set_title("SNR of each device")

    def _update_snr(self, features):
        SNR_FRAMES = 128
        feature_key = "snr"
        # update local data
        # maybe this can be abstracted, but it's very feature-dependent
        # self.feature_data[feature_key] = {}
        self.axs[feature_key].clear()
        for device_ip in self.device_names.keys():
            if device_ip not in features: # TODO: Remove this I guess
                continue
            if device_ip not in self.feature_data[feature_key]:
                self.feature_data[feature_key][device_ip] = [0] * SNR_FRAMES
            if device_ip in features and feature_key in features[device_ip]:  # this might be slow, who knows, but it's just plotting, does it block the thread?
                self.feature_data[feature_key][device_ip].append(features[device_ip][feature_key])
                self.feature_data[feature_key][device_ip].pop(0)
            nf = features[device_ip]["noise_floor"]
            self.axs[feature_key].plot(self.feature_data[feature_key][device_ip], label=device_ip+"-NE:{:.3f}".format(nf),
                                       color=self.device_colors[device_ip])

        self.axs[feature_key].legend()

    # update plots

    def update_device_names(self, add, ip):
        if add == True:
            self.device_names[ip] = True
        else:
            if ip in self.device_names:
                del self.device_names[ip]
        
        if ip not in self.device_colors:
            self.device_colors[ip] = COLORMAP(len(self.device_colors))

    def _update_vad(self, features):
        feature_key = "vad"
        device_names = sorted(list(features.keys()))
        vad = [
            features[device_name][feature_key]
            for device_name in device_names
        ]
        colors = [
            self.device_colors[device_name]
            for device_name in device_names
        ]
        
        self.axs[feature_key].clear()
        self.axs[feature_key].set_title("Voice activity probability for each device")
        self.axs[feature_key].bar(device_names, vad, color=colors)
        self.axs[feature_key].set_ylim([0, 1])

    def _update_msc(self, features):
        feature_key = "vad"
        device_names = sorted(list(features.keys()))
        msc = [
            features[device_name][feature_key]
            for device_name in device_names
        ]

        self.axs[feature_key].clear()
        self.axs[feature_key].set_title("Magnitude-squared coherence of each device")
        self.axs[feature_key].bar(device_names, msc)
        self.axs[feature_key].set_ylim([0, 1])
