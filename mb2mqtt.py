from pyModbusTCP.client import ModbusClient
import paho.mqtt.client as mqtt
from time import sleep
from threading import Thread
import sys


class ClienteMODBUS():
    """
    Classe Cliente MODBUS 
    """

    def __init__(self, server_addr, porta, device_id, broker_addr, broker_port, scan_time=0.2):
        """
        Construtor
        """
        self._app = True
        self._scan_time = scan_time
        self._server_ip = server_addr
        self._device_id = device_id
        self._port = porta
        self._cliente = ModbusClient(
            host=server_addr, 
            port=porta, 
            unit_id=device_id)

        self._broker_addrs = broker_addr
        self._broker_port = broker_port
        self._client_mqtt = mqtt.Client()
        self._status_conn_mqtt = False

        self._threadread = None
        self._readingthread = False


    def app(self):
        """
        Método para primeiras opções do usuário
        """
        try:
            print('-' * 100)
            print('Welcome to Modbus2MQTT Gateway!!'.center(100))
            print()
            while self._app == True:
                print("""
Available Options:
1- Default configurations (Modbus and MQTT local, it is also possible to change it later)
2- Set Modbus and MQTT configurations
3- About Modbus2MQTT Gateway
4- Close APP""")
                while True:
                    firstoptions = input("Option: ")
                    if firstoptions not in '1' and firstoptions not in '2' and firstoptions not in '3' and firstoptions not in '4':
                        print('Enter a valid option...')
                        sleep(0.5)
                    else:
                        break

                if firstoptions == '1':
                    print('\nDefault Configurations...')
                    self.atendimento()

                elif firstoptions == '2':
                    try:
                        modbus_server_ip = input('\nPlease, enter the Modbus TCP IP Address: ')
                        if modbus_server_ip == "l":
                            self._server_ip = 'localhost'
                        else:
                            self._server_ip = modbus_server_ip
                        self._port = input('Enter the TCP Port: ')
                        print('\n--> Testing Modbus/TCP connection.. ', end='')
                        self._cliente.open()
                        sleep(0.3)
                        print('--> OK')
                    except Exception as e: 
                        print('ERROR: ', e.args)

                    mqtt_broker = str(
                        input('\nPlease, now enter the MQTT Broker Address: '))
                    if mqtt_broker == "aws":
                        self._broker_addrs = "3.134.40.193"
                    else:
                        self._broker_addrs = mqtt_broker
                    self._broker_port = int(input('Enter the Port: '))
                    print('\n--> Testing MQTT BROKER connection.. ', end='')
                    sleep(1)
                    try:
                        if self._client_mqtt.connect(self._broker_addrs, self._broker_port, 60) != 0:
                            print("Unable to establish connection with MQTT Broker!")
                            sys.exit(-1)
                        else:
                            print('--> OK')
                            self._status_conn_mqtt = True
                    except Exception as e: 
                        print('ERROR: ', e.args)
                        print(
                            "\nUnable to establish connection with MQTT Broker!\nCheck if the IP Address is OK and try again...")
                        print('Following without connection with MQTT Broker..')
                    self._client_mqtt.disconnect()
                    self.atendimento()

                elif firstoptions == '3':
                    print()
                    print('-' * 100)
                    print('Modbus2MQTT Gateway- (Version 2 - 2022)'.center(100))
                    print("""
Modbus2MQTT Gateway is an app responsible for communicating between a Modbus/TCP network 
and an MQTT Broker through a specific topic, security options such as password and user
for MQTT communication have not yet been implemented in this version...""")
                    print('\nDeveloped by: Guilherme Balduino Lopes')
                    print('Email: guilhermebalopes@ufu.br\n')
                    print('-' * 100)
                    print()
                    exitabt = input('Enter to exit...')

                elif firstoptions == '4':
                    confirm_close = input('\nType "YES" to confirm you want to exit the app: ').capitalize()[0]
                    if confirm_close == 'Y':
                        sleep(0.2)
                        print('\nShutting down...\n')
                        sleep(1)
                        self._app = False
                    else:
                        print('\nGetting back...')
                else:
                    print('Not found...')

        except Exception as e:
            print('ERRO: ', e.args)


    def atendimento(self):
        """
         Método para atendimento do usuário
        """
        try:
            atendimento = True
            while atendimento:
                print()
                print('-'*100)
                print('ModbusTCP/MQTT Client'.center(100))
                print('-'*100)
                sel = input("""
Available services: 
1- Start a read 
2- Stop reading 
3- Write a value 
4- Configuration 
5- About 
6- Exit 
Service N°: """)
                if sel == '1':
                    print('\nAvailable Function Codes:')
                    print("""
1- Coil Status 
2- Input Status 
3- Holding Register 
4- Input Register""")
                    while True:
                        tipo = int(input("Function Code: "))
                        if str(tipo) not in '12345':
                            print('Enter a valid type...')
                            sleep(0.5)
                        else:
                            break

                    if tipo == 3 or tipo == 4:
                        if tipo == 3:
                            func = "F03-HoldingRegister"
                        else:
                            func = "F04-InputRegister"
                        addr = int(input(f'\nModbus Starting Address: '))
                        leng = int(input(f'Quantity of Registers: '))
                        sleep(0.3)
                        try:
                            self._readingthread = True
                            self._threadread = Thread(target=self.readThread, args=(tipo, addr, leng, func))
                            self._threadread.start()
                            print('\nReading has started and data is being published to the specified topic...\n')
                        except Exception as e:
                            print('ERRO: ', e.args)
                            try:
                                sleep(0.5)
                                print('\nTrying again...')
                                if not self._cliente.is_open():
                                    self._cliente.open()
                                sleep(0.5)
                                self._readingthread = True
                                self._threadread = Thread(target=self.readThread, args=(tipo, addr, leng, func))
                                self._threadread.start()
                                print('\nReading has started and data is being published to the specified topic...\n')
                            except Exception as e:
                                print('ERRO: ', e.args)
                                print('\nClient was unable to receive a response... \nBack to menu...\n\n')
                                sleep(1.5)

                    else:
                        if tipo == 1:
                            func = "F01-CoilStatus"
                        else:
                            func = "F02-InputStatus"
                        addr = int(input(f'\nModbus Starting Address: '))
                        leng = int(input(f'Quantity of Registers: '))
                        sleep(0.3)
                        try:
                            self._readingthread = True
                            self._threadread = Thread(target=self.readThread, args=(tipo, addr, leng, func))
                            self._threadread.start()
                            print('\nReading has started and data is being published to the specified topic...\n')
                        except Exception as e:
                            print('ERRO: ', e.args)
                            try:
                                sleep(0.5)
                                print('\nTrying again...')
                                if not self._cliente.is_open():
                                    self._cliente.open()
                                sleep(0.5)
                                self._readingthread = True
                                self._threadread = Thread(target=self.readThread, args=(tipo, addr, leng, func,))
                                self._threadread.start()
                                print('\nReading has started and data is being published to the specified topic...\n')
                            except Exception as e:
                                print('ERRO: ', e.args)
                                print('\nClient was unable to receive a response... \nBack to menu...\n\n')
                                sleep(1.5)

                elif sel == '2':
                    try:
                        self._readingthread = False
                        print("\nStopping reading...\n")
                    except Exception as e:
                        print('ERROR: ', e.args)
                        print('\nUnable to sotp reading... \nReturning to menu...\n\n')
                        sleep(1.5)

                elif sel == '3':
                    print('\nWhat kind of data do you want to write? \n1- Coil Status \n2- Holding Register')
                    while True:
                        tipo = int(input("Type: "))
                        if tipo > 2:
                            print('Enter a valid type...')
                            sleep(0.5)
                        else:
                            break
                    addr = input('Address: ')
                    valor = int(input('What to write: '))
                    try:
                        print('\nWriting...')
                        sleep(0.5)
                        self.escreveDado(int(tipo), int(addr), valor)
                    except Exception as e:
                        print('ERROR: ', e.args)
                        print('\nUnable to write... \nReturning to menu...\n\n')
                        sleep(1.5)

                elif sel == '4':
                    print('\nSettings: ')
                    print('1- Modbus Connection Settings \n2- MQTT Broker Settings \n3- Exit')
                    while True:
                        tpconfig = input("Set up: ")
                        if tpconfig not in '123':
                            print('Enter a valid configuration type... (1, 2 or 3)')
                            sleep(0.5)
                        else:
                            break
                    if int(tpconfig) == 1:
                        print('')
                        print('-' * 100)
                        print('Modbus Communication Settings'.center(100))
                        print(f'\n-> Current settings: - IP Addrs: {self._server_ip} - TCP Port: {self._port} - Device ID: {self._device_id} - Scan_Time: {self._scan_time}s')
                        print('\nSettings: \n1- IP Address \n2- TCP Port  \n3- Device ID \n4- Scan Time \n5- Exit')
                        while True:
                            config = input("Set up: ")
                            if config not in '12345':
                                print('Enter a valid configuration type... (1, 2, 3, 4 or 5)')
                                sleep(0.5)
                            else:
                                break
                        if int(config) == 1:
                            ipserv = str(input(' New IP address: '))
                            try:
                                self._cliente.close()
                                self._server_ip = ipserv
                                self._cliente = ModbusClient(
                                    host=self._server_ip)
                                self._cliente.open()
                                print(f'\nIP address successfully chaged to {ipserv}!!\n')
                                sleep(0.5)
                            except Exception as e:
                                print('ERROR: ', e.args)
                                print('\nUnable to change IP address.. \nReturning to menu...\n\n')
                                sleep(0.5)
                        elif int(config) == 2:
                            porttcp = input(' New TCP port: ')
                            try:
                                self._cliente.close()
                                self._port = int(porttcp)
                                self._cliente = ModbusClient(port=self._port)
                                self._cliente.open()
                                print(f'\nTCP port successfully changed to {porttcp}!!\n')
                                sleep(0.5)
                            except Exception as e:
                                print('ERROR: ', e.args)
                                print('\nUnable to change TCP port... \nReturning to menu...\n\n')
                                sleep(0.5)
                        elif int(config) == 3:
                            while True:
                                iddevice = input(' New device ID: ')
                                if 0 <= int(iddevice) < 256:
                                    break
                                else:
                                    print('Device ID must be an integer between 0 and 256.', end='')
                                    sleep(0.5)
                            try:
                                self._cliente.close()
                                self._device_id = int(iddevice)
                                self._cliente = ModbusClient(
                                    unit_id=self._device_id)
                                self._cliente.open()
                                print(f'\nDevice ID successfully changed to {iddevice}!!\n')
                                sleep(0.5)
                            except Exception as e:
                                print('ERROR: ', e.args)
                                print('\nUnable to change device ID.. \nReturning to menu...\n\n')
                                sleep(0.5)
                        elif int(config) == 4:
                            scant = input(' New scan time [s]: ')
                            try:
                                self._scan_time = float(scant)
                                print(f'\nScan time successfully changed to {scant}s!!\n')
                            except Exception as e:
                                print('ERROR: ', e.args)
                                print('\nUnable to change Scan Time.. \nReturning to menu...\n\n')
                                sleep(0.5)
                        elif int(config) == 5:
                            print('\nGetting back...\n')
                            sleep(0.5)
                        else:
                            print('Not found...\n')
                            sleep(0.7)
                    elif int(tpconfig) == 2:
                        print('')
                        print('-' * 100)
                        print('MQTT Broker Settings'.center(100))
                        print(f'\n-> Current settings: - IP Addrs: {self._broker_addrs} - Port: {self._broker_port}')
                        print('\nSettings: \n1- IP Address \n2- Port \n3- Exit')
                        while True:
                            config = input("Set up: ")
                            if config not in '123':
                                print('Enter a valid configuration type... (1, 2 or 3)')
                                sleep(0.5)
                            else:
                                break
                        if int(config) == 1:
                            ipserv = str(input(' New Broker IP address: '))
                            try:
                                self._broker_addrs = ipserv
                                print('\n--> Testing MQTT BROKER Connection... ', end='')
                                sleep(0.5)
                                try:
                                    if self._client_mqtt.connect(self._broker_addrs, self._broker_port, 60) != 0:
                                        print("Unable to establish connection with MQTT Broker!")
                                        sys.exit(-1)
                                    else:
                                        print(' --> OK')
                                        print(f'Broker IP successfully changed to {ipserv}!!\n')
                                        self._status_conn_mqtt = True
                                        sleep(0.2)
                                except Exception as e:
                                    print('ERROR: ', e.args)
                                    print("\nCould not establish connection with MQTT Broker!\nCheck if IP Address is OK and try again..")
                                    print('Following without connection with MQTT Broker..')
                                    self._status_conn_mqtt = False
                                self._client_mqtt.disconnect()
                            except Exception as e:
                                print('ERROR: ', e.args)
                                print('\nUnable to change Broker IP address.. \nReturning to menu..\n\n')
                                sleep(0.5)
                        elif int(config) == 2:
                            portbroker = input(' New port: ')
                            try:
                                self._broker_port = portbroker
                                print(f'\nPort successfully changed to {portbroker}!!\n')
                                sleep(0.5)
                            except Exception as e:
                                print('ERROR: ', e.args)
                                print('\nUnable to change MQTT port.. \nReturning to menu..\n\n')
                                sleep(0.5)
                        elif int(config) == 3:
                            print('\nGetting back...\n')
                            sleep(0.5)
                        else:
                            print('Not found...\n')
                            sleep(0.7)
                    else:
                        print('\nGetting back...\n')
                        sleep(0.5)
                elif sel == '5':
                    print()
                    print('-' * 100)
                    print('ModbusTCP/MQTT - (Version 2 - 2022)'.center(100))
                    print('\nDeveloped by: Guilherme Balduino Lopes')
                    print('Email: guilhermebalopes@ufu.br\n')
                    print('-' * 100)
                    print()
                    exitabt = input('Enter to exit...')
                elif sel == '6':
                    confirm_close = input('\nType "YES" to confirm you want to exit the app: ').capitalize()[0]
                    if confirm_close == 'Y':
                        sleep(0.2)
                        print('\nShutting down...\n')
                        self._readingthread = False
                        self._cliente.close()
                        sleep(1)
                        atendimento = False
                        self._app = False
                    else:
                        print('\nGetting back...')
                else:
                    print('Not found...\n')
                    sleep(0.7)
        except Exception as e:
            print('ERRO: ', e.args)

    def lerDado(self, tipo, addr, leng=1):
        """
        Método para leitura MODBUS
        """
        if tipo == 1:
            co = self._cliente.read_coils(addr - 1, leng)
            return co

        elif tipo == 2:
            di = self._cliente.read_discrete_inputs(addr - 1, leng)
            return di

        elif tipo == 3:
            hr = self._cliente.read_holding_registers(addr - 1, leng)
            return hr

        elif tipo == 4:
            ir = self._cliente.read_input_registers(addr - 1, leng)
            return ir

        else:
            print('Not Found...')


    def escreveDado(self, tipo, addr, valor):
        """
        Método para escrita MODBUS
        """
        try:
            if tipo == 1:
                print(f'{valor} written at the specified address ({addr})\n')
                return self._cliente.write_single_coil(addr - 1, valor)
            elif tipo == 2:
                print(f'{valor} written at the specified address ({addr})\n')
                return self._cliente.write_single_register(addr - 1, valor)
            else:
                print('Invalid writing type..\n')

        except Exception as e:
            print('ERROR: ', e.args)

    def mqttPublish(self, topic, msg):
        """
        Método para escrita MODBUS
        """
        try:
            if self._client_mqtt.connect(self._broker_addrs, self._broker_port, 60) != 0:
                print("Unable to establish connection with MQTT Broker!")
                sys.exit(-1)
            self._client_mqtt.publish(topic, msg)
            sleep(0.2)
            self._client_mqtt.disconnect()
        except Exception as e:
            print('ERROR: ', e.args, end='')
            print('Error when trying to publish to broker, please check IP address and port...')
            self._status_conn_mqtt = False

    def readThread(self, tipo, addr, leng, func):
        """
        Método para thread de leitura
        """
        try:
            i = 0
            while self._readingthread:
                modbusValues = self.lerDado(int(tipo), int(addr), leng)
                if self._status_conn_mqtt:
                    self.mqttPublish(topic="test/status", msg=f"Read {i+1} - ({addr}:{leng}) {func}: {modbusValues}")
                sleep(self._scan_time)
                i += 1
                sleep(0.2)
        except Exception as e:
            print('ERROR: ', e.args, end='')
            print('Error when trying to publish to broker, please check IP address and port...')
