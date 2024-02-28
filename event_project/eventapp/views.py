from django.shortcuts import render, redirect
from .forms import EventForm
from rest_framework import generics
from .models import Event
from .serializers import EventSerializer

def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_url')
    else:
        form = EventForm()
    return render(request, 'event_form.html', {'form': form})

class EventListAPIView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
