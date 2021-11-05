import os
import shutil

from pywasn.database import Database

TEST_DATABASE_PATH = "tests/fixtures/recordings.db"
TEMP_WAV_OUTPUT_FILE = "tests/temp/recording.wav"

def test_load_database_from_file():
    database = Database(TEST_DATABASE_PATH)

    entries = database.get_signals()
    
    assert len(entries) == 50


def test_to_wav():
    os.makedirs("tests/temp/", exist_ok=True)
    if os.path.exists(TEMP_WAV_OUTPUT_FILE):
        os.remove(TEMP_WAV_OUTPUT_FILE)

    database = Database(TEST_DATABASE_PATH)
    database.to_wav(TEMP_WAV_OUTPUT_FILE)

    assert os.path.exists(TEMP_WAV_OUTPUT_FILE)