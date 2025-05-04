import json
from channels.generic.websocket import AsyncWebsocketConsumer


class DataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        print("Данные получены по WebSocket:", data)
        # Можно сохранять в базу или отправлять клиентам
        await self.send(text_data=json.dumps({"status": "received", "data": data}))
