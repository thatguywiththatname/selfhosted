# Converts the "json" file from ttn-receiver into a csv file.
# Example usage:
#   python3 ./out-to-csv.py ./ttn-receiver-data/data.json ./data.csv

import json
import sys

with open(sys.argv[2], "w") as outf:
    outf.write("time,pm1_pm10,pm1_pm25,pm2_pm10,pm2_pm25,temperature,humidity\n")
    with open(sys.argv[1], "r") as f:
        for line in f.readlines():
            data = json.loads(line)
            p = data["payload_fields"]
            time = data["metadata"]["time"]
            temp = int(p["temperature"]) / 10
            humidity = int(p["humidity"]) / 10
            outf.write(
                f'{time},{p["PM1_PM10"]},{p["PM1_PM25"]},{p["PM2_PM10"]},{p["PM2_PM25"]},{temp},{humidity}\n'
            )
