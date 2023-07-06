from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from room.models import Room, Message
class Chatconsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.roomname=self.scope['url_route']['kwargs']['room_name']
        self.room_group_name="chat_%s" % self.roomname
        await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
                )
        await self.accept()
                         
   
    async def receive(self, text_data):
        data=json.loads(text_data)
        message=data['message']
        username=data['username']
        roomname=data['roomname']
        await self.save_message(username,roomname,message)
        await self.channel_layer.group_send(
                self.room_group_name,
                {
                "type":"chat_message",
                 "message":message,
                 "username":username,
                 'roomname':roomname
                 })

                             
   
    async def chat_message(self,event):
        message=event["message"]
        username=event["username"]
        roomname=event["roomname"]
        print(message)
        await self.send(text_data=json.dumps({
            'type':'text',
            'message': message,
            'username': username,
            'roomname':roomname
             }))
      
    @sync_to_async
    def save_message(self, username, room, message):
        user = User.objects.get(username=username)
        room = Room.objects.get(name=room)


        Message.objects.create(user=user, room=room, content=message)
