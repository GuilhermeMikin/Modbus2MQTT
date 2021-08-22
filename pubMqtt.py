import paho.mqtt.client as mqtt
import sys
from time import sleep

broker_local_addrs = "127.0.0.1"
broker_aws_addrs = "3.134.40.193"
port = 1883

client = mqtt.Client()

if client.connect(broker_aws_addrs, port, 60) != 0:
    print("Não foi possível estabelecer conexão com o Broker MQTT!")
    sys.exit(-1)

topic1 = "/test/status/"
msg1 = f"Mensagem recebida de {topic1}!"

client.publish(topic1, msg1)
sleep(0.2)
print(f"\nMensagem publicada em {topic1}..\n")

client.disconnect()