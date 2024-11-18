from django.shortcuts import render, redirect

from blog.models import Categoria,Post

# Create your views here.

def blog(request):

    Cat=Categoria.objects.all()
    Pos=Post.objects.all()
    return render(request,'blog/blog.html', {"Categoria":Cat,"Post": Pos})

#Esta clase se define para que cuando pulsemos sobre una categoria en blog.html
#se muestre categoria.html con el filtrado por la categoria seleccionada

def categoria(request, categoria_id):

    Cat=Categoria.objects.all()
    Cate=Categoria.objects.get(id=categoria_id) #Obtiene la Categoria segun el Id de la base de datos
    Pos=Post.objects.filter(categorias=categoria_id) #Obtiene los post de esa categoria
    return render(request,'blog/categorias.html', {"Categorias":Cat,"Post": Pos,"Cate":Cate})