import paho.mqtt.client as mqtt
import json
from group_3_util import print_data

max_attempts = 3
attempts = 0
max_loops = 300
loops = 0

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
    global attempts, loops
    
    while attempts < max_attempts:
        try:
            client.connect("mqtt.eclipseprojects.io", 1883, 60)
            client.subscribe("test/topic")
            print("Subscribed to topic: test/topic")
            break
        except Exception as e:
            attempts += 1
            print(f"Attempt {attempts} failed: {e}")
            if attempts >= max_attempts:
                print(f"Exceeded maximum attempts ({max_attempts}). Exiting.")
                break
    while loops < max_loops:
        client.loop(timeout=1.0)
        loops += 1
    print("Timeout Achieved. Exiting.")
    client.disconnect()

if __name__ == "__main__":
    subscribe()
