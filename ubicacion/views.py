from django.shortcuts import render,redirect


# Create your views here.

def ubicacion(request):
   
    return render(request, 'ubicacion/ubicacion.html')