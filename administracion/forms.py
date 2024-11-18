from django import forms

from usuarios.models import Cliente2,Contrato2,Tarjeta,ServicioAdicional,Pagos2,ActualizacionContrato2,DetalleGastos
from administracion.models import CartaMenu, CartaMenu_enFila

class GenerarFormCliente(forms.ModelForm):
    class Meta:
        model = Cliente2
        fields = ['nombrecliente','numcliente','fecha_nacimiento','sexo','foto','ciudad','provincia','direccion','tipodocunento', 'numdocumento']
        labels = {'nombrecliente' : 'Nombre del Cliente','numcliente' : 'Num de Cliente','fecha_nacimiento' : 'Fecha de Nacimiento','tipodocunento' : 'Tipo de Docunento', 'numdocumento' : 'Num de Documento'}
        widgets = {'fecha_nacimiento': forms.DateInput(attrs={'type':'date'})}
        

class GenerarFormClienteRegistrado(forms.ModelForm):
    class Meta:
        model = Cliente2
        fields = ['nombrecliente','numcliente','fecha_nacimiento','sexo','foto','ciudad','provincia','direccion','tipodocunento', 'numdocumento']
        labels = {'nombrecliente' : 'Nombre del Cliente','numcliente' : 'Num de Cliente','fecha_nacimiento' : 'Fecha de Nacimiento','tipodocunento' : 'Tipo de Docunento', 'numdocumento' : 'Num de Documento'}
        #widgets = {'foto': forms.FileInput(attrs={'class':'form-control', 'name': 'foto' })}     


class GenerarFormContrato(forms.ModelForm):
    class Meta:
        model = Contrato2
        fields = ['cliente','ident_comtrato','fechaevento','tipoevento','fotocontrato']
        labels = {'ident_comtrato': 'Identificacion del Contrato','fechaevento':'Fecha del Evento','tipoevento':'Tipo de Evento','fotocontrato':'Foto del Contrato'}
        widgets = {'fechaevento': forms.DateInput(attrs={'type':'date'}),'cliente':forms.HiddenInput}

class GenerarFormContratoRegistrado(forms.ModelForm):
    class Meta:
        model = Contrato2
       
        fields = ['ident_comtrato','fechaevento','tipoevento','estadoevento','estadopago','fotocontrato','montooriginal','montoactualizado','saldopendiente','TarjetasPendientes','Valortarj_actualizado']
        labels = {'ident_comtrato': 'Identificacion del Contrato','fechaevento':'Fecha del Evento','estadoevento':'Estado del Evento','estadopago':'Estado del Pago','tipoevento':'Tipo de Evento','fotocontrato':'Foto del Contrato','montooriginal':'Monto','montoactualizado':'Monto Actualizado','saldopendiente':'Saldo Pendiente','TarjetasPendientes':'Tarjetas Pendientes','Valortarj_actualizado':'Valor Actualizado de Tarjeta'}
        widgets = {'ident_comtrato': forms.TextInput(attrs={'readonly':'readonly'}),
        'fechaevento': forms.DateInput(attrs={'class':'form-control','type':'date'}),
        'estadoevento': forms.TextInput(attrs={'readonly':'readonly'}),
        'estadopago': forms.TextInput(attrs={'readonly':'readonly'}),
        'montooriginal': forms.TextInput(attrs={'readonly':'readonly'}),
        'montoactualizado': forms.TextInput(attrs={'readonly':'readonly'}),
        'saldopendiente': forms.TextInput(attrs={'readonly':'readonly'}),
        'TarjetasPendientes':forms.TextInput(attrs={'readonly':'readonly'}),
        'Valortarj_actualizado':forms.TextInput(attrs={'readonly':'readonly'})
        }


class GenerarFormTarjeta(forms.ModelForm):
    class Meta:
        model = Tarjeta
        fields = ['contrato','cliente','cant_tarjetas','tipodemenu','modalidaddelmenu']
        labels = {'cant_tarjetas': 'Cantidad de Tarjetas','tipodemenu':'Tipo de Menu','modalidaddelmenu':'Modalidad'}
        widgets = {'contrato':forms.HiddenInput,'cliente':forms.HiddenInput}

#class GenerarFormServicioShow(forms.Form):
   
#        id_contrato=forms.IntegerField(widget=(forms.HiddenInput))
#        id_familiamenu=forms.IntegerField(widget=(forms.HiddenInput))
#        costo_item=forms.FloatField(label='Ingrese el Costo')
#        detalleservicio=forms.CharField(label='Describa el tipo de Servicio',widget=forms.Textarea(attrs={"rows":7, "cols":20}))
        

class GenerarFormServicio(forms.ModelForm):
    class Meta:
        model = ServicioAdicional
        fields = ['costo_item','detalleservicio']
        labels = {'costo_item':'Ingrese el Costo','detalleservicio':'Describa el tipo de Servicio'}
        widgets = {'detalleservicio': forms.Textarea(attrs={"rows":7, "cols":20})}


class GenerarFormPagos(forms.ModelForm):
    class Meta:
        model = Pagos2
        fields = ['cliente','contrato','costo_tarjeta','tarjetas_pend','deuda_a_la_fecha','ident_pago','formadepago','fechapago','monto','numcomprobante','imagencomprobante']
        labels = {'ident_pago':'Identificacion del Pago','formadepago':'Forma de Pago','fechapago':'Fecha del Pago','monto':'Monto Pagado','numcomprobante':'Num. de Comprobante','imagencomprobante':'Foto del Comprobante'}
        widgets = {'contrato':forms.HiddenInput,'cliente':forms.HiddenInput,'costo_tarjeta':forms.HiddenInput,'tarjetas_pend':forms.HiddenInput,'deuda_a_la_fecha':forms.HiddenInput,
        'fechapago': forms.DateInput(attrs={'type':'date'})}

       
