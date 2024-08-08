import paho.mqtt.client as mqtt
import json
import time
from group_3_util import create_data

def publish(repeat=5):
    client = mqtt.Client()

    try:
        client.connect("mqtt.eclipseprojects.io", 1883, 60)
    except Exception as e:
        print(f"Failed to connect to MQTT broker: {e}")
        return

    for _ in range(repeat):
        try:
            data = create_data()
            payload = json.dumps(data)
            client.publish("test/topic", payload)
            print(f"Published: {payload}")
        except Exception as e:
            print(f"Failed to publish message: {e}")
        
        time.sleep(2)

    client.disconnect()

if __name__ == "__main__":
    publish()
