from django.urls import path
from galeria import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('',views.galeria, name="Galeria"),
    path('sector/<int:sector_id>/',views.sector, name="sector"), #Se pasa el Id de categoría por parametro
]