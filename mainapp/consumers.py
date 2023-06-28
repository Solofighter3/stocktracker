import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async, async_to_sync
from urllib.parse import parse_qs
from django_celery_beat.models import PeriodicTask, IntervalSchedule
class StockConsumer(AsyncWebsocketConsumer):
    @sync_to_async
    def addToCeleryBeat(self, stockpicker):
        task = PeriodicTask.objects.filter(name = "every-70-seconds")
        #It will basically cheak whether the task is present or not
        #If task is already present then we will only add stocks as arguments to task
        #If task is not present we will create new task.
        if len(task)>0:
            print("hello")  # testing that task.first() will work or not
            task = task.first()
            args = json.loads(task.args)
            print(args)
            args = args[0]
            for x in stockpicker:
                if x not in args:
                    args.append(x)
            task.args = json.dumps([args])
            task.save()
        else:
            schedule, created = IntervalSchedule.objects.get_or_create(every=70, period = IntervalSchedule.SECONDS)
            task = PeriodicTask.objects.create(interval = schedule, name='every-70-seconds', task="mainapp.tasks.my_task", args = json.dumps([stockpicker]))
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        print(self.room_group_name)

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        #Parse qurrey string from url
        query_params = parse_qs(self.scope["query_string"].decode())
        print(query_params)
        stockpicker = query_params['stockspicker']
        
        #adding task in celerybeat with the parameters we just got in query_string
        await self.addToCeleryBeat(stockpicker)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
                self.room_group_name, {"type":"send_update",
                                   "message": message}
        )

    # Receive message from room group
    async def send_stock_update(self, event):
        message = event["message"]
        print("send vayexainaaaa")

        #Once we recieve message from tasks we will send that message which contains data to
        #frontend through WebSocket
        await self.send(text_data=json.dumps( message))