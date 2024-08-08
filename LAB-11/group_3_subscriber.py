import paho.mqtt.client as mqtt
import json
from group_3_util import print_data

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode('utf-8')
        data = json.loads(payload)
        print_data(data)
    except Exception as e:
        print(f"Failed to process message: {e}")

def subscribe():
    client = mqtt.Client()
    client.on_message = on_message

    try:
        client.connect("mqtt.eclipseprojects.io", 1883, 60)
        client.subscribe("test/topic")
        print("Subscribed to topic: test/topic")
    except Exception as e:
        print(f"Failed to connect or subscribe to MQTT broker: {e}")
        return

    client.loop_forever()

if __name__ == "__main__":
    subscribe()
