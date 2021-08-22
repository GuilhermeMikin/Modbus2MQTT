# import paho.mqtt.client as mqtt
# import sys
# from time import sleep


# class MQTTPublisher():
#     """
#     Classe MQTT Publicador
#     """
#     def __init__(self,broker_addrs,porta,device_id=1,scan_time=0.1,valor=0,dbpath="C:\database.db"):
#         """
#         Construtor
#         """
#         self.broker_addrs = "3.134.40.193"
#         self.broker_port = 1883
#         self._scan_time = scan_time
#         self._server_ip = server_ip
#         self._device_id = device_id
#         self._port = porta
#         self._cliente = ModbusClient(host=server_ip, port=porta, unit_id=device_id)

#         self._dbpath = dbpath
#         self._valor = valor
#         self._con = sqlite3.connect(self._dbpath)
#         self._cursor = self._con.cursor()

#     def atendimento(self):