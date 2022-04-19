from mb2mqtt import ClienteMODBUS

modbus_Addrs = 'localhost'
modbus_Port = 502
modbus_DeviceID = 1
broker_local_Addrs = 'localhost'
broker_Port = 1883

c = ClienteMODBUS(modbus_Addrs, modbus_Port, modbus_DeviceID, broker_local_Addrs, broker_Port)
c.app()

# IP SEL: 192.168.100.180
# IP AWS: 3.134.40.193
# SEL735 - TENSÃO VAB 40365-366 LONG
#          CORRENT IA 40351-352 LONG
#          RELOGIO 2° 40201     UINT16