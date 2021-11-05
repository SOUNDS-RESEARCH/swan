import socket
import sqlite3

from pywasn.settings import DATABASE_FILENAME, CHUNK
from pywasn.audio_utils import frames_to_wav


CREATE_QUERY = f"""
    CREATE TABLE recordings
    (data BINARY({CHUNK}), timestamp FLOAT, sender_ip VARCHAR)
"""

INSERT_QUERY = """INSERT INTO recordings (data, timestamp, sender_ip)
                  VALUES (?, ?, ?)"""

GET_QUERY = """SELECT * FROM recordings WHERE sender_ip == ? """


class Database:
    def __init__(self, path=None):
        if path is None:
            self.con = sqlite3.connect(DATABASE_FILENAME)
            self.cur = self.con.cursor()

            self.cur.execute(CREATE_QUERY)
            self.con.commit()
        else:
            self.con = sqlite3.connect(path)
            self.cur = self.con.cursor()

    def insert(self, data, timestamp, id):
        self.cur.execute(INSERT_QUERY, (data, timestamp, id))
        self.con.commit()

    def get_signals(self, sender_ip=None):
        if sender_ip is None:
            # Default: save local signal
            sender_ip = _get_local_ip()

        entries = self.cur.execute(GET_QUERY, (sender_ip, ))
        return entries.fetchall()

    def to_wav(self, output_file_path, sender_ip=None):
        entries = self.get_signals(sender_ip)
        frames = [entry[0] for entry in entries]
        
        frames_to_wav(frames, output_file_path)


def _get_local_ip():
    return socket.gethostbyname(socket.gethostname())
