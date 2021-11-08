import os
import re

from pywasn.database import Database

TEST_DATABASE_PATH = "tests/fixtures/recordings.db"
TEMP_WAV_OUTPUT_FILE = "tests/temp/recording.wav"

def test_load_database_from_file():
    database = Database(path=TEST_DATABASE_PATH)

    entries = database.get_packets()
    
    assert len(entries) == 152


# def test_to_wav():
#     os.makedirs("tests/temp/", exist_ok=True)
#     if os.path.exists(TEMP_WAV_OUTPUT_FILE):
#         os.remove(TEMP_WAV_OUTPUT_FILE)

#     database = Database(path=TEST_DATABASE_PATH)
#     #os.chdir("tests/temp/")
#     database.to_wav()

#     assert os.path.exists(TEMP_WAV_OUTPUT_FILE)


def test_get_publisher_ips():
    database = Database(path=TEST_DATABASE_PATH)

    entries = database.get_publisher_ips()
    assert len(entries) == 2
    assert re.match(r"(\d+\.){3}\d", entries[0])
