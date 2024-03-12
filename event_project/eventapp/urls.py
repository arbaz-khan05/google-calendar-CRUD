# urls.py
from django.urls import path
from .views import (
    EventListView,
    EventListCreateAPIView,
    EventRetrieveUpdateDestroyAPIView,
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
    EventOrganizerRetrieveUpdateDestroyAPIView, 
    UserCredentialsCreateView,
    UserLoginAPIView,
)

urlpatterns = [
    
    # CRUD operations for events using class-based views
    path('', EventListView.as_view(), name='event_list'),
    path('event/<int:pk>/', EventRetrieveUpdateDestroyAPIView.as_view(), name='event_detail'),
    path('event/create/', EventCreateView.as_view(), name='event_create'),
    path('event/update/<int:pk>/', EventUpdateView.as_view(), name='event_update'),
    path('event/delete/<int:pk>/', EventDeleteView.as_view(), name='event_delete'),
    path('event/api/', EventListCreateAPIView.as_view(), name='api_event_list_create'), #it creates the event
    path('event/api/<int:pk>/', EventRetrieveUpdateDestroyAPIView.as_view(), name='api_event_detail'),

    # CRUD operations for musicians using class-based views
    path('musicians/', MusicianListView.as_view(), name='musician_list'),
    path('musicians/create/', MusicianCreateView.as_view(), name='musician_create'),
    path('musicians/update/<int:pk>/', MusicianUpdateView.as_view(), name='musician_update'),
    path('musicians/delete/<int:pk>/', MusicianDeleteView.as_view(), name='musician_delete'),
    path('musicians/api/', MusicianListCreateAPIView.as_view(), name='musician_list_create'),
    path('musicians/api/<int:pk>/', MusicianRetrieveUpdateDestroyAPIView.as_view(), name='musician_retrieve_update_destroy'),

    # CRUD operations for event organizers using class-based views
    path('eventorganizers/', EventOrganizerListView.as_view(), name='event_organizer_list'),
    path('eventorganizers/create/', EventOrganizerCreateView.as_view(), name='event_organizer_create'),
    path('eventorganizers/update/<int:pk>/', EventOrganizerUpdateView.as_view(), name='event_organizer_update'),
    path('eventorganizers/delete/<int:pk>/', EventOrganizerDeleteView.as_view(), name='event_organizer_delete'),
    path('eventorganizers/api/', EventOrganizerListCreateAPIView.as_view(), name='event_organizer_list_create'),
    path('eventorganizers/api/<int:pk>/', EventOrganizerRetrieveUpdateDestroyAPIView.as_view(), name='event_organizer_retrieve_update_destroy'),

    # CRUD operations for Login and User using class-based views
    path('user-credentials/create/', UserCredentialsCreateView.as_view(), name='user_credentials_create'),
    path('login/', UserLoginAPIView.as_view(), name='user_login'),
]



