import pyaudio

# Recording settings
FORMAT = pyaudio.paInt16
SAMPLE_SIZE_IN_BYTES = 2 # This and FORMAT are coupled.
CHANNELS = 1
RATE = 44100
CHUNK = 4096

MQTT_BROKER_PORT = 1883
MQTT_BROKER_ADDRESS = "localhost"
MQTT_BROKER_KEEPALIVE_IN_SECS = 60

TOPIC = "topic/streams"
DATABASE_FILENAME = "recordings.db"
WAV_FILENAME = "recording.wav"
