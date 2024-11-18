from django.shortcuts import render,redirect
from django.core.mail import EmailMessage
from .forms import FormularioContacto

# Create your views here.

def contacto(request):

                    
    #Ejemplo utilizando API FORM
    miformulario=FormularioContacto()
      
    if request.method=="POST":
        miformulario=FormularioContacto(data=request.POST)
        if miformulario.is_valid():
            nombre = request.POST.get("nombre")
            mail = request.POST.get("mail")
            contenido = request.POST.get("contenido")

            
            email= EmailMessage("Mensaje desde App Django","El usuario {} \n con el nombre {} \n Escribe lo siguiente: \n\n {}" 
            .format(nombre,mail,contenido),"",["fiesta.minieventos@gmail.com"])

            try:
                
                email.send()

                return redirect("/contacto/?Valido")       
       
            except:
                
                return redirect("/contacto/?NoValido")


    
    return render(request, 'contacto/contacto.html',{"Form":miformulario})

   