class GenerarFormPagosUpdate(forms.ModelForm):
    class Meta:
        model = Pagos2
        fields = ['cliente','contrato','costo_tarjeta','tarjetas_pend','deuda_a_la_fecha','ident_pago','formadepago','fechapago','monto','numcomprobante','imagencomprobante']
        labels = {'ident_pago':'Identificacion del Pago','formadepago':'Forma de Pago','fechapago':'Fecha del Pago','monto':'Monto Pagado','numcomprobante':'Num. de Comprobante','imagencomprobante':'Foto del Comprobante'}
        widgets = {'contrato':forms.HiddenInput,'cliente':forms.HiddenInput,'costo_tarjeta':forms.HiddenInput,'tarjetas_pend':forms.HiddenInput,'deuda_a_la_fecha':forms.HiddenInput,
        'fechapago': forms.DateInput()}
        

class GenerarFormActualizacion(forms.ModelForm):
    class Meta:
        model = ActualizacionContrato2
        fields = ['cliente','contrato','saldopendiente','fechaactualizacion','porcentaje']
        labels = {'saldopendiente':'Saldo Pendiente','fechaactualizacion':'Fecha de Actualizacion','Porcentaje':'Porcentaje'}
        widgets = {'contrato':forms.HiddenInput,'cliente':forms.HiddenInput,
                'fechaactualizacion': forms.DateInput(attrs={'type':'date'}),
                'saldopendiente': forms.TextInput(attrs={'readonly':'readonly'})}


class GenerarFormActualizacionUpdates(forms.ModelForm):
    class Meta:
        model = ActualizacionContrato2
        fields = ['cliente','contrato','saldopendiente','fechaactualizacion','porcentaje']
        labels = {'saldopendiente':'Saldo Pendiente','fechaactualizacion':'Fecha de Actualizacion','Porcentaje':'Porcentaje'}
        widgets = {'contrato':forms.HiddenInput,'cliente':forms.HiddenInput,
                'fechaactualizacion': forms.DateInput(),
                'saldopendiente': forms.TextInput(attrs={'readonly':'readonly'})}


class GenerarFormGastos(forms.ModelForm):
    class Meta:
        model = DetalleGastos
        fields = {'cliente','contrato','familiamenu','proveedor','numfactura','fechagasto','montogasto','formadepago','fechapago','detallecompra'}
        labels = {'familiamenu':'Tipo de Menu','proveedor':'Nombre Proveedor','numfactura': 'Numero de Factura','fechagasto': 'Fecha del Gasto' ,'montogasto':'Monto Gastado','formadepago': 'Forma de Pago','fechapago':'Fecha de Pago','detallecompra':'Detalle de la Compra'}
        widgets = {'contrato':forms.HiddenInput,'cliente':forms.HiddenInput,
                    'fechagasto': forms.DateInput(attrs={'type':'date'}),
                    'fechapago': forms.DateInput(attrs={'type':'date'}),
                    'detallecompra': forms.Textarea(attrs={"rows":7, "cols":20})}

class GenerarFormGastosUpdate(forms.ModelForm):
    class Meta:
        model = DetalleGastos
        fields = {'cliente','contrato','familiamenu','proveedor','numfactura','fechagasto','montogasto','formadepago','fechapago','detallecompra'}
        labels = {'familiamenu':'Tipo de Menu','proveedor':'Nombre Proveedor','numfactura': 'Numero de Factura','fechagasto': 'Fecha del Gasto' ,'montogasto':'Monto Gastado','formadepago': 'Forma de Pago','fechapago':'Fecha de Pago','detallecompra':'Detalle de la Compra'}
        widgets = {'contrato':forms.HiddenInput,'cliente':forms.HiddenInput,
                    'fechagasto': forms.DateInput(),
                    'fechapago': forms.DateInput(),
                    'detallecompra': forms.Textarea(attrs={"rows":7, "cols":20})}

class GenerarFormMenuUpdate(forms.ModelForm):
    class Meta:
        model = CartaMenu_enFila
        fields = {'nombremenu','costomenu','tipofamilia','fotomenu','detallemenu','juvenil','mayor','normal','celiaco','vegano','vegetariano'}
        labels = {'nombremenu': 'Nombre del Menu','costomenu':'Costo del Menu','tipofamilia':'Tipo de Menu','fotomenu':'Foto','detallemenu':'Descripción','juvenil': 'Menu Juvenil','mayor': 'Menu de Mayores','normal':'Menu Normal','celiaco':'Menu Celiaco','vegano':'Menu Vegano','vegetariano':'Menu Vejetariano'}
        widgets = {'juvenil':forms.CheckboxInput() ,
                    'mayor':forms.CheckboxInput(),
                    'normal':forms.CheckboxInput(),
                    'celiaco':forms.CheckboxInput(),
                    'vegano':forms.CheckboxInput(),
                    'vegetariano':forms.CheckboxInput(),
                    'detallemenu': forms.Textarea(attrs={"rows":7, "cols":20})
                    }