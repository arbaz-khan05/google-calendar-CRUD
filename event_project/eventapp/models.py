# models.py
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
import uuid
from django.db import models
from django.conf import settings

class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField()
    created_on = models.DateTimeField(default=timezone.now) 
    event_start_date = models.DateTimeField()
    event_end_date = models.DateTimeField()
    event_organiser_email = models.EmailField(unique=True)
    event_organiser_name = models.CharField(max_length=100)
    google_event_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    def __str__(self):
        return self.event_name

    def clean(self):
        if self.event_start_date > self.event_end_date:
            raise ValidationError('Event end date should be after event start date.')

class Musician(models.Model):
    musician_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    created_on = models.DateTimeField(default=timezone.now)
    category = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    ratings = models.DecimalField(max_digits=5, decimal_places=2)
    profileline = models.CharField(max_length=200)
    imageAddress = models.URLField()

class EventOrganizer(models.Model):
    eventorganizer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    created_on = models.DateTimeField(default=timezone.now)
    club_address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    profileline = models.CharField(max_length=200)
    imageaddress = models.URLField()

class UserCredentials(models.Model):
    UserCredential_id = models.AutoField(primary_key=True)
    createdon = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def validate_email(self):
        if self.category == 'musician':
            try:
                Musician.objects.get(email=self.email)
                return True, f"{self.email} is already registered as a musician. Kindly login."
            except Musician.DoesNotExist:
                return False, f"{self.email} is not registered as a musician. Please complete registration."
        elif self.category == 'event organizer':
            try:
                EventOrganizer.objects.get(email=self.email)
                return True, f"{self.email} is already registered as an event organizer. Kindly login."
            except EventOrganizer.DoesNotExist:
                return False, f"{self.email} is not registered as an event organizer. Please complete registration."
        else:
            return False, "Invalid category specified."
