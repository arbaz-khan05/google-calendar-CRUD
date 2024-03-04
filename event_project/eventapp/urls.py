from django.urls import path
from .views import (
    EventListView,
    EventListCreate,
    EventRetrieveUpdateDestroy,
    EventCreateView,
    EventUpdateView,
    EventDeleteView,
    MusicianListView,
    MusicianCreateView,
    MusicianUpdateView,
    MusicianDeleteView,
    EventOrganizerListView,
    EventOrganizerCreateView,
    EventOrganizerUpdateView,
    EventOrganizerDeleteView,
    MusicianListCreateAPIView, 
    EventOrganizerListCreateAPIView,
    MusicianRetrieveUpdateDestroyAPIView,
    EventOrganizerRetrieveUpdateDestroyAPIView
)

urlpatterns = [
    
    # CRUD operations for events using class-based views
    path('', EventListView.as_view(), name='event_list'),
    path('event/<int:pk>/', EventRetrieveUpdateDestroy.as_view(), name='event_detail'),
    path('event/add/', EventCreateView.as_view(), name='event_create'),
    path('event/update/<int:pk>/', EventUpdateView.as_view(), name='event_update'),
    path('event/delete/<int:pk>/', EventDeleteView.as_view(), name='event_delete'),
    path('events/api/', EventListCreate.as_view(), name='api_event_list_create'),
    path('events/api/<int:pk>/', EventRetrieveUpdateDestroy.as_view(), name='api_event_detail'),

    # CRUD operations for musicians using class-based views
    path('musicians/', MusicianListView.as_view(), name='musician_list'),
    path('musicians/add/', MusicianCreateView.as_view(), name='musician_create'),
    path('musicians/update/<int:pk>/', MusicianUpdateView.as_view(), name='musician_update'),
    path('musicians/delete/<int:pk>/', MusicianDeleteView.as_view(), name='musician_delete'),
    path('musicians/api/', MusicianListCreateAPIView.as_view(), name='musician_list_create'),
    path('musicians/api/<int:pk>/', MusicianRetrieveUpdateDestroyAPIView.as_view(), name='musician_retrieve_update_destroy'),

    # CRUD operations for event organizers using class-based views
    path('eventorganizers/', EventOrganizerListView.as_view(), name='event_organizer_list'),
    path('eventorganizers/add/', EventOrganizerCreateView.as_view(), name='event_organizer_create'),
    path('eventorganizers/update/<int:pk>/', EventOrganizerUpdateView.as_view(), name='event_organizer_update'),
    path('eventorganizers/delete/<int:pk>/', EventOrganizerDeleteView.as_view(), name='event_organizer_delete'),
    path('eventorganizers/api/', EventOrganizerListCreateAPIView.as_view(), name='event_organizer_list_create'),
    path('eventorganizers/api/<int:pk>/', EventOrganizerRetrieveUpdateDestroyAPIView.as_view(), name='event_organizer_retrieve_update_destroy'),
]

