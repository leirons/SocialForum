from django.http.response import HttpResponse
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from django.core.cache import cache

cache.set("messages", [])


class Consumer(WebsocketConsumer):
    def connect(self):
        print("connected")
        self.room_name = self.scope['url_route']['kwargs']["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )
        self.accept()


    def disconnect(self, code):
        pass

    def receive(self, text_data):
        print('receive')
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )
        lst = cache.get("messages")
        lst.append(message)
        cache.set("messages",lst)
        print(cache.get("messages"))

    def chat_message(self,event):
        print("message")
        message = event['message']
        self.send(text_data=json.dumps({
            "message":message
        }))


