from pywasn.database import Database
from pywasn.statistics import get_packet_stats


TEST_DATABASE_PATH = "tests/fixtures/recordings.db"


def test_get_packet_stats():
    database = Database(TEST_DATABASE_PATH)

    entries = database.get_signals()
    
    avg_time_between_packets, std_time_between_packets = get_packet_stats(entries)

    assert avg_time_between_packets == 0.09300661087036133
    assert std_time_between_packets == 0.005686837660447592