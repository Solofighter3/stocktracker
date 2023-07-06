
# Create your models here.

from django.db import models
from  django.contrib.auth.models import User
class Room(models.Model):
    name=models.CharField(max_length=225)
    

class Message(models.Model):
     room=models.ForeignKey(Room,related_name='messages',on_delete=models.CASCADE)
     user=models.ForeignKey(User,related_name='messages',on_delete=models.CASCADE)
     content=models.TextField()
     date_added=models.DateTimeField(auto_now_add=True)
     class Meta:
        ordering=('date_added',) 
