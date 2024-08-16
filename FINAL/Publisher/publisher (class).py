import time
import json
import paho.mqtt.client as mqtt
from data_generator import SensorSimulator

class Publisher:
    def __init__(self, broker_address="localhost", port=1883, topic="test/topic", min_value=18, max_value=21):
        """
        Starts the publisher with the specified parameters.
        
        :param broker_address: Address of the MQTT broker (localhost).
        :param port: Port to connect to the MQTT broker (1883).
        :param topic: The topic to publish messages to (test/topic).
        :param min_value: The minimum value the sensor can generate (18).
        :param max_value: The maximum value the sensor can generate (21).
        """
        self.broker_address = broker_address
        self.port = port
        self.topic = topic
        self.client = mqtt.Client(protocol=mqtt.MQTTv311)
        self.sensor = SensorSimulator(min_value=min_value, max_value=max_value)

    def connect(self):
        self.client.connect(self.broker_address, self.port, 60)

    def disconnect(self):
        self.client.disconnect()

    def publish(self, repeat=10, interval=2):
        """
        Generates and sends data to the MQTT broker a specified number of times.
        
        :param repeat: Number of times to send data (10 times).
        :param interval: Time to wait between sending each message (2 seconds).
        """
        for _ in range(repeat):
            # Generate sensor data and package it with a timestamp as a JSON object
            data = {
                'sensor_value': self.sensor.generate_value(),
                'timestamp': time.asctime()
            }
            payload = json.dumps(data)

            # Publish the data to the broker on the specified topic
            self.client.publish(self.topic, payload)
            print(f"Published: {payload}")

            # Wait for 2 seconds before sending the next data
            time.sleep(interval)

    def start(self, repeat=10, interval=2):
        try:
            self.connect()
            self.publish(repeat=repeat, interval=interval)
        finally:
            self.disconnect()

# When the script is run directly, execute the publishing process
if __name__ == "__main__":
    publisher = Publisher()
    publisher.start()
