## MQTT Broker Setup

### Installing Mosquitto
1. Download and install the Mosquitto broker from [mosquitto.org/download](https://mosquitto.org/download/).
2. Once installed, start the broker using the following command:
mosquitto

3. Ensure the broker is running by testing it with simple publish and subscribe commands:

mosquitto_sub -h localhost -t test/topic
mosquitto_pub -h localhost -t test/topic -m "Test Message"

### Running the Publisher and Subscriber
1. Start the broker as described above.
2. Run the Publisher script:

python FINAL/Publisher/publisher.py

3. Run the Subscriber script provided by your team members to ensure messages are being received.

