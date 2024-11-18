from django.db import models
from django.contrib.auth.models import User #Importa los usuarios
from servicios.models import Servicio
from django.db.models import F
from administracion.models import CartaMenu,FamiliaMenu,TipoMenu,ModalidadMenu,FormadePago


# Create your models here.

class Cliente2(models.Model):
    
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    nombrecliente=models.CharField(max_length=50, null=True)
    numcliente= models.IntegerField()
    fecha_nacimiento=models.DateField(null=True)
    sexo=models.CharField(max_length=15)
    foto=models.ImageField(upload_to='usuarios', null=True, blank=True)
    ciudad=models.CharField(max_length=50)
    provincia=models.CharField(max_length=50)
    direccion=models.CharField(max_length=50)
    tipodocunento=models.CharField(max_length=5)
    numdocumento=models.BigIntegerField()
    

    class Meta:
        ordering = ["nombrecliente"]
        verbose_name="Cliente"
        verbose_name_plural="Clientes"
        unique_together = ["user"]

    def __str__(self):
        return self.nombrecliente

class Contrato2(models.Model):
    ident_comtrato=models.CharField(max_length=50) 
    cliente= models.ForeignKey(Cliente2, on_delete=models.CASCADE)
    fechaevento=models.DateTimeField(null=True)
    tipoevento=models.ManyToManyField(Servicio)
    estadoevento=models.CharField(max_length=15, default="pendiente")
    estadopago=models.CharField(max_length=15, default="pendiente")
    fotocontrato=models.ImageField(upload_to='usuarios', null=True, blank=True)
    montooriginal=models.FloatField(null=True)
    montoactualizado=models.FloatField(null=True)
    saldopendiente=models.FloatField(null=True)
    TarjetasPendientes=models.FloatField(null=True)
    Valortarj_actualizado=models.FloatField(null=True)
    cant_tarj_contratadas=models.IntegerField(null=True)
    TarjetasPagadas=models.FloatField(null=True)
    TotalGastos=models.FloatField(null=True)
    Diferencia=models.FloatField(null=True)
    porcentaje=models.FloatField(null=True)

    class Meta:
        ordering = ["cliente_id","id"]
        verbose_name="Contrato"
        verbose_name_plural="Contratos"

    def __str__(self):
        return f'{self.cliente} -- {self.ident_comtrato}'
    
class Pagos2(models.Model):
    ident_pago=models.CharField(max_length=50)
    cliente= models.ForeignKey(Cliente2, on_delete=models.CASCADE)
    contrato=models.ForeignKey(Contrato2, on_delete=models.CASCADE)
    fechapago=models.DateTimeField()
    monto=models.FloatField()
    formadepago=models.ForeignKey(FormadePago, on_delete=models.PROTECT)
    numcomprobante=models.IntegerField(null=True)
    imagencomprobante=models.ImageField(upload_to='usuarios', null=True, blank=True)
    costo_tarjeta=models.FloatField(null=True)
    tarjetas_pend=models.FloatField(null=True)
    deuda_a_la_fecha= models.FloatField(null=True)

    class Meta:
        ordering = ["cliente_id","contrato_id","id"]
        verbose_name="Pagos"
        verbose_name_plural="Pagos"

    def __str__(self):
        return f'{self.contrato.cliente} -- {self.contrato.fechaevento} -- {self.ident_pago}'

class SumaContrato2(models.Model):
    contrato=models.ForeignKey(Contrato2, on_delete=models.CASCADE)
    cliente= models.ForeignKey(Cliente2, on_delete=models.CASCADE)
    monto=models.FloatField(null=True)

    class Meta:
        verbose_name="SumaContrato"
        verbose_name_plural="SumaContratos"

    def __str__(self):
        return f'{self.contrato}'

class ActualizacionContrato2(models.Model):
    contrato=models.ForeignKey(Contrato2, on_delete=models.CASCADE)
    saldopendiente=models.FloatField()
    fechaactualizacion=models.DateTimeField(null=True)
    porcentaje=models.FloatField()
    incremento=models.FloatField()
    aplicado=models.BooleanField(default=False)
    cliente= models.ForeignKey(Cliente2, on_delete=models.CASCADE)

    class Meta:
        ordering = ["cliente_id","contrato_id","id"]
        verbose_name="ActualizacionContrato"
        verbose_name_plural="ActualizacionContratos"

    def __str__(self):
        return f'{self.contrato}'

class SumaActualizacion2(models.Model):
    contrato=models.ForeignKey(Contrato2, on_delete=models.CASCADE)
    cliente= models.ForeignKey(Cliente2, on_delete=models.CASCADE)
    monto=models.FloatField()

    class Meta:
        verbose_name="SumaActualizacion"
        verbose_name_plural="SumaActualizacions"

    def __str__(self):
        return f'{self.contrato}'


class Tarjeta(models.Model):
    contrato=models.ForeignKey(Contrato2, on_delete=models.CASCADE)
    cliente= models.ForeignKey(Cliente2, on_delete=models.CASCADE)
    tipodemenu=models.ForeignKey(TipoMenu, on_delete=models.PROTECT)
    modalidaddelmenu=models.ForeignKey(ModalidadMenu, on_delete=models.PROTECT)
    cant_tarjetas=models.IntegerField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)
    costo_tarjeta=models.FloatField(default=0)
    
    class Meta:
        ordering = ["contrato_id","id"]
        verbose_name="Tarjeta"
        verbose_name_plural="Tarjetas"

    def __str__(self):
        return f'{self.contrato}'

