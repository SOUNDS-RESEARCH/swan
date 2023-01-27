import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("TkAgg")

class MscPlotter:
    def __init__(self):
        # Currently only creating one plot, which
        # will hold the MSC.
        self.fig, self.ax = plt.subplots()

        plt.ion()
        plt.show()
        self.bar = None

    def update(self, features):
        device_ips = sorted(list(features.keys()))

        msc = [
            features[device_ip]["msc"]
            for device_ip in device_ips
        ]

        self.ax.clear()
        self.ax.set_title("Magnitude-squared coherence of each device")
        self.bar = self.ax.bar(device_ips, msc)

        self.fig.canvas.draw()
 
        # This will run the GUI event
        # loop until all UI events
        # currently waiting have been processed
        self.fig.canvas.flush_events()
