import paho.mqtt.client as mqtt
import sys
from time import sleep

broker_local_addrs = "127.0.0.1"
broker_cloud_addrs = "****************"
port = 1883

def onMessage(client, userdata, msg):
    sleep(0.5)
    print("\nMensagem recebida..")
    print("Topic: " + str(msg.topic) + "  Message: " + str(msg.payload.decode("utf-8")))

client = mqtt.Client()
client.on_message = onMessage

if client.connect(broker_local_addrs, port, 60) != 0:
    print("Não foi possível estabelecer conexão com o Broker MQTT!")
    sys.exit(-1)
else:
    print("Cliente MQTT conectado..")

client.subscribe("/test/status/")

try:
    print("\nPressione CTRL+C para desconectar...")
    client.loop_forever()
except:
    print("\nDesconectando-se do Broker")
client.disconnect()