import paho.mqtt.client as mqtt
import redis
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import mariadb
import sys
from datetime import datetime
from pytz import timezone


seoul = timezone('Asia/Seoul')


# redis

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


# influx

org = "daegun"
bucket="mybucket"
token = "vQvd8DSmUI08XPImHRSLzPpBJsV0x1mwPigtMQU_i8SaiTeaJpNHzz1crHSnbHRAqpy53w_WXwOUmd7qvtt-6Q=="
url = "http://localhost:8086"

client = influxdb_client.InfluxDBClient(
        url = url,
        token = token,
        org = org
)

write_api = client.write_api(write_options=SYNCHRONOUS)

def make_point(tablename, dic):
    point = {
    'measurement': tablename,
    'tags': dic['tags'],
    'fields': dic['fields'],
    }
    return point


# mariaDB

try:
        conn = mariadb.connect(
                user="root",
                password="daegun123",
                host="localhost",
                port=3306,
                database="mydb"
                )
                
except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

# Get Cursor
cur = conn.cursor()

select_query = "SELECT accumulate_energy FROM ems_ems ORDER BY id DESC LIMIT 1"
        
cur.execute(select_query)

query_data = cur.fetchone()

if query_data:
        accumulate_energy = float(query_data[0])
else:
        accumulate_energy = 0
        
seconds = 0

def on_message(client, userdata, message):
        
        global seconds
        
        # receive data

        parse = list(message.payload)
        
        pcs = parse[0:8]
        battery = parse[8:17]
        pv = parse[17:18]
        
        voltage_r = pcs[0]
        voltage_s = pcs[1]
        voltage_t = pcs[2]
        current_r = pcs[3]
        current_s = pcs[4]
        current_t = pcs[5]
        active_power = pcs[6]
        frequency = pcs[7]
        
        save_date = datetime.now(seoul)
        
        global accumulate_energy
        accumulate_energy += active_power / 3600
        parse.insert(8, round(accumulate_energy, 2))
        
        # redis
        
        for i in range(len(parse)):
                redis_client.set(i, parse[i])
               
               
        # influx
        
        dic = {
                'tags': {
                        'location' : 'daegun'
                },
                'fields' : {
                        'voltage_R' : voltage_r,
                        'voltage_S' : voltage_s,
                        'voltage_T' : voltage_t,
                        'current_R' : current_r,
                        'current_S' : current_s,
                        'current_T' : current_t,
                        'active_power' : active_power,
                        'frequency' : frequency,
                        'accumulate_energy' : accumulate_energy
                }
        }

        p = make_point("ems_data", dic)

        send_body = []
        send_body.append(p)

        write_api.write(bucket=bucket, org=org, record=send_body)
        
                
        # maria        
        
        print(f'second: {seconds}')

        if seconds % 60 == 0:
                pcs_query = "INSERT INTO ems_ems(voltage_R, voltage_S, voltage_T, current_R, current_S, current_T, active_power, frequency, save_date, accumulate_energy) \
                        VALUES (%s,%s,%s, %s,%s,%s, %s,%s, %s, %s)"
                battery_query = "INSERT INTO ems_battery(DCvoltage_R, DCvoltage_S, DCvoltage_T, DCcurrent_R, DCcurrent_S, DCcurrent_T, active_power, SOC, SOH, save_date) \
                        VALUES (%s,%s,%s, %s,%s,%s, %s,%s,%s, %s)"
                pv_query = "INSERT INTO ems_photovoltaics(active_power, save_date) \
                        VALUES (%s,%s)"
                        
                try: 
                        pcs.append(save_date)
                        pcs.append(accumulate_energy)
                        battery.append(save_date)
                        pv.append(save_date)
                        
                        cur.execute(pcs_query, pcs)
                        cur.execute(battery_query, battery)
                        cur.execute(pv_query, pv)
                        conn.commit()
                except mariadb.Error as e: 
                        print(f"Error: {e}")
                        conn.rollback()
       
        seconds += 1

broker_address = "127.0.0.1"
client1 = mqtt.Client("client1")
client1.connect(broker_address)
client1.subscribe("PLC")
client1.on_message = on_message
client1.loop_forever()