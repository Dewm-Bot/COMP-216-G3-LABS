import paho.mqtt.client as mqtt
import json
import time
from group_3_util import create_data

def publish():
    client = mqtt.Client()
    client.connect("mqtt.eclipseprojects.io", 1883, 60) 

    for _ in range(5):
        data = create_data()
        payload = json.dumps(data)

        client.publish("test/topic", payload)
        print(f"Published: {payload}")

        time.sleep(2)

    client.disconnect()

if __name__ == "__main__":
    publish()