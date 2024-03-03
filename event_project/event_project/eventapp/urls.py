from django.urls import path
from . import views
from .views import EventListCreate, EventRetrieveUpdateDestroy

urlpatterns = [
    # CRUD operations using function-based views
    path('', views.event_list, name='event_list'),
    path('event/<int:pk>/', views.event_detail, name='event_detail'),
    path('event/new/', views.event_create, name='event_create'),
    path('event/<int:pk>/edit/', views.event_update, name='event_update'),
    path('event/<int:pk>/delete/', views.event_delete, name='event_delete'),

    # CRUD operations using class-based views and REST API
    path('event/api/', EventListCreate.as_view(), name='event-list-create'),
    path('events/<int:pk>/', EventRetrieveUpdateDestroy.as_view(), name='event-detail'),
]
