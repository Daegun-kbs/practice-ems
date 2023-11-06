import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
import aioredis
import requests
from datetime import datetime, timedelta, timezone
from decouple import config
from ems.models import *

service_key = config('WEATHER_KEY')
weather_url = config('WEATHER_URL')

# timezone
timezone_kst = timezone(timedelta(hours=9))

now_date = datetime.now().strftime('%Y%m%d')


class DataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        self.redis = await aioredis.from_url(f'redis://{config("REDIS_HOST")}')

        await self.receive_data()

    async def disconnect(self, close_code):
        self.redis.close()
        await self.redis.close()

    async def receive_data(self):
        while True:
            data = []
            
            for key in range(19):
                value = await self.redis.get(key)
                value = value.decode('utf-8')
                data.append((key, value))
            if data:
                await self.send(text_data=json.dumps({'data': data}))

            await asyncio.sleep(1)


class TimeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        while True:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 서버 시간을 가져옴
            await self.send(json.dumps({'time': current_time}))
            await asyncio.sleep(1)

    async def disconnect(self, close_code):
        pass


class WeatherConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        while True:
            try:
                now_time = datetime.now().strftime('%H00')
                params ={'serviceKey' : service_key, 'pageNo' : '1', 'numOfRows' : '1000', 'dataType' : 'JSON', 'base_date' : now_date, 'base_time' : now_time, 'nx' : '68', 'ny' : '101' }

                response = requests.get(weather_url, params=params, timeout=0.1)
                response = json.loads(response.content)
                try:
                    tmp, rain = parse_data(response)
                except:
                    # none body catch
                    now_time = int(datetime.now().strftime('%H00')) - 100
                    if now_time < 1000:
                        now_time = "0" + str(now_time)
                    params ={'serviceKey' : service_key, 'pageNo' : '1', 'numOfRows' : '1000', 'dataType' : 'JSON', 'base_date' : now_date, 'base_time' : now_time, 'nx' : '68', 'ny' : '101' }

                    response = requests.get(weather_url, params=params, timeout=0.1)
                    response = json.loads(response.content)
                    tmp, rain = parse_data(response)
            except:
            # time out catch
                tmp = ""
                rain = ""
        
            context = {
                'temp': tmp,
                'rain': rain
            }

            await self.send(json.dumps(context))
            await asyncio.sleep(10)        
                    
    async def disconnect(self, close_code):
        pass



# sub logic
def parse_data(response):
    data_body = response["response"]["body"]
    data_list = data_body["items"]["item"]

    for data in data_list:
        if data["category"] == "T1H":
            tmp = data["obsrValue"]
        elif data["category"] == "PTY":
            rain = data["obsrValue"]
    
    return tmp, rain