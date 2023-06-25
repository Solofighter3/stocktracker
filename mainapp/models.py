from django.db import models

class Contactus(models.Model):
    name=models.CharField(max_length=300)
    email=models.CharField(max_length=200)
    text=models.TextField()
    def __str__(self):
        return self.name

