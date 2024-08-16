import time
import json
import paho.mqtt.client as mqtt
from data_generator import SensorSimulator
import threading

class Publisher:
    def __init__(self, broker_address="localhost", port=1883, topic="test/topic", min_value=18, max_value=21):
        self.broker_address = broker_address
        self.port = port
        self.topic = topic
        self.client = mqtt.Client(protocol=mqtt.MQTTv311)
        self.sensor = SensorSimulator(min_value=min_value, max_value=max_value)
        self.stop_flag = threading.Event()

    def connect(self):
        self.client.connect(self.broker_address, self.port, 60)

    def disconnect(self):
        self.client.disconnect()

    def publish(self, repeat=10, interval=2):
        self.connect()
        try:
            for _ in range(repeat):
                if self.stop_flag.is_set():
                    print("Publishing stopped.")
                    break
                # Generate sensor data and package it with a timestamp as a JSON object
                data = {
                    'sensor_value': self.sensor.generate_value(),
                    'timestamp': time.asctime()
                }
                payload = json.dumps(data)

                # Publish the data to the broker on the specified topic
                self.client.publish(self.topic, payload)
                print(f"Published: {payload}")

                # Wait for the specified interval before sending the next data
                time.sleep(interval)
        finally:
            self.disconnect()

    def start(self, repeat=10, interval=2):
        self.stop_flag.clear()
        self.publish(repeat=repeat, interval=interval)

    def stop(self):
        self.stop_flag.set()

# Standalone execution
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="MQTT Publisher")
    parser.add_argument("--repeat", type=int, default=10, help="Number of times to publish data")
    parser.add_argument("--interval", type=float, default=2, help="Interval between publications in seconds")
    parser.add_argument("--min_value", type=float, default=18, help="Minimum value for sensor data")
    parser.add_argument("--max_value", type=float, default=21, help="Maximum value for sensor data")
    args = parser.parse_args()

    publisher = Publisher(min_value=args.min_value, max_value=args.max_value)
    publisher.start(repeat=args.repeat, interval=args.interval)
