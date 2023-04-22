from cgitb import text
from channels.generic.websocket import WebsocketConsumer
import json
from .models import *
from asgiref.sync import async_to_sync, sync_to_async

class OrderProgress(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['id']
        print(self.room_name)
        self.room_group_name = "order_%s" % self.room_name
        print('connect')
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        order = order_Data.given_order(self.room_name)
        self.send(text_data=json.dumps({
            "payload":order}
        ))
    

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
    def receive(self, text_data):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'order_stats',
                'payload':text_data
            }
        )

    def order_stats(self,event):
        print(event)
        data=json.loads(event['value'])
        self.send(text_data=json.dumps({
            'payload':data
        }))