from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from carro.carro import Carro
from django.contrib import admin

from django.contrib.auth.forms import AuthenticationForm
from .forms import GenerarFormRegistracion

# Create your views here.

class VRegistro(View):

    def get(self,request):
        form=GenerarFormRegistracion()
        return render(request,"registro/registro.html",{"form":form})

    def post(self,request):
                
        form=GenerarFormRegistracion(request.POST)

        if form.is_valid():
            
            usuario=form.save()

            login(request, usuario)

            return redirect("Inicio")

        else:
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])

            return render(request,"registro/registro.html",{"form":form})


def cerrar_sesion(request):
        logout(request)
        
        return redirect("Inicio")


def logear(request):
    
    if request.method=="POST":
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            nombre_usuario=form.cleaned_data.get("username")
            contra=form.cleaned_data.get("password")
            usuario=authenticate(username=nombre_usuario,password=contra)

            if usuario is not None:
                login(request,usuario)
                return redirect("Inicio")
            else:
                for msg in form.error_messages:
                    messages.error(request, form.error_messages[msg])
        else:
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])
    
    
    form=AuthenticationForm()
    return render(request,"login/login.html",{"form":form})

    