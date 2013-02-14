from django.db import models

# Create your models here.
class CalEvent(models.Model):
    name = models.CharField(max_length=200)
    startDate = models.DateTimeField('startDate')
    endDate = models.DateTimeField('endDate')
    description = models.CharField(max_length=2000)
    day = models.CharField(max_length=2)
