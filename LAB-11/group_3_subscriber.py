import paho.mqtt.client as mqtt
import json
from group_3_util import print_data

def on_message(client, userdata, msg):
    payload = msg.payload.decode('utf-8')
    data = json.loads(payload)
    print_data(data)

def subscribe():
    client = mqtt.Client()
    client.on_message = on_message

    client.connect("mqtt.eclipseprojects.io", 1883, 60)
    client.subscribe("test/topic")

    print("Subscribed to topic: test/topic")
    client.loop_forever()

if __name__ == "__main__":
    subscribe()
