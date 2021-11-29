from mb2mqtt import ClienteMODBUS

modbus_Addrs = '127.0.0.1'
modbus_Port = 502
modbus_DeviceID = 1
broker_local_Addrs = "127.0.0.1"
broker_cloud_Addrs = "3.134.40.193"
broker_Port = 1883

#192.168.100.180

c = ClienteMODBUS(modbus_Addrs, modbus_Port, modbus_DeviceID, broker_cloud_Addrs, broker_Port)
c.atendimento()

# SEL735 - TENSÃO VAB 40365-366 LONG
#          CORRENT IA 40351-352 LONG
#          RELOGIO 2° 40201     UINT16