from pywasn.database import Database
from pywasn.utils.statistics import get_packet_time_stats


TEST_DATABASE_PATH = "tests/fixtures/recordings.db"


def test_get_packet_time_stats():
    database = Database(path=TEST_DATABASE_PATH)

    entries = database.get_packets()
    
    stats = get_packet_time_stats(entries)
    assert stats == (0.09285523559873467, # Avg
                     0.0053123145302723706, # Std
                     0.08434772491455078, # Min
                     0.10402798652648926) # Max