from django.urls import path
from ubicacion import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('',views.ubicacion, name="Ubicacion"),
]