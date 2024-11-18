from django.urls import path
from servicios import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    
    path('',views.servicio, name="Servicio"),
    path('item/<int:servicio_id>/',views.item, name="item"), #Se pasa el Id de item por parametro
    
]

