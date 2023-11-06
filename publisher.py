from pymodbus.client import ModbusTcpClient
from pymodbus.transaction import *
import paho.mqtt.client as mqtt
import time
import random

client = ModbusTcpClient("127.0.0.1", 502)
result = client.read_holding_registers(0, 10, unit=1)

mqttc = mqtt.Client("python_pub")
mqttc.connect("127.0.0.1", 1883)

while True:
    data = []
    for i in range(15):
        data.append(random.randrange(0, 100))

    a = random.randrange(40, 100)
    b = random.randrange(80, 100)
    
    if (a >= b):
        data.append(b)
        data.append(a)
    else:
        data.append(a)
        data.append(b)
    data.append(random.randrange(0, 100))
    client.write_registers(0, data)
    # 0~7 pcs
    # 8~16 battery
    # 17 pv
    rr = client.read_holding_registers(0, 18, unit=1)

    mqttc.publish("PLC", bytearray(rr.registers))
    
    time.sleep(1)