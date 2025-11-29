from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from certs.api import token
import random
import time

# ---- InfluxDB Config ----
url = "http://localhost:8086"
org = "my_org"                   # Replace with your org
bucket = "game_metrics"          # Bucket you created

client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

# ---- Simulate Game Metrics ----
players = ["Alice", "Bob", "Charlie"]

while True:
    for player in players:
        score = random.randint(0, 100)      # Example metric
        health = random.randint(50, 100)    # Another metric
        level = random.randint(1, 10)       # Example game level

        point = Point("player_stats") \
            .tag("player", player) \
            .field("score", score) \
            .field("health", health) \
            .field("level", level)

        write_api.write(bucket=bucket, org=org, record=point)
        print(f"Sent metrics for {player}: score={score}, health={health}, level={level}")

    time.sleep(5)  # Send updates every 5 seconds
