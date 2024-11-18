from django.shortcuts import render, redirect

from galeria.models import Sector,Detalle


# Create your views here.

def galeria(request):
   
    Sect=Sector.objects.all()
    Det=Detalle.objects.all()
   
    return render(request, 'galeria/galeria.html', {"Sector":Sect,"Detalle": Det})

#Esta clase se define para que cuando pulsemos sobre un sector en galeria.html
#se muestre galeria.html con el filtrado por el sector seleccionado


def sector(request, sector_id):

    Sect=Sector.objects.all()
    Secto=Sector.objects.get(id=sector_id) #Obtiene la Categoria segun el Id de la base de datos
    Det=Detalle.objects.filter(sectores=Secto) #Obtiene los post de esa categoria
    return render(request, 'galeria/detalle.html', {"Sector":Sect,"Detalle": Det,"Sectorid":Secto})

