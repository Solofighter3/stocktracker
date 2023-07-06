from django.shortcuts import render
from .models import Room,Message
# Create your views here.
def room(request,id):
    val=[c.name for c in Room.objects.all()]
    if id not in val:
         room=Room.objects.create(name=id)
    else:
        room=Room.objects.get(name=id)
    message=Message.objects.filter(room=room)
    print(message)
    return render(request,"room.html",{"room_name":id,"messages":message})
