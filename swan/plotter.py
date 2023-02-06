import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("TkAgg")


class Plotter:
    def __init__(self):
        self.feature_keys = ["msc"] # When adding new features, add their keys to this list

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
        
        self._update_msc(features)
        # Add new features plotting functions here.
        # You may use the _update_msc function as a template.

        self.fig.canvas.draw()
        # This will run the GUI event
        # loop until all UI events
        # currently waiting have been processed
        self.fig.canvas.flush_events()

    def _update_msc(self, features):
        device_ips = sorted(list(features.keys()))
        msc = [
            features[device_ip]["msc"]
            for device_ip in device_ips
        ]
        
        self.axs[0].clear()
        self.axs[0].set_title("Magnitude-squared coherence of each device")
        self.axs[0].bar(device_ips, msc)
