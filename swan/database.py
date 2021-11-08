import sqlite3
import pandas as pd

from pywasn.utils.audio import frames_to_wav
from pywasn.utils.hydra import load_config
from pywasn.utils.network import get_local_ip
from pywasn.utils.statistics import get_packet_time_stats


CREATE_QUERY = """
    CREATE TABLE frames (
        data BLOB({}), timestamp FLOAT, publisher_ip VARCHAR
    )
"""

INSERT_QUERY = """INSERT INTO frames (data, timestamp, publisher_ip)
                  VALUES (?, ?, ?)"""

GET_PUBLISHERS_QUERY = """SELECT DISTINCT publisher_ip  FROM frames"""

GET_SIGNAL_QUERY = """SELECT * FROM frames WHERE publisher_ip == ? """


class Database:
    def __init__(self, config=None, path=None):
        if not config:
            config = load_config()

        self.config = config

        if path is None:
            self.con = sqlite3.connect(config["audio"]["database_filename"])
            self.cur = self.con.cursor()

            self.cur.execute(CREATE_QUERY.format(config["audio"]["chunk"]))
            self.con.commit()
        else:
            self.con = sqlite3.connect(path)
            self.cur = self.con.cursor()

    def insert(self, data, timestamp, id):
        self.cur.execute(INSERT_QUERY, (data, timestamp, id))
        self.con.commit()

    def get_packets(self, publisher_ip=None, only_frame=False):
        if publisher_ip is None:
            # Default: save local signal
            publisher_ip = get_local_ip()

        entries = self.cur.execute(GET_SIGNAL_QUERY, (publisher_ip, ))
        frames = entries.fetchall()
        if only_frame:
            frames = [entry[0] for entry in frames]
        return frames

    def to_wav(self):
        publisher_ips = self.get_publisher_ips()
        for publisher_ip in publisher_ips:
            frames = self.get_packets(publisher_ip, only_frame=True)
            file_name = publisher_ip.replace(".", "_") + ".wav"
            frames_to_wav(frames, self.config["audio"], file_name)

    def get_publisher_ips(self):
        publishers = self.cur.execute(GET_PUBLISHERS_QUERY)
        return [p[0] for p in publishers.fetchall()]

    def get_stats(self, as_dataframe=True):
        publisher_ips = self.get_publisher_ips()
        stats = []
        for publisher_ip in publisher_ips:
            frames = self.get_packets(publisher_ip)
            avg, std, min, max = get_packet_time_stats(frames)
            stats.append({
                "publisher_ip": publisher_ip,
                "avg": avg,
                "std": std,
                "min": min,
                "max": max
            })

        if as_dataframe:
            stats = pd.DataFrame(stats)

        return stats
