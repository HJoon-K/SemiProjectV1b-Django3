import datetime

from django.db import models

# Create your models here.
class Board(models.Model):
    id = models.AutoField(primary_key=True)
    userid = models.CharField(max_length=18)
    title = models.CharField(max_length=100)
    contxt = models.TextField(max_length=5000)
    regdate = models.DateTimeField(default=datetime.datetime.now)
    lpcnt = models.IntegerField(default=0)

