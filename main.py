import os
import paho.mqtt.client as mqtt


class MQTTSubscriber:
    def __init__(self, host, port, topic):
        self.host = host
        self.port = port
        self.topic = topic
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode()
        os.system(f"echo {payload} >> cache")

    def start(self):
        self.client.connect(self.host, self.port, 60)
        self.client.loop_forever()


def main():
    print("UP MQTT")
    mqtt_host = "localhost"
    mqtt_port = 1883
    mqtt_topic = "test/status"

    mqtt_subscriber = MQTTSubscriber(mqtt_host, mqtt_port, mqtt_topic)

    mqtt_subscriber.start()


if __name__ == "__main__":
    main()
