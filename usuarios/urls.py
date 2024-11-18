from django.urls import path
from usuarios import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('',views.usuarios, name="Usuarios"),
    path('contratos/<int:categoria_id>/',views.contratos, name="contratos"),
    path('vermenu/<int:categoria_id>/',views.vermenu, name="vermenu"),
    
]