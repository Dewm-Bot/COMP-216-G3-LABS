import time
import json
import paho.mqtt.client as mqtt
from data_generator import SensorSimulator

# The publish function sends data to the MQTT broker at regular intervals.
def publish(repeat=10):
    """
    Generates and sends data to the MQTT broker a specified number of times.
    :param repeat: Number of times to send data (default is 10 times).
    """
    # Create an MQTT client and connect to the Mosquitto broker
    client = mqtt.Client(protocol=mqtt.MQTTv311)
    client.connect("localhost", 1883, 60)

    # Create a SensorSimulator object
    sensor = SensorSimulator(min_value=18, max_value=21)

    for _ in range(repeat):
        # Generate sensor data and package it with a timestamp as a JSON object
        data = {
            'sensor_value': sensor.generate_value(),
            'timestamp': time.asctime()
        }
        payload = json.dumps(data)

        # Publish the data to the broker on the specified topic
        client.publish("test/topic", payload)
        print(f"Published: {payload}")

        # Wait for 2 seconds before sending the next data
        time.sleep(2)

    # Disconnect from the broker after publishing is complete
    client.disconnect()

# When the script is run directly, execute the publish function
if __name__ == "__main__":
    publish()
