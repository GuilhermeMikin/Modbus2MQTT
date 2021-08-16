import paho.mqtt.client as mqtt
import sys
from time import sleep

broker_addrs = "127.0.0.1"
port = 1883

client = mqtt.Client()

if client.connect(broker_addrs, port, 60) != 0:
    print("Could not connect to MQTT Broker!")
    sys.exit(-1)

topic1 = "test/status"
msg1 = "Hello World from paho-mqtt!"

client.publish(topic1, msg1)
sleep(0.2)
print(f"Publicado no tópico {topic1}..")

client.disconnect()