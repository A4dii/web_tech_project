from channels.generic.websocket import AsyncWebsocketConsumer
import json

class GestureConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("gesture_group", self.channel_name)
        await self.accept()
        print("✅ WebSocket connection accepted!")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("gesture_group", self.channel_name)
        print("❌ WebSocket disconnected!")

    async def receive(self, text_data):
        print("📥 Received from python sender:", text_data)
        data = json.loads(text_data)
        gesture = data.get("gesture")

        await self.channel_layer.group_send(
            "gesture_group",
            {
                "type": "gesture.message",
                "gesture": gesture
            }
        )

    async def gesture_message(self, event):
        gesture = event["gesture"]
        await self.send(text_data=json.dumps({
            'action': gesture
        }))
        print("📤 Sent to frontend:", gesture)
