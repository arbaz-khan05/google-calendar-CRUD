from django.urls import path
from .views import (
    EventListCreateAPIView,
    EventRetrieveUpdateDestroyAPIView,
    MusicianListCreateAPIView,
    MusicianRetrieveUpdateDestroyAPIView,
    EventOrganizerListCreateAPIView,
    EventOrganizerRetrieveUpdateDestroyAPIView,
    UserCredentialsCreateView,
    UserLoginAPIView,
    EventFilterByEmailAPIView,
)

urlpatterns = [
    # CRUD operations for events using class-based views
    path('events/', EventListCreateAPIView.as_view(), name='event_list'),
    path('events/update/<int:pk>/', EventRetrieveUpdateDestroyAPIView.as_view(), name='event_update'),
    path('events/delete/<int:pk>/', EventRetrieveUpdateDestroyAPIView.as_view(), name='event_delete'),
    path('events/api/', EventListCreateAPIView.as_view(), name='api_event_list_create'), #it creates the event
    path('events/api/<int:pk>/', EventRetrieveUpdateDestroyAPIView.as_view(), name='api_event_detail'),


    # CRUD operations for musicians using class-based views
    path('musicians/', MusicianListCreateAPIView.as_view(), name='musician_list'),
    path('musicians/update/<int:pk>/', MusicianRetrieveUpdateDestroyAPIView.as_view(), name='musician_update'),
    path('musicians/delete/<int:pk>/', MusicianRetrieveUpdateDestroyAPIView.as_view(), name='musician_delete'),
    path('musicians/api/', MusicianListCreateAPIView.as_view(), name='musician_list_create'),
    path('musicians/api/<int:pk>/', MusicianRetrieveUpdateDestroyAPIView.as_view(), name='musician_retrieve_update_destroy'),

    # CRUD operations for event organizers using class-based views
    path('eventorganizers/', EventOrganizerListCreateAPIView.as_view(), name='event_organizer_list'),
    path('eventorganizers/update/<int:pk>/', EventOrganizerRetrieveUpdateDestroyAPIView.as_view(), name='event_organizer_update'),
    path('eventorganizers/delete/<int:pk>/', EventOrganizerRetrieveUpdateDestroyAPIView.as_view(), name='event_organizer_delete'),
    path('eventorganizers/api/', EventOrganizerListCreateAPIView.as_view(), name='event_organizer_list_create'),
    path('eventorganizers/api/<int:pk>/', EventOrganizerRetrieveUpdateDestroyAPIView.as_view(), name='event_organizer_retrieve_update_destroy'),

    # CRUD operations for User Credentials using class-based views
    path('user-credentials/create/', UserCredentialsCreateView.as_view(), name='user_credentials_create'),
    path('login/', UserLoginAPIView.as_view(), name='user_login'),

    # API endpoint for filtering events by email
    path('events/filter-by-email/', EventFilterByEmailAPIView.as_view(), name='event_filter_by_email'),
]
