from django.shortcuts import render,redirect

from servicios.models import Servicio,Item

# Create your views here.

def servicio(request):

    serv=Servicio.objects.all()
    Pos=Item.objects.all()
    return render(request,'servicios/servicio.html', {"Servicios":serv,"Post": Pos})

#Esta clase se define para que cuando pulsemos sobre una servicio en servicio.html
#se muestre item.html con el filtrado por el servicio seleccionada

def item(request, servicio_id):

    servtodos=Servicio.objects.all()
    serv=Servicio.objects.get(id=servicio_id) #Obtiene la Categoria segun el Id de la base de datos
    Pos=Item.objects.filter(items=serv) #Obtiene los post de esa categoria
    return render(request,'servicios/item.html', {"ServTodos": servtodos,"Servicios": serv,"Post": Pos})