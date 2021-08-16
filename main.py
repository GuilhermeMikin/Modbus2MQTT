from mestreModbus import ClienteMODBUS

dbpath = "C:\\Users\\mikin\\GitHubRepository\\SistemaModbus2MQTT\\DB\\database.db"

ipAddrs = '127.0.0.1'

c = ClienteMODBUS(ipAddrs, 502, 1, dbpath=dbpath)
c.atendimento()