from django.db import models

class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField()
    form_filling_date = models.DateTimeField()
    event_start_date = models.DateTimeField()
    event_end_date = models.DateTimeField()
    attendees_gmail = models.EmailField()
    event_organiser_email = models.EmailField()
    event_organiser_name = models.CharField(max_length=100)
    google_event_id = models.CharField(max_length=255, blank=True, null=True)  # Add this field

    
    def __str__(self):
        return self.event_name
    

from django.db import models

class Musician(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    age = models.PositiveIntegerField()
    musician_category = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    ratings = models.FloatField()
    profileline = models.CharField(max_length=200)
    image_address = models.URLField()

    def __str__(self):
        return self.name

class EventOrganizer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    age = models.PositiveIntegerField()
    club_address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    profileline = models.CharField(max_length=200)
    image_address = models.URLField()

    def __str__(self):
        return self.name

