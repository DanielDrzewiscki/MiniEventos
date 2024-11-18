from django.urls import path,include
from Aplicacion1 import views



from django.conf import settings
from django.conf.urls.static import static
#from django.conf.urls import url



urlpatterns = [
    path('',views.inicio, name="Inicio"),

]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



