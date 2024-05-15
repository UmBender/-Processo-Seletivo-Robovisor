import asyncio
import os
import paho.mqtt.client as mqtt

queue = asyncio.Queue()


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
        queue.put_nowait(payload)

    async def start(self):
        while True:
            self.client.connect(self.host, self.port, 60)
            self.client.loop_start()
            await asyncio.sleep(0.5)
            self.client.loop_stop()


async def consumer():
    while True:
        token = await queue.get()
        print(queue)
        format = f"echo \'{token}\' >> .temp"
        os.system(format)
        festival_command = "festival --tts .temp"
        process = await asyncio.create_subprocess_shell(
            festival_command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.communicate()
        os.system("rm .temp")
        queue.task_done()


async def main():
    print("UP MQTT")
    mqtt_host = "localhost"
    mqtt_port = 1883
    mqtt_topic = "test/status"

    sub = MQTTSubscriber(mqtt_host, mqtt_port, mqtt_topic)

    consumers = [asyncio.create_task(consumer()) for _ in range(1)]
    producers = [asyncio.create_task(sub.start()) for _ in range(1)]

    await asyncio.gather(*consumers)
    await asyncio.gather(*producers)


if __name__ == "__main__":
    asyncio.run(main())
