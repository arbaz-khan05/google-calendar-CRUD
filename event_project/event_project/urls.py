from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('event/', include('eventapp.urls')),
    path('success/', RedirectView.as_view(url='/event/'), name='success_url'),
    path('', RedirectView.as_view(url='/event/')),  
]
