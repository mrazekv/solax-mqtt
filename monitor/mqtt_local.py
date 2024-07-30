
import paho.mqtt.client as mqtt
import random
import logging
import time

class MqttLocal:
    def __init__(self, server, user, password, port, topic):
        self.topic = topic
        self.user = user
        self.password = password
        client_id = f'python-mqtt-{random.randint(0, 1000)}'
        self.client = self.connect_mqtt(client_id, server, port)


    def connect_mqtt(self, client_id, broker, port):
        def on_connect(client, userdata, flags, reason_code, properties):
            if reason_code == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", reason_code)
        # Set Connecting Client ID
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        if self.user:
            client.username_pw_set(self.user, self.password)

        client.on_connect = on_connect
        client.on_disconnect = self.on_disconnect
        client.connect(broker, port)
        return client

    # (client, userdata, disconnect_flags, reason_code, properties)
    def on_disconnect(self, client, userdata, disconnect_flags, rc, params):
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
    
