from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Tablas(models.Model):
    titulo = models.CharField(max_length=50)
    linkpagina = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    orden = models.IntegerField(null=True)

    class Meta:
        verbose_name = "tabla"
        verbose_name_plural = "tablas"
        ordering = ['orden']

    def __str__(self):
        return self.titulo


class Pagina(models.Model):
    nombreformulario = models.CharField(max_length=50)
    nombrevista = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    habilitado = models.BooleanField(default=True)
    tabla = models.ForeignKey(Tablas, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "pagina"
        verbose_name_plural = "paginas"

    def __str__(self):
        return self.nombreformulario


class Usuarioregistrado(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombreusuario = models.CharField(max_length=50)
    mailusuario = models.CharField(max_length=50)
    passwordusuario = models.CharField(max_length=50)

    class Meta:
        verbose_name = "usuarioregistrado"
        verbose_name_plural = "usuarioregistrados"
        ordering = ['nombreusuario']
        unique_together = ["usuario"]

    def __str__(self):
        return self.nombreusuario

class ModalidadMenu(models.Model):
    modalidaddemenu=models.CharField(max_length=50)
    activo=models.BooleanField(default=True)

    class Meta:
        verbose_name = "ModalidadMenu"
        verbose_name_plural = "ModalidadMenus"
        ordering = ['modalidaddemenu']
        

    def __str__(self):
        return self.modalidaddemenu


class TipoMenu(models.Model):
    tipodemenu=models.CharField(max_length=50)
    activo=models.BooleanField(default=True)

    class Meta:
        verbose_name = "TipoMenu"
        verbose_name_plural = "TipoMenus"
        ordering = ['tipodemenu']
        

    def __str__(self):
        return self.tipodemenu


class FamiliaMenu(models.Model):
    nombrefamilia=models.CharField(max_length=50)
    activo=models.BooleanField(default=True)
    orden=models.IntegerField()

    class Meta:
        verbose_name = "FamiliaMenu"
        verbose_name_plural = "FamiliaMenus"
        ordering = ['orden']
        

    def __str__(self):
        return self.nombrefamilia

class CartaMenu(models.Model):
    tipofamilia=models.ForeignKey(FamiliaMenu, on_delete=models.PROTECT)
    tipomodalidad=models.ForeignKey(ModalidadMenu, on_delete=models.PROTECT)
    tipomenu=models.ForeignKey(TipoMenu, on_delete=models.PROTECT)
    nombremenu=models.CharField(max_length=50)
    fotomenu=models.ImageField(upload_to='administracion', null=True, blank=True)
    detallemenu=models.TextField(null=True)
    costomenu=models.FloatField()
    activo=models.BooleanField(default=True)
    id_plato=models.IntegerField()

    class Meta:
        verbose_name = "cartamenu"
        verbose_name_plural = "cartamenus"
        ordering = ['id_plato']
        

    def __str__(self):
        return self.nombremenu

class CartaMenu_enFila(models.Model):
    nombremenu=models.CharField(max_length=50)
    costomenu=models.FloatField()
    id_plato=models.IntegerField()
    tipofamilia=models.ForeignKey(FamiliaMenu, on_delete=models.PROTECT)
    fotomenu=models.ImageField(upload_to='administracion', null=True, blank=True)
    detallemenu=models.TextField(null=True)
    juvenil=models.BooleanField(null=True)
    mayor=models.BooleanField(null=True)
    normal=models.BooleanField(null=True)
    celiaco=models.BooleanField(null=True)
    vegano=models.BooleanField(null=True)
    vegetariano=models.BooleanField(null=True)
    

    class Meta:
        verbose_name = "cartamenu_enfila"
        verbose_name_plural = "cartamenus_enfila"
        ordering = ['id_plato']
        

    def __str__(self):
        return self.nombremenu

class FormadePago(models.Model):
    tipopago=models.CharField(max_length=50)
    activo=models.BooleanField(default=True)

    class Meta:
        verbose_name = "FormadePago"
        verbose_name_plural = "FormadePagos"
        ordering = ['tipopago']
        

    def __str__(self):
        return self.tipopago


class Temp_FamiliaMenu(models.Model):
    id_familia=models.IntegerField()
    nombrefamilia=models.CharField(max_length=50)
    orden=models.IntegerField()
   

    class Meta:
        verbose_name = "Temp_FamiliaMenu"
        verbose_name_plural = "Temp_FamiliaMenus"
        ordering = ['orden']
        

    def __str__(self):
        return self.nombrefamilia


