from django.db import models
from django.contrib.auth.models import User
class Contactus(models.Model):
    name=models.CharField(max_length=300)
    email=models.CharField(max_length=200)
    text=models.TextField()
    def __str__(self):
        return self.name


# Create your models here.
#We need this table so that we can provide details about only those stocks to user
#That he has selected 
#At first we will add those selected stocks by user inside our database
class StockDetail(models.Model):
    stockselected=models.CharField(max_length=255,unique=True)
    user=models.ManyToManyField(User)
    def __str__(self):
        return self.stockselected
    #ManyToManyField is used because any user can select any amount of stocks
