from django.db import models

# Create your models here.

class User(models.Model):
    email = models.CharField(max_length=120)
    password = models.CharField(max_length=120)
    name = models.CharField(max_length=30)
    profile = models.CharField(max_length=250,default='')

    def __str__(self):
        return self.email



