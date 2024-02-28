from django.urls import path
from . import views
from .views import EventListAPIView

urlpatterns = [
    path('', views.add_event, name='add_event'), 
    path('api/', EventListAPIView.as_view(), name='event-list'),
]
