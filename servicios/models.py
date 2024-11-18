from django.db import models

# Create your models here.

class Servicio(models.Model):
    titulo=models.CharField(max_length=50)
    contenido=models.CharField(max_length=50, null=True)
    imagen=models.ImageField(upload_to='servicios', null=True, blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name="servicio"
        verbose_name_plural="servicios"

    def __str__(self):
        return self.titulo 

    
class Item(models.Model):
    tituloitem=models.CharField(max_length=50)
    nombreitem=models.CharField(max_length=50, null=True)
    contenidoitem=models.TextField(editable=True, null=True)
    imagenitem=models.ImageField(upload_to='servicios', null=True, blank=True) # indica que el campo no es obligatorio
    items=models.ManyToManyField(Servicio) #Esto le dice que es una relacion de mucho a muchos, Ej. Una categoria tiene muchos Post y un Post puede tener varias categorias
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)
    habilitado=models.BooleanField(default=True)

    class Meta:
        verbose_name="item"
        verbose_name_plural="items"

    def __str__(self):
        return self.tituloitem