from django.db import models

class Event(models.Model):
    event_id = models.CharField(max_length=100)
    event_name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    organiser_email = models.EmailField()
    organiser_name = models.CharField(max_length=100)