class Menu(models.Model):
    id_contrato=models.ForeignKey(Contrato2, on_delete=models.CASCADE)
    id_tarjeta=models.ForeignKey(Tarjeta, on_delete=models.CASCADE)
    id_familiamenu=models.ForeignKey(FamiliaMenu, on_delete=models.PROTECT)
    id_item=models.ForeignKey(CartaMenu, on_delete=models.PROTECT)
    costo_item=models.FloatField()

    class Meta:
        ordering = ["id_contrato_id","id_tarjeta_id"]
        verbose_name="Menu"
        verbose_name_plural="Menus"

    def __str__(self):
        return f'{self.id_contrato}'

class ServicioContratado(models.Model):
    id_contrato=models.ForeignKey(Contrato2, on_delete=models.CASCADE)
    id_familiamenu=models.ForeignKey(FamiliaMenu, on_delete=models.PROTECT)
    id_item=models.ForeignKey(CartaMenu, on_delete=models.PROTECT)
    costo_item=models.FloatField()

    class Meta:
        ordering = ["id_contrato_id"]
        verbose_name="ServicioContratado"
        verbose_name_plural="ServicioContratados"

    def __str__(self):
        return f'{self.id_contrato}'


class ServicioAdicional(models.Model):
    id_contrato=models.ForeignKey(Contrato2, on_delete=models.CASCADE)
    id_familiamenu=models.ForeignKey(FamiliaMenu, on_delete=models.PROTECT)
    costo_item=models.FloatField()
    detalleservicio=models.TextField(null=True)

    class Meta:
        ordering = ["id_contrato_id"]
        verbose_name="ServicioAdicional"
        verbose_name_plural="ServiciosAdicionales"

    def __str__(self):
        return f'{self.id_contrato}'


class TotalContrato(models.Model):
    id_contrato=models.ForeignKey(Contrato2, on_delete=models.CASCADE)
    cant_tarjetas=models.IntegerField()
    costo_tarjeta=models.FloatField()
    tot_tarjetas=models.FloatField()
    tot_comunes=models.FloatField()
    tot_adicionales=models.FloatField()
    tot_logistica=models.FloatField()
    tot_contrato=models.FloatField()

    class Meta:
        ordering = ["id_contrato_id"]
        verbose_name="TotalContrato"
        verbose_name_plural="TotalContratos"

    def __str__(self):
        return f'{self.id_contrato}'

class ControlTarjetas(models.Model):
    contrato=models.ForeignKey(Contrato2, on_delete=models.CASCADE)
    cliente=models.ForeignKey(Cliente2, on_delete=models.CASCADE) 
    pago_id=models.ForeignKey(Pagos2, on_delete=models.CASCADE)
    cant_tarjetas_pagas=models.FloatField()
    cant_tarjetas_pendientes=models.FloatField()
    costo_tarjeta_actualizado=models.FloatField()

    class Meta:
        ordering = ["cliente_id","contrato_id","pago_id"]
        verbose_name="ControlTarjeta"
        verbose_name_plural="ControlTarjetas"

    def __str__(self):
        return f'{self.cliente} -- {self.contrato}'

class Proveedor(models.Model):
    razonsocial=models.TextField()
    direccion=models.TextField(null=True)
    CUIT=models.TextField(null=True)

    class Meta:
        ordering = ["razonsocial"]
        verbose_name="Proveedor"
        verbose_name_plural="Proveedores"

    def __str__(self):
        return f'{self.razonsocial}'
        

class DetalleGastos(models.Model):
    cliente=models.ForeignKey(Cliente2, on_delete=models.CASCADE)
    contrato=models.ForeignKey(Contrato2, on_delete=models.CASCADE)
    familiamenu=models.ForeignKey(FamiliaMenu, on_delete=models.PROTECT)
    proveedor=models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    numfactura=models.IntegerField(null=True)
    fechagasto=models.DateTimeField()
    montogasto=models.FloatField()
    formadepago=models.ForeignKey(FormadePago, on_delete=models.PROTECT)
    fechapago=models.DateTimeField()
    detallecompra=models.TextField()

    class Meta:
        ordering = ["cliente_id","contrato_id","familiamenu_id"]
        verbose_name="DetalleGasto"
        verbose_name_plural="DetalleGastos"

    def __str__(self):
        return f'{self.cliente} -- {self.contrato}'
        

class TotalGastos(models.Model):
    cliente=models.ForeignKey(Cliente2, on_delete=models.CASCADE)
    contrato=models.ForeignKey(Contrato2, on_delete=models.CASCADE)
    familiamenu=models.ForeignKey(FamiliaMenu, on_delete=models.PROTECT)
    montogasto=models.FloatField(null=True)
    montoingreso=models.FloatField(null=True)
    diferencia=models.FloatField(null=True)
    porcentaje=models.FloatField(null=True)

    class Meta:
        ordering = ["cliente_id","contrato_id","familiamenu_id"]
        verbose_name="TotalGasto"
        verbose_name_plural="TotalGastos"

    def __str__(self):
        return f'{self.cliente} -- {self.contrato}'

class SumaGastos(models.Model):
    cliente=models.ForeignKey(Cliente2, on_delete=models.CASCADE)
    contrato=models.ForeignKey(Contrato2, on_delete=models.CASCADE)
    totalgastos=models.FloatField()

    class Meta:
        ordering = ["cliente_id","contrato_id"]
        verbose_name="SumaGasto"
        verbose_name_plural="SumaGastos"

    def __str__(self):
        return f'{self.cliente} -- {self.contrato}'





    
