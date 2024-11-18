from django.db import models
from django.contrib.auth.models import User #Importa los usuarios

# Create your models here.

class Categoria(models.Model):
    nombre=models.CharField(max_length=50)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name="Categoria"
        verbose_name_plural="Categorias"

    def __str__(self):
        return self.nombre

class Post(models.Model):
    titulo=models.CharField(max_length=50)
    nombrecliente=models.CharField(max_length=50, null=True)
    fechaevento=models.DateTimeField(null=True)
    contenido=models.TextField(editable=True, null=True)
    imagen=models.ImageField(upload_to='blog', null=True, blank=True) # indica que el campo no es obligatorio
    autor=models.ForeignKey(User, on_delete=models.CASCADE) # Esto relaciona el post con el usuario y permite borrar todas las entradas cuando el usuario se borra o retira de la página
    categorias=models.ManyToManyField(Categoria) #Esto le dice que es una relacion de mucho a muchos, Ej. Una categoria tiene muchos Post y un Post puede tener varias categorias
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)
    habilitado=models.BooleanField(default=True)

    class Meta:
        verbose_name="post"
        verbose_name_plural="posts"

    def __str__(self):
        return self.titulo