from modbus2MQTT import ClienteMODBUS

dbPath = "C:\\Users\\mikin\\GitHubRepository\\SistemaModbus2MQTT\\DB\\database.db"
modbus_Addrs = '127.0.0.1'
modbus_Port = 502
modbus_DeviceID = 1
broker_local_Addrs = "127.0.0.1"
broker_cloud_Addrs = "****************"
broker_Port = 1883

c = ClienteMODBUS(modbus_Addrs, modbus_Port, modbus_DeviceID, broker_cloud_Addrs, broker_Port, dbPath)
c.atendimento()