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
