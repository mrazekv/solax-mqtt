
from paho.mqtt import client as mqtt_client
import random
import logging
import time

class MqttLocal:
    # username = 'emqx'
    # password = 'public'

    def __init__(self):
        broker = 'localhost'
        port = 1883
        self.topic = "solax"
        client_id = f'python-mqtt-{random.randint(0, 1000)}'
        self.client = self.connect_mqtt(client_id, broker, port)
        pass

    def connect_mqtt(self, client_id, broker, port):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)
        # Set Connecting Client ID
        client = mqtt_client.Client(client_id)
        # client.username_pw_set(username, password)
        client.on_connect = on_connect
        client.on_disconnect = self.on_disconnect
        client.connect(broker, port)
        return client


    def on_disconnect(self, client, userdata, rc):
        FIRST_RECONNECT_DELAY = 1
        RECONNECT_RATE = 2
        MAX_RECONNECT_COUNT = 12
        MAX_RECONNECT_DELAY = 60
        logging.info("Disconnected with result code: %s", rc)
        reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
        while reconnect_count < MAX_RECONNECT_COUNT:
            logging.info("Reconnecting in %d seconds...", reconnect_delay)
            time.sleep(reconnect_delay)

            try:
                client.reconnect()
                logging.info("Reconnected successfully!")
                return
            except Exception as err:
                logging.error("%s. Reconnect failed. Retrying...", err)

            reconnect_delay *= RECONNECT_RATE
            reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
            reconnect_count += 1
        logging.info("Reconnect failed after %s attempts. Exiting...", reconnect_count)


    def __setitem__(self, i, val):
        self.client.publish(self.topic + "/" + i, val)
        pass

if __name__ == "__main__":
    mqtt = MqttLocal()
    mqtt["topic1"] = random.random() * 100
    