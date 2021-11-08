import numpy as np

from typing import List


def get_packet_time_stats(packets: List[tuple]):
    """Get the average and standard deviation
        of the time between received packets, in seconds.


    Args:
        packets (List[tuple]): List of tuples where every tuple contains three elements:
                                    The signal, the timestamp at the sender, and the sender id
    """
    
    times = []

    for i in range(len(packets) - 1):
        times.append(
            packets[i + 1][1] - packets[i][1] 
        )

    times = np.array(times)

    return times.mean(), times.std(), times.min(), times.max()
