import json
import copy
from .models import StockDetail
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
            print(stockpicker)
            for x in stockpicker:
                if x not in args:
                    args.append(x)
            task.args = json.dumps([args])
            task.save()
        else:
            schedule,created= IntervalSchedule.objects.get_or_create(every=70, period = IntervalSchedule.SECONDS)
            task = PeriodicTask.objects.create(interval = schedule, name='every-70-seconds', task="mainapp.tasks.my_task", args = json.dumps([stockpicker]))

    @sync_to_async
    def AddsStocksDetail(self,stockpicker):
        user=self.scope["user"]
        for i in stockpicker:
            stock,created=StockDetail.objects.get_or_create(stockselected=i)
            stock.user.add(user)#To make stock selection user specific we need to add user
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
        #Adding those user specific selected stocks inside our database so that
        #we can send user specific details
        await self.AddsStocksDetail(stockpicker)

        await self.accept()
    #We need this helper method to remove stocks and stock detail  object if our user is disconnected
    #from websocket and to remove the task if there is no arguments
    @sync_to_async
    def helper_func(self):
        user = self.scope["user"] #getting current user
        stocks = StockDetail.objects.filter(user__id = user.id)#getting stock_details objects of current user
        print(stocks)
        task = PeriodicTask.objects.get(name = "every-70-seconds")#getting periodic task object
        args = json.loads(task.args)#Getting arguments of periodic task
        args = args[0]
        print(args)
        for i in stocks:
            i.user.remove(user)#Removing user object related to stockdetail object
            print(i.user.count())
            if i.user.count() == 0:
                args.remove(i.stockselected)#If user is removed then stock  releted to that user
                               #will also be removed
                i.delete()#In same way stock details related to that user will
        print()                   #also get deleted
        if args == None:#IF there is no arguments in task then arguments field will be empty
            args = []
        #This condition deletes the task if task does not have any arguments
        if len(args) == 0:
            task.delete()
        else:
            task.args = json.dumps([args])
            task.save()
    async def disconnect(self, close_code):
        await self.helper_func()
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

    @sync_to_async
    def selectstockdetail(self):
        user=self.scope["user"]
        #We need __set for reverse lookup to StockDetail class objects.
        #basically we are acessing  all those StockDetails objects associated with specified
        #user
        print(user)
        user_stocks=user.stockdetail_set.values_list('stockselected',flat=True)
        return list(user_stocks)
    # Receive message from room group
    async def send_stock_update(self, event):
        message = event["message"]
        #Now we have a problem here as we know python automatically uses call by reference feature
        # when we are deleting message with del method in below code, we are actaully deleting the 
        #memory address that points towards that message by removing memory address which points towards
        #that message,The actual message will be removed form heap memory which will eventaually
        #remove message for all the users.To avoid that  we need to copy actaul message instead of
        #memory address for each user and delete that copied message.
        
        #Copying message
        message=copy.copy(message)
        #Note: message will contain address of newly created copy of actual data in heap memory.
        print("send vayexainaaaa")

        #Now we need to send those user specific details in frontend
        user_stocks=await self.selectstockdetail()
        keys=message.keys()
        print(keys)
        for i in list(keys):
            if i in user_stocks:
                pass
            else:
                del message[i]

        #Once we recieve message from tasks we will send that message which contains data to
        #frontend through WebSocket
        await self.send(text_data=json.dumps(message))
