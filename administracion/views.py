from django.db.models import Count,Max
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.humanize.templatetags.humanize import intcomma
from django.db import connection, transaction

from administracion.models import Tablas, Usuarioregistrado,CartaMenu,TipoMenu,ModalidadMenu,FamiliaMenu,CartaMenu_enFila
from usuarios.models import Cliente2,Contrato2,Tarjeta,Menu,ServicioContratado,ServicioAdicional,TotalContrato,Pagos2,ActualizacionContrato2,ControlTarjetas,TotalGastos,DetalleGastos,Proveedor,SumaGastos
from django.contrib.auth.models import User
from django.views.generic import View
from django.contrib import messages
from autenticacion.forms import GenerarFormRegistracion
from .forms import GenerarFormCliente,GenerarFormClienteRegistrado,GenerarFormContrato,GenerarFormContratoRegistrado,GenerarFormTarjeta,GenerarFormServicio,GenerarFormPagos,GenerarFormPagosUpdate,GenerarFormActualizacion,GenerarFormActualizacionUpdates,GenerarFormGastos,GenerarFormGastosUpdate,GenerarFormMenuUpdate
from usuarios.views import Actualizacion
from datetime import datetime

# Create your views here.

class Registrar(View):

    def get(self, request):
        Sect = Tablas.objects.all()
        form = GenerarFormRegistracion()
        return render(request, "administracion/usuarios.html", {"form": form, "Sector": Sect})

    def post(self, request):

        Sect = Tablas.objects.all()
        form = GenerarFormRegistracion(request.POST)

        if form.is_valid():

            form.save()

            nombre = request.POST.get("username")
            passw = request.POST.get("password1")
            correo = request.POST.get("email")
            tabla = "usuario"

            Usu = User.objects.get(username=nombre, email=correo)

            usuario = list()

            usuario.append(Usuarioregistrado(
                usuario_id=Usu.id,
                nombreusuario=nombre,
                mailusuario=correo,
                passwordusuario=passw,
            ))

            Usuarioregistrado.objects.bulk_create(usuario)

            return render(request, 'administracion/administracion.html', {"Sector": Sect, "Tabla": tabla, "Nombre": nombre, "Pass": passw, "Correo": correo})

        else:
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])

            return render(request, "administracion/usuarios.html", {"form": form, "Sector": Sect})


def administracion(request):

    Sect = Tablas.objects.all()

    tabla = "vacia"

    return render(request, 'administracion/administracion.html', {"Sector": Sect, "Tabla": tabla})


def admincliente(request):
    Sect = Tablas.objects.all()
    Cli = Cliente2.objects.all()
    clientes = Cliente2.objects.all().values('user_id')
   



    usu_suelto = Usuarioregistrado.objects.exclude(usuario_id__in = clientes)


    return render(request, 'administracion/cliente.html', {"Sector": Sect, "Usuarios": usu_suelto, "Clientes": Cli})


def get_usuarios(_request):
    usuarios = list(Usuarioregistrado.objects.values())

    if (len(usuarios) > 0):
        data = {'messages': 'Satisfactorio', 'usuarios': usuarios}
    else:
        data = {'messages': 'No Encontrado'}

    return JsonResponse(data)


def get_cliente(request, categoria_id):
    clientes = list(Cliente2.objects.filter(user_id=categoria_id).values())

    if (len(clientes) > 0):
        data = {'messages': 'Satisfactorio', 'usuarios': clientes}
    else:
        data = {'messages': 'No Encontrado'}

    return JsonResponse(data)


def admincontratos(request):

    Sect = Tablas.objects.all()
    Cli = Cliente2.objects.all().order_by('nombrecliente')
    
    contratos = Contrato2.objects.all().values('cliente_id')
    Contrato=Contrato2.objects.all().select_related("cliente").order_by('cliente','ident_comtrato') #Trae los datos de Contrato2 para cada registro de Clientes2
   



    usu_suelto = Cliente2.objects.exclude(id__in = contratos).order_by('nombrecliente')


    return render(request, 'administracion/contratos.html', {"Sector": Sect, "Usuarios": usu_suelto, "Clientes": Cli, "Contratos": Contrato})


def admintarjetas(request):
    Sect = Tablas.objects.all()
    Contrato = Contrato2.objects.filter(estadoevento='pendiente')

    return render(request, 'administracion/tarjetas.html', {"Sector": Sect, "Contratos": Contrato})


def adminpagos(request):

    Sect = Tablas.objects.all()
    Contrato = Contrato2.objects.filter(estadoevento='pendiente',saldopendiente__gt=0) # significa mayor que 0
    
    return render(request, 'administracion/pagos.html', {"Sector": Sect, "Contratos": Contrato})


def adminactualizacion(request):

    Sect = Tablas.objects.all()
    Contrato = Contrato2.objects.filter(estadoevento='pendiente',saldopendiente__gt=0) # significa mayor que 0

    return render(request, 'administracion/actualizacion.html', {"Sector": Sect, "Contratos": Contrato})

def admingastos(request):

    Sect = Tablas.objects.all()
    Contrato = Contrato2.objects.filter(estadoevento='pendiente',saldopendiente__gt=0) # significa mayor que 0

    return render(request, 'administracion/gastos.html', {"Sector": Sect, "Contratos": Contrato})


def adminmenu(request):
    Sect = Tablas.objects.all()
    Familia = FamiliaMenu.objects.filter(orden__lte='8').order_by('orden')
    
    return render(request, 'administracion/cartamenu.html', {"Sector": Sect, "Familia": Familia})


def adminusuario(request):

    Sect = Tablas.objects.all()

    return render(request, 'administracion/usuarios.html', {"Sector": Sect})


def formcliente(request, categoria_id):

    if request.method == "POST":
        Usu = Usuarioregistrado.objects.all()
        Sect = Tablas.objects.all()
        
        Cli = Cliente2.objects.filter(user_id=categoria_id)
        

        if Cli:

            Cli2 = Cliente2.objects.get(user_id=categoria_id)                
            form = GenerarFormCliente(request.POST,request.FILES, instance=Cli2)
            if form.is_valid():
                                
                nombrecliente2=form.cleaned_data.get("nombrecliente")
                numcliente2=form.cleaned_data.get("numcliente")
                fecha_nacimiento2=form.cleaned_data.get("fecha_nacimiento")
                sexo2=form.cleaned_data.get("sexo")
                foto2=form.cleaned_data.get("foto")
                ciudad2=form.cleaned_data.get("ciudad")
                provincia2=form.cleaned_data.get("provincia")
                direccion2=form.cleaned_data.get("direccion")
                tipodocunento2=form.cleaned_data.get("tipodocunento")
                numdocumento2=form.cleaned_data.get("numdocumento")

                                
                form.save()

                #Cliente2.objects.filter(id=categoria_id).update(nombrecliente=nombrecliente2,numcliente=numcliente2,fecha_nacimiento=fecha_nacimiento2,sexo=sexo2,foto=foto2,ciudad=ciudad2,provincia=provincia2,direccion=direccion2,tipodocunento=tipodocunento2,numdocumento=numdocumento2)
            
            return render(request, 'administracion/formcliente.html', {"form": form, "Sector": Sect,"Foto":foto2})
        
        else:
            form = GenerarFormCliente(request.POST,request.FILES)
            if form.is_valid():
                
                nombrecliente2=form.cleaned_data.get("nombrecliente")
                numcliente2=form.cleaned_data.get("numcliente")
                fecha_nacimiento2=form.cleaned_data.get("fecha_nacimiento")
                sexo2=form.cleaned_data.get("sexo")
                foto2=form.cleaned_data.get("foto")
                ciudad2=form.cleaned_data.get("ciudad")
                provincia2=form.cleaned_data.get("provincia")
                direccion2=form.cleaned_data.get("direccion")
                tipodocunento2=form.cleaned_data.get("tipodocunento")
                numdocumento2=form.cleaned_data.get("numdocumento")
                
                

                cliente=list()
                cliente.append(Cliente2(
                id=categoria_id,
                user_id=categoria_id,
                nombrecliente=nombrecliente2,
                numcliente=numcliente2,
                fecha_nacimiento=fecha_nacimiento2,
                sexo=sexo2,
                foto=foto2,
                ciudad=ciudad2,
                provincia=provincia2,
                direccion=direccion2,
                tipodocunento=tipodocunento2,
                numdocumento=numdocumento2
                ))

        

                Cliente2.objects.bulk_create(cliente)
            
            return redirect("admincliente")
            
    
    else:
        
        Sect = Tablas.objects.all()
        Cli = Cliente2.objects.filter(user_id=categoria_id)
       

        if Cli:
            for Clien in Cli:
                nombrecliente = Clien.nombrecliente
                numcliente=Clien.numcliente
                fecha_nacimiento=formatofecha(Clien.fecha_nacimiento)
                sexo=Clien.sexo
                foto=Clien.foto
                ciudad=Clien.ciudad
                provincia=Clien.provincia
                direccion=Clien.direccion
                tipodocunento=Clien.tipodocunento
                numdocumento=Clien.numdocumento
                
                initial_data = {'nombrecliente': nombrecliente,'numcliente':numcliente,'fecha_nacimiento':fecha_nacimiento,'sexo':sexo,'foto':foto,'ciudad':ciudad,'provincia':provincia,'direccion':direccion,'tipodocunento':tipodocunento,'numdocumento':numdocumento}
            
            form = GenerarFormCliente(initial=initial_data)
            return render(request, 'administracion/formcliente.html', {"form": form, "Sector": Sect,"Cliente": Cli})
        else:
            
                        
            form = GenerarFormCliente()
            return render(request, 'administracion/formcliente.html', {"form": form, "Sector": Sect})


def formcontrato(request, categoria_id):

    Sect = Tablas.objects.all()
    Cli = Cliente2.objects.filter(user_id=categoria_id)
       

    if request.method == "POST":
        form = GenerarFormContrato(request.POST,request.FILES)
        if form.is_valid():

            cliente2=form.cleaned_data.get("cliente")    
            ident_comtrato2=form.cleaned_data.get("ident_comtrato")
            #tipoevento2=form.cleaned_data.get("tipoevento")
            #fechaevento2=form.cleaned_data.get("fechaevento")
            montooriginal2=form.cleaned_data.get("montooriginal")
            #fotocontrato2=form.cleaned_data.get("fotocontrato")
            
            form.save()              



        
            Contrato2.objects.filter(cliente_id=cliente2,ident_comtrato=ident_comtrato2).update(montoactualizado=montooriginal2,saldopendiente=montooriginal2)
           # Contrato2.objects.bulk_create(contrato)
            
            return redirect("/administracion/admincontratos/")

    else:
        initial_data = {'cliente': categoria_id}
        form = GenerarFormContrato(initial=initial_data)
        return render(request, 'administracion/formcontrato.html', {"form": form, "Sector": Sect,"Cliente":Cli})



def formcontratoregistrado(request, categoria_id):

    Sect = Tablas.objects.all()
    Contrato = Contrato2.objects.filter(id=categoria_id)

    if Contrato:
        for Con in Contrato:
            Cli_id = Con.cliente.pk
            ident_comtrato=Con.ident_comtrato 
                    
            fechaevento=formatofecha(Con.fechaevento)
                        
            tipoevento=Con.tipoevento.select_related()
            estadoevento=Con.estadoevento
            estadopago=Con.estadopago
            fotocontrato=Con.fotocontrato
            montooriginal= Con.montooriginal
            montoactualizado=Con.montoactualizado
            saldopendiente=Con.saldopendiente
            TarjetasPendientes=Con.TarjetasPendientes
            Valortarj_actualizado=Con.Valortarj_actualizado
         
        if montooriginal is not None:
            montooriginal=round(montooriginal)
            montooriginal=intcomma(montooriginal)
        else:
            montooriginal=0
        
        if montoactualizado is not None:
            montoactualizado=round(montoactualizado)
            montoactualizado=intcomma(montoactualizado)
        else:
            montoactualizado=0
        
        if saldopendiente is not None:
            saldopendiente=round(saldopendiente)
            saldopendiente=intcomma(saldopendiente)
        else:
            saldopendiente=0
        
        if Valortarj_actualizado is not None:
            Valortarj_actualizado=round(Valortarj_actualizado)
            Valortarj_actualizado=intcomma(Valortarj_actualizado)
        else:
            Valortarj_actualizado=0
        
        if TarjetasPendientes is not None:
            TarjetasPendientes=round(TarjetasPendientes,1)
        else:
            TarjetasPendientes=0
        
     

        Cli = Cliente2.objects.filter(user_id=Cli_id)   


        if request.method == "POST":
            
            Cli2 = Contrato2.objects.get(id=categoria_id)                
            form = GenerarFormContratoRegistrado(request.POST,request.FILES, instance=Cli2)
            
            
            if form.is_valid():

                                       
                form.save()              


               
                           
            return redirect("/administracion/formcontratoregistrado/"+str(categoria_id))
            
        
            
            
        #initial_data = {'ident_comtrato':ident_comtrato,'fechaevento':fechaevento,'tipoevento':tipoevento.select_for_update(),'estadoevento':estadoevento,'estadopago':estadopago,'fotocontrato':fotocontrato,'montooriginal':montooriginal,'montoactualizado':montoactualizado,'saldopendiente':saldopendiente,'TarjetasPendientes':TarjetasPendientes,'Valortarj_actualizado':Valortarj_actualizado}
        initial_data = {'ident_comtrato':ident_comtrato,'fechaevento':fechaevento,'tipoevento':tipoevento,'estadoevento':estadoevento,'estadopago':estadopago,'fotocontrato':fotocontrato,'montooriginal':montooriginal,'montoactualizado':montoactualizado,'saldopendiente':saldopendiente,'TarjetasPendientes':TarjetasPendientes,'Valortarj_actualizado':Valortarj_actualizado}
        #initial_data = {'ident_comtrato':ident_comtrato,'fechaevento':fechaevento,'tipoevento':tipoevento}
        form = GenerarFormContratoRegistrado(initial=initial_data)
        #form = GenerarFormContratoRegistrado()
        return render(request, 'administracion/formcontratoregistrado.html', {"form": form, "Sector": Sect,"Cliente":Cli})

    else:
        return redirect("/administracion/admincontratos/")



def formatofecha(fecha):
    
    Ano=fecha.year
    Mes=fecha.month
    Dia=fecha.day
    if Mes < 10:
        Mes = '0'+str(Mes)
    if Dia < 10:
        Dia = '0'+str(Dia)

            
            
    Fecha=str(Ano)+'-'+str(Mes)+'-'+str(Dia)

    return Fecha
    
    

def formtarjetas(request, categoria_id):
    
    Sect = Tablas.objects.all()
    Contrato = Contrato2.objects.filter(id= categoria_id)
    
    if Contrato:
        for Con in Contrato:
            Cli_id = Con.cliente.pk
            Con_id = Con.pk
            

        Cli = Cliente2.objects.filter(user_id=Cli_id)
        
        tarjeta= Tarjeta.objects.filter(contrato_id= categoria_id)
        
        CartaMesaDulce = CartaMenu.objects.filter(tipofamilia_id=4,activo=True)

        CartaMesaCaliente = CartaMenu.objects.filter(tipofamilia_id=5,activo=True)

        CartaCierre = CartaMenu.objects.filter(tipofamilia_id=6,activo=True)
        
        CartaCotillon = CartaMenu.objects.filter(tipofamilia_id=8,activo=True)
        
        ServicioExiste = ServicioContratado.objects.filter(id_contrato_id=categoria_id)

        MesaDulce = ServicioContratado.objects.filter(id_contrato_id=categoria_id,id_familiamenu_id='4').select_related("id_item")

        MesaCaliente = ServicioContratado.objects.filter(id_contrato_id=categoria_id,id_familiamenu_id='5').select_related("id_item")

        Cierre = ServicioContratado.objects.filter(id_contrato_id=categoria_id,id_familiamenu_id='6').select_related("id_item")

        Cotillon = ServicioContratado.objects.filter(id_contrato_id=categoria_id,id_familiamenu_id='8').select_related("id_item")
        
               
        if tarjeta:
            totaltarjeta = 0
            costotarjeta=0
            for Tar in tarjeta:
                costotarjeta=0
                totaltarjeta = totaltarjeta + Tar.cant_tarjetas 
                CostoMenu=Menu.objects.filter(id_tarjeta_id= Tar.pk)   
                for Cos in CostoMenu:
                    costotarjeta=costotarjeta+Cos.costo_item
                costotarjeta=costotarjeta*Tar.cant_tarjetas
                sumatarjeta=Tarjeta.objects.filter(id= Tar.pk).update(costo_tarjeta=costotarjeta)

                TotalTarjetas=Tarjeta.objects.filter(contrato_id= categoria_id)
                totaltarjetas=0
                for Tot in TotalTarjetas:
                    totaltarjetas=totaltarjetas+Tot.costo_tarjeta

            

            totalservicio=0
            costoservicio=0
            if ServicioExiste:
                for Ser in ServicioExiste:
                    totalservicio=totalservicio+Ser.costo_item
                costoservicio=totalservicio*totaltarjeta


            #Grabar la Tabla "TotalContrato" con el total del contrato

            resultado = Total_Contrato(categoria_id,Cli_id)
            
            total_contrato=TotalContrato.objects.filter(id_contrato_id=categoria_id)

            

            familiamenu=9
            servicioadicional= ServicioAdicional.objects.filter(id_contrato_id= categoria_id,id_familiamenu_id=familiamenu)
            if servicioadicional:
                for adi in servicioadicional:
                    costo=adi.costo_item
                    detalle=adi.detalleservicio
                initial_data = {'costo_item':costo,'detalleservicio':detalle}
                formshow = GenerarFormServicio(initial=initial_data)
            else:
                
                formshow = GenerarFormServicio()

            familiamenu=10
            servicioadicional= ServicioAdicional.objects.filter(id_contrato_id= categoria_id,id_familiamenu_id=familiamenu)
            if servicioadicional:
                for adi in servicioadicional:
                    costo=adi.costo_item
                    detalle=adi.detalleservicio
                initial_data = {'costo_item':costo,'detalleservicio':detalle}
                formlogistica = GenerarFormServicio(initial=initial_data)
            else:
               formlogistica = GenerarFormServicio()

            Contrato = Contrato2.objects.filter(id= categoria_id)
            for Con in Contrato:
                Pend = Con.TarjetasPendientes
                Valor = Con.Valortarj_actualizado
            
            tarjeta= Tarjeta.objects.filter(contrato_id= categoria_id)


            return render(request, 'administracion/formtarjetas.html', {"formShow": formshow,"formServicio": formlogistica,"Sector": Sect,"Cliente":Cli,"Con":categoria_id,"Contrato":Contrato,"Tarjeta":tarjeta,"Total":totaltarjeta,"Pend":Pend,"Valor":Valor,"TotalTarjeta":totaltarjetas,"TotalServicio":costoservicio,"TotalContrato":total_contrato,"CartaMesaDulce":CartaMesaDulce,"CartaMesaCaliente":CartaMesaCaliente,"CartaCierre":CartaCierre,"CartaCotillon":CartaCotillon,"ServicioExiste":ServicioExiste,"MesaDulce":MesaDulce,"MesaCaliente":MesaCaliente,"Cierre":Cierre,"Cotillon":Cotillon})    
        else:
            ruta="/administracion/formtarjetascreate/" + str(categoria_id)
            return redirect(ruta)
    else:
        
        return redirect("/administracion/admintarjetas/")

def formtarjetascreate(request, categoria_id):
    
    Sect = Tablas.objects.all()
    Contrato = Contrato2.objects.filter(id= categoria_id)
    
    if Contrato:
        for Con in Contrato:
            Cli_id = Con.cliente.pk

        Cli = Cliente2.objects.filter(user_id=Cli_id)

        if request.method == "POST":
            formTarjetaupdate = GenerarFormTarjeta(request.POST,request.FILES)
            if formTarjetaupdate.is_valid():

                formTarjetaupdate.save()

            ruta = "/administracion/formtarjetas/" + str(categoria_id)

            return redirect(ruta)

        else:
            initial_data_Tarjeta = {'contrato':categoria_id,'cliente':Cli_id}
            formTarjeta = GenerarFormTarjeta(initial=initial_data_Tarjeta)
        
            return render(request, 'administracion/formtarjetascreate.html', {"formTarjeta": formTarjeta,"Sector": Sect,"Cliente":Cli,"Contrato":Contrato})  


def formtarjetasupdate(request, categoria_id):
    
    Sect = Tablas.objects.all()
    tarjeta= Tarjeta.objects.filter(id= categoria_id)
    
    if tarjeta:
        for Tar in tarjeta:
            contrato = Tar.contrato.pk
            cliente = Tar.cliente.pk
            tipodemenu = Tar.tipodemenu.pk
            modalidaddelmenu = Tar.modalidaddelmenu.pk
            cant_tarjetas = Tar.cant_tarjetas

        ruta = "/administracion/formtarjetas/" + str(contrato)
        
        Contrato = Contrato2.objects.filter(id= contrato)
    
        Cli = Cliente2.objects.filter(user_id= cliente)

        if request.method == "POST":
            Tar = Tarjeta.objects.get(id=categoria_id)                
            form = GenerarFormTarjeta(request.POST,request.FILES, instance=Tar)
            
            
            if form.is_valid():

                                       
                form.save()

                menuborrado= Menu.objects.filter(id_tarjeta_id= categoria_id).delete()  
                
                
                
                return redirect(ruta)
                
            
            else:
            
                return redirect("/administracion/admintarjetas/")


        else:

            initial_data_Tarjeta = {'contrato':contrato,'cliente':cliente,'tipodemenu':tipodemenu,'modalidaddelmenu':modalidaddelmenu,'cant_tarjetas':cant_tarjetas}
            formTarjeta = GenerarFormTarjeta(initial=initial_data_Tarjeta)

            return render(request, 'administracion/formtarjetasupdate.html', {"formTarjeta": formTarjeta,"Sector": Sect,"Cliente":Cli,"Contrato":Contrato})    

    else:
        return redirect("/administracion/admintarjetas/")


def tarjetasdelete(request, categoria_id):

    Sect = Tablas.objects.all()
    tarjeta= Tarjeta.objects.filter(id= categoria_id)
    
    if tarjeta:
        for Tar in tarjeta:
            contrato = Tar.contrato.pk
            
 
        tarjeta= Tarjeta.objects.filter(id= categoria_id).delete()

                   
        ruta="/administracion/formtarjetas/" + str(contrato)
        return redirect(ruta)

    else:
        return redirect("/administracion/admintarjetas/")

def formpagos(request, categoria_id):

    Sect = Tablas.objects.all()
    contrato = Contrato2.objects.filter(id=categoria_id)
    pagos = Pagos2.objects.filter(contrato_id=categoria_id)
    
    if contrato:
        for Con in contrato:
            Cli_id = Con.cliente.pk

        Cli = Cliente2.objects.filter(id=Cli_id)
    
        totalpagos=0
        totalcomprob=0
        if pagos:
            for pag in pagos:
                totalpagos=totalpagos+pag.monto
                totalcomprob=totalcomprob+1
        
        
        return render(request, 'administracion/formpagos.html', {"Sector": Sect,"Cliente":Cli,"Contrato":contrato,"Pagos":pagos,'TotalPagos':totalpagos,'Total':totalcomprob})

    else:
        return redirect("/administracion/adminpagos/")

def formpagoscreate(request, categoria_id):
    
    Sect = Tablas.objects.all()
    Contrato = Contrato2.objects.filter(id= categoria_id)
    
    if Contrato:
        for Con in Contrato:
            Cli_id = Con.cliente.pk
            costotarjeta = Con.Valortarj_actualizado
            tarjetaspend = Con.TarjetasPendientes
            deuda = Con.saldopendiente

        Cli = Cliente2.objects.filter(user_id=Cli_id)

        if request.method == "POST":
            formTarjetaupdate = GenerarFormPagos(request.POST,request.FILES)
            if formTarjetaupdate.is_valid():

                           
                
                formTarjetaupdate.save()

                #Actualizar "ControlTarjetas" para cancelar tarjetas y actualizar pendientes
                
                actualizartarjetas = ActualizarTarjetas(categoria_id) 


                #Actualizar Contrato

                actualizar = Actualizacion(categoria_id,Cli)
           
                ruta = "/administracion/formpagos/" + str(categoria_id)

                return redirect(ruta)

            else:
                ruta = "/administracion/adminpagos/"

                return redirect(ruta)

        else:
            initial_data_Tarjeta = {'contrato':categoria_id,'cliente':Cli_id,'costo_tarjeta':costotarjeta,'tarjetas_pend':tarjetaspend,'deuda_a_la_fecha':deuda}
            formPagos = GenerarFormPagos(initial=initial_data_Tarjeta)
        
            return render(request, 'administracion/formpagoscreate.html', {"formTarjeta": formPagos,"Sector": Sect,"Cliente":Cli,"Contrato":Contrato})  

def formpagosupdate(request, categoria_id):
    
    Sect = Tablas.objects.all()
    pagos= Pagos2.objects.filter(id= categoria_id)
    
    if pagos:
        for Tar in pagos:
            id = Tar.pk
            contrato = Tar.contrato.pk
            cliente = Tar.cliente.pk
            ident_pago = Tar.ident_pago
            fechapago = Tar.fechapago
            monto = Tar.monto
            numcomprobante = Tar.numcomprobante
            imagencomprobante = Tar.imagencomprobante
            formadepago = Tar.formadepago.pk
            costotarjeta = Tar.costo_tarjeta
            tarjetaspend = Tar.tarjetas_pend
            deuda = Tar.deuda_a_la_fecha

        ruta = "/administracion/formpagos/" + str(contrato)
        
        Contrato = Contrato2.objects.filter(id= contrato)
    
        Cli = Cliente2.objects.filter(user_id= cliente)

        if request.method == "POST":
            Tar = Pagos2.objects.get(id=categoria_id)                
            form = GenerarFormPagos(request.POST,request.FILES, instance=Tar)
            
            
            if form.is_valid():

                                       
                form.save()

                
                actualizartarjetas = ActualizarTarjetas(contrato)
                
                actualizar = Actualizacion(contrato,cliente)           
                
                
                return redirect(ruta)
                
            
            else:
            
                return redirect("/administracion/adminpagos/")


        else:




            initial_data_Tarjeta = {'contrato':contrato,'cliente':cliente,'costo_tarjeta':costotarjeta,'tarjetas_pend':tarjetaspend,'deuda_a_la_fecha':deuda,'ident_pago':ident_pago,'fechapago':fechapago,'monto':monto,'numcomprobante':numcomprobante,'imagencomprobante':imagencomprobante,'formadepago':formadepago}
            formPagos = GenerarFormPagosUpdate(initial=initial_data_Tarjeta)

            return render(request, 'administracion/formpagosupdate.html', {"formTarjeta": formPagos,"Sector": Sect,"Cliente":Cli,"Contrato":Contrato})    

    else:
        return redirect("/administracion/adminpagos/")



def borrarpagos(request, categoria_id):

    pago= Pagos2.objects.filter(id= categoria_id)
    
    if pago:
        for Tar in pago:
            contrato = Tar.contrato.pk
            cliente = Tar.cliente.pk
            
 
        tarjeta= Pagos2.objects.filter(id= categoria_id).delete()

       
        actualizartarjetas = ActualizarTarjetas(contrato)
       
        actualizar = Actualizacion(contrato,cliente)           

                   
        ruta="/administracion/formpagos/" + str(contrato)
        return redirect(ruta)

    else:
        return redirect("/administracion/adminpagos/")


def formactualizaciones(request, categoria_id):

    Sect = Tablas.objects.all()
    contrato = Contrato2.objects.filter(id=categoria_id)
    actualizacion = ActualizacionContrato2.objects.filter(contrato_id=categoria_id,aplicado=True)

    
    if contrato:
        for Con in contrato:
            Cli_id = Con.cliente.pk

        Cli = Cliente2.objects.filter(id=Cli_id)
    
        totalpagos=0
        
        if actualizacion:
            for pag in actualizacion:
                totalpagos=totalpagos+pag.incremento
                
        
        
        return render(request, 'administracion/formactualizaciones.html', {"Sector": Sect,"Cliente":Cli,"Contrato":contrato,"Actualizacion":actualizacion,'TotalPagos':totalpagos})

    else:
        return redirect("/administracion/adminactualizacion/")

def formactualizacioncreate(request, categoria_id):
    
    Sect = Tablas.objects.all()
    actualizacion = ActualizacionContrato2.objects.filter(contrato_id=categoria_id,aplicado=False)

    if actualizacion:
        for Tar in actualizacion:
            id2=Tar.pk
            contrato = Tar.contrato.pk
            cliente = Tar.cliente.pk
            saldopendiente = Tar.saldopendiente
            fechaactualizacion = Tar.fechaactualizacion
            porcentaje = Tar.porcentaje
            
            saldopendiente=round(saldopendiente)

            saldopendiente=intcomma(saldopendiente)

        ruta = "/administracion/formactualizaciones/" + str(contrato)
        
        Contrato = Contrato2.objects.filter(id= contrato)
    
        Cli = Cliente2.objects.filter(user_id= cliente)

        if request.method == "POST":
            
                                      
            form = GenerarFormActualizacion(request.POST)
            
            
            if form.is_valid():

                                       
                fechaactualizacion2=form.cleaned_data.get("fechaactualizacion")
                porcentaje2=form.cleaned_data.get("porcentaje")
                saldopendiente2=form.cleaned_data.get("saldopendiente")
                incremento2=(saldopendiente2*porcentaje2)/100
                

                ActualizacionContrato2.objects.filter(id=id2).update(fechaactualizacion=fechaactualizacion2,porcentaje=porcentaje2,incremento=incremento2,aplicado=True)


                actualizar = Actualizacion(contrato,cliente)           
                
                
                return redirect(ruta)
                
            
            else:
            
                return redirect("/administracion/adminactualizacion/")


        else:




            initial_data_Tarjeta = {'contrato':contrato,'cliente':cliente,'saldopendiente':saldopendiente,'fechaactualizacion':fechaactualizacion,'porcentaje':porcentaje}
            formPagos = GenerarFormActualizacion(initial=initial_data_Tarjeta)

            return render(request, 'administracion/formactualizacionescreate.html', {"formTarjeta": formPagos,"Sector": Sect,"Cliente":Cli,"Contrato":Contrato})    

    else:
        return redirect("/administracion/adminactualizacion/")


def formactualizacionupdate(request, categoria_id):
    Sect = Tablas.objects.all()
    actualizacion = ActualizacionContrato2.objects.filter(id=categoria_id)

    if actualizacion:
        for Tar in actualizacion:
            id2=Tar.pk
            contrato = Tar.contrato.pk
            cliente = Tar.cliente.pk
            saldopendiente = Tar.saldopendiente
            fechaactualizacion = Tar.fechaactualizacion
            porcentaje = Tar.porcentaje
            incremento = Tar.incremento
    
    
        ruta = "/administracion/formactualizaciones/" + str(contrato)
        
        Contrato = Contrato2.objects.filter(id= contrato)
    
        Cli = Cliente2.objects.filter(user_id= cliente)

        if request.method == "POST":
            
                                  
            form = GenerarFormActualizacionUpdates(request.POST)
            
            
            if form.is_valid():

                                       
                fechaactualizacion2=form.cleaned_data.get("fechaactualizacion")
                porcentaje2=form.cleaned_data.get("porcentaje")
                saldopendiente2=form.cleaned_data.get("saldopendiente")
                incremento2=(saldopendiente2*porcentaje2)/100
                diferencia = incremento2 - incremento
                

                ActualizacionContrato2.objects.filter(id=id2).update(fechaactualizacion=fechaactualizacion2,porcentaje=porcentaje2,incremento=incremento2,aplicado=True)


                actualizar = AjustarActualizaciones(contrato,categoria_id,diferencia)



                actualizar = Actualizacion(contrato,cliente)           
                
                
                return redirect(ruta)
                
            
            else:
            
                return redirect("/administracion/adminactualizacion/")


        else:




            initial_data_Tarjeta = {'contrato':contrato,'cliente':cliente,'saldopendiente':saldopendiente,'fechaactualizacion':fechaactualizacion,'porcentaje':porcentaje}
            formPagos = GenerarFormActualizacionUpdates(initial=initial_data_Tarjeta)

            return render(request, 'administracion/formactualizacionescreate.html', {"formTarjeta": formPagos,"Sector": Sect,"Cliente":Cli,"Contrato":Contrato})    

    else:
        return redirect("/administracion/adminactualizacion/")



def borraractualizacion(request,categoria_id):
        pago= ActualizacionContrato2.objects.filter(id= categoria_id)
    
        if pago:
           for Tar in pago:
            contrato = Tar.contrato.pk
            cliente = Tar.cliente.pk
            incremento = Tar.incremento

            diferencia = incremento * -1
               
 
           tarjeta= ActualizacionContrato2.objects.filter(id= categoria_id).delete()


           actualizar = AjustarActualizaciones(contrato,categoria_id,diferencia)
           
           
           actualizar = Actualizacion(contrato,cliente)           

                      
           ruta="/administracion/formactualizaciones/" + str(contrato)
           return redirect(ruta)

        else:
           return redirect("/administracion/adminactualizacion/")

def formgasto(request, categoria_id):

    Sect = Tablas.objects.all()
    contrato = Contrato2.objects.filter(id=categoria_id)
    

    
    if contrato:
        for Con in contrato:
            Cli_id = Con.cliente.pk

        Cli = Cliente2.objects.filter(id=Cli_id)
    
        gastos=DetalleGastos.objects.filter(contrato_id=categoria_id,cliente_id=Cli_id).order_by('familiamenu_id')
       
        totalgasto = TotalGasto(categoria_id,Cli_id)
        
        totalgasto=TotalGastos.objects.filter(contrato_id=categoria_id,cliente_id=Cli_id).order_by('familiamenu_id')

        sumagastos=Contrato2.objects.filter(id=categoria_id,cliente_id=Cli_id)     
        

        consultaSQL = DetalleGastos.objects.raw("Select DISTINCT administracion_familiamenu.id,administracion_familiamenu.nombrefamilia from usuarios_detallegastos INNER JOIN administracion_familiamenu ON usuarios_detallegastos.familiamenu_id = administracion_familiamenu.id")

        familias=DetalleGastos.objects.filter(contrato_id=categoria_id,cliente_id=Cli_id).order_by('familiamenu_id')

                
        return render(request, 'administracion/formgasto.html', {"Sector": Sect,"Cliente":Cli,"Contrato":contrato,"DetalleGasto":gastos,"TotalGasto":totalgasto,"SumaGasto":sumagastos,"Familia":consultaSQL})     
    
    else:
        return redirect("/administracion/admingastos/")

def formgastoscreate(request, categoria_id):
    Sect = Tablas.objects.all()
    contrato = Contrato2.objects.filter(id=categoria_id)


    if contrato:
        for Con in contrato:
            Cli_id = Con.cliente.pk
            

        Cli = Cliente2.objects.filter(user_id=Cli_id)

        if request.method == "POST":
            formGastos = GenerarFormGastos(request.POST,request.FILES)
            if formGastos.is_valid():

                fam_id=formGastos.cleaned_data.get("familiamenu")
                           
                
                formGastos.save()

                
                      
                ruta = "/administracion/formgasto/" + str(categoria_id)

                return redirect(ruta)

            else:
                ruta = "/administracion/admingastos/"

                return redirect(ruta)

        else:
            initial_data_Tarjeta = {'contrato':categoria_id,'cliente':Cli_id}
            formGastos = GenerarFormGastos(initial=initial_data_Tarjeta)
            formGastos.order_fields(field_order=['familiamenu','proveedor','numfactura','fechagasto','montogasto','formadepago','fechapago','detallecompra'])
        
            return render(request, 'administracion/formgastoscreate.html', {"formTarjeta": formGastos,"Sector": Sect,"Cliente":Cli,"Contrato":contrato})  


def formgastosupdate(request,categoria_id):
    Sect = Tablas.objects.all()
    detallegasto = DetalleGastos.objects.filter(id=categoria_id)

    if detallegasto:
        for Tar in detallegasto:
            id2=Tar.pk
            contrato = Tar.contrato.pk
            cliente = Tar.cliente.pk
            familia = Tar.familiamenu.pk
            proveedor = Tar.proveedor.pk
            formadepago = Tar.formadepago.pk
            numfactura = Tar.numfactura
            fechagasto = Tar.fechagasto
            fechapago = Tar.fechapago
            montogasto = Tar.montogasto
            detallecompra = Tar.detallecompra

    
    
        ruta = "/administracion/formgasto/" + str(contrato)
        
               
        Contrato = Contrato2.objects.filter(id= contrato)
    
        Cli = Cliente2.objects.filter(user_id= cliente)

        if request.method == "POST":
            
                                  
            form = GenerarFormGastosUpdate(request.POST, instance=Tar)
            
            
            if form.is_valid():

                
                form.save()
                

                
                return redirect(ruta)
                
            
            else:
            
                return redirect("/administracion/admingastos/")


        else:

            initial_data_Tarjeta = {'contrato':contrato,'cliente':cliente,'familiamenu':familia,'proveedor':proveedor,'formadepago':formadepago,'numfactura':numfactura,'fechagasto':fechagasto,'fechapago':fechapago,'montogasto':montogasto,'detallecompra':detallecompra}
            formGastos = GenerarFormGastosUpdate(initial=initial_data_Tarjeta)
            formGastos.order_fields(field_order=['familiamenu','proveedor','numfactura','fechagasto','montogasto','formadepago','fechapago','detallecompra'])
        
            return render(request, 'administracion/formgastoscreate.html', {"formTarjeta": formGastos,"Sector": Sect,"Cliente":Cli,"Contrato":Contrato})  

    else:
        return redirect("/administracion/admingastos/")


def borrargasto(request,categoria_id):
    detallegasto = DetalleGastos.objects.filter(id=categoria_id)

    if detallegasto:
        for Con in detallegasto:
            contrato=Con.contrato.pk
    
    
        borrargasto = DetalleGastos.objects.filter(id=categoria_id).delete()

    
        ruta = "/administracion/formgasto/" + str(contrato)

    else:

        ruta = "/administracion/admingastos/"

    return redirect(ruta)


def formmenu(request,categoria_id):
    Sect = Tablas.objects.all()
    Familia = FamiliaMenu.objects.filter(orden__lte='8').order_by('orden')
    #Carta = CartaMenu.objects.filter(tipofamilia_id=categoria_id,activo=True).order_by("id_plato","tipomenu_id","tipomodalidad_id")
    tipofamilia=FamiliaMenu.objects.filter(id=categoria_id)
    for tip in tipofamilia:
        tipo = tip.nombrefamilia
   
    
    cursor = connection.cursor()

    cursor.execute("EXEC GenerarTablaCartaMenuenLinea")
       
    cursor.close()

    
    
    
    

    Carta = CartaMenu_enFila.objects.filter(tipofamilia_id=categoria_id).order_by("id_plato")


    return render(request, 'administracion/cartamenu.html', {"Sector": Sect, "Familia": Familia,"Carta":Carta,"Tipo":tipo})



def formmenucreate(request):
    Sect = Tablas.objects.all()
    Familia = FamiliaMenu.objects.filter(orden__lte='8').order_by('orden')
        
    
    if request.method == "POST":
                           
        form = GenerarFormMenuUpdate(request.POST,request.FILES)
        if form.is_valid():
    
            nombremenu2=form.cleaned_data.get("nombremenu")
            costomenu2=form.cleaned_data.get("costomenu")
            tipofamilia= form.cleaned_data.get("tipofamilia")
            fotomenu2=form.cleaned_data.get("fotomenu")                       
            detallemenu2=form.cleaned_data.get("detallemenu")
            juvenil=form.cleaned_data.get("juvenil")
            mayor=form.cleaned_data.get("mayor")
            normal=form.cleaned_data.get("normal")
            celiaco=form.cleaned_data.get("celiaco")
            vegano=form.cleaned_data.get("vegano")
            vegetariano=form.cleaned_data.get("vegetariano")
    
            Familia2 = FamiliaMenu.objects.get(nombrefamilia=tipofamilia)
            id_tipofamilia = Familia2.pk
    
            consultaSQL = "Insert Into administracion_cartamenu ([nombremenu],[detallemenu],[costomenu],[activo],[id_plato],[tipofamilia_id],[tipomenu_id],[tipomodalidad_id]) values (%s,%s,%s,%s,%s,%s,%s,%s)"

            cursor = connection.cursor()

            
            idplato = CartaMenu.objects.raw("Select max(id_plato) as id from administracion_cartamenu")
            
            if idplato:
                for pla in idplato:
                    plaid = pla.id

                platoid = plaid + 1

            else:
                platoid = 1
      
            
            if juvenil == True:
                Tipo= TipoMenu.objects.get(tipodemenu='juvenil')
                idtipo=Tipo.pk
                if normal == True:
                    Modalidad=ModalidadMenu.objects.get(modalidaddemenu='normal')
                    idmodalidad=Modalidad.pk
                    cursor.execute(consultaSQL,[nombremenu2,detallemenu2,costomenu2,'True',platoid,id_tipofamilia,idtipo,idmodalidad])
                if celiaco == True:
                    Modalidad=ModalidadMenu.objects.get(modalidaddemenu='celiaco')
                    idmodalidad=Modalidad.pk
                    cursor.execute(consultaSQL,[nombremenu2,detallemenu2,costomenu2,'True',platoid,id_tipofamilia,idtipo,idmodalidad])
                if vegano == True:
                    Modalidad=ModalidadMenu.objects.get(modalidaddemenu='vegano')
                    idmodalidad=Modalidad.pk
                    cursor.execute(consultaSQL,[nombremenu2,detallemenu2,costomenu2,'True',platoid,id_tipofamilia,idtipo,idmodalidad])
                if vegetariano == True:
                    Modalidad=ModalidadMenu.objects.get(modalidaddemenu='vejetariano')
                    idmodalidad=Modalidad.pk
                    cursor.execute(consultaSQL,[nombremenu2,detallemenu2,costomenu2,'True',platoid,id_tipofamilia,idtipo,idmodalidad])
            if mayor == True:
                Tipo= TipoMenu.objects.get(tipodemenu='mayor')
                idtipo=Tipo.pk
                if normal == True:
                    Modalidad=ModalidadMenu.objects.get(modalidaddemenu='normal')
                    idmodalidad=Modalidad.pk
                    cursor.execute(consultaSQL,[nombremenu2,detallemenu2,costomenu2,'True',platoid,id_tipofamilia,idtipo,idmodalidad])
                if celiaco == True:
                    Modalidad=ModalidadMenu.objects.get(modalidaddemenu='celiaco')
                    idmodalidad=Modalidad.pk
                    cursor.execute(consultaSQL,[nombremenu2,detallemenu2,costomenu2,'True',platoid,id_tipofamilia,idtipo,idmodalidad])
                if vegano == True:
                    Modalidad=ModalidadMenu.objects.get(modalidaddemenu='vegano')
                    idmodalidad=Modalidad.pk
                    cursor.execute(consultaSQL,[nombremenu2,detallemenu2,costomenu2,'True',platoid,id_tipofamilia,idtipo,idmodalidad])
                if vegetariano == True:
                    Modalidad=ModalidadMenu.objects.get(modalidaddemenu='vejetariano')
                    idmodalidad=Modalidad.pk
                    cursor.execute(consultaSQL,[nombremenu2,detallemenu2,costomenu2,'True',platoid,id_tipofamilia,idtipo,idmodalidad])

                #grabo los datos comunes al plato
                grabar= CartaMenu.objects.filter(id_plato=platoid).update(fotomenu=fotomenu2)
                
    
    
            cursor.execute("EXEC GenerarTablaCartaMenuenLinea")
        
            cursor.close()


        Carta = CartaMenu_enFila.objects.filter(tipofamilia_id=id_tipofamilia).order_by("id_plato")


        return render(request, 'administracion/cartamenu.html', {"Sector": Sect, "Familia": Familia,"Carta":Carta,"Tipo":tipofamilia})

    
    FormMenu = GenerarFormMenuUpdate()
    FormMenu.order_fields(field_order=['nombremenu','costomenu','tipofamilia','fotomenu','detallemenu','juvenil','mayor','normal','celiaco','vegano','vegetariano'])

    return render(request, 'administracion/formmenucreate.html', {"formMenu":FormMenu,"Sector": Sect})





def formmenudesactivar(request,categoria_id):
    Sect = Tablas.objects.all()
    Familia = FamiliaMenu.objects.filter(orden__lte='8').order_by('orden')
    Carta = CartaMenu_enFila.objects.get(id_plato=categoria_id)
    tipo=Carta.tipofamilia
    idfamilia=Carta.tipofamilia.pk

    Desactivar = CartaMenu.objects.filter(id_plato=categoria_id).update(activo=False)

    cursor = connection.cursor()

    cursor.execute("EXEC GenerarTablaCartaMenuenLinea")
       
    cursor.close()

    Carta = CartaMenu_enFila.objects.filter(tipofamilia_id=idfamilia).order_by("id_plato")


    return render(request, 'administracion/cartamenu.html', {"Sector": Sect, "Familia": Familia,"Carta":Carta,"Tipo":tipo})



def formmenuupdate(request,categoria_id):
    Sect = Tablas.objects.all()
    Familia = FamiliaMenu.objects.filter(orden__lte='8').order_by('orden')
    
    if request.method == "POST":
                           
        form = GenerarFormMenuUpdate(request.POST,request.FILES)
        if form.is_valid():
    
            nombremenu2=form.cleaned_data.get("nombremenu")
            costomenu2=form.cleaned_data.get("costomenu")
            id_plato=categoria_id
            tipofamilia= form.cleaned_data.get("tipofamilia")
            fotomenu2=form.cleaned_data.get("fotomenu")                       
            detallemenu2=form.cleaned_data.get("detallemenu")
            juvenil=form.cleaned_data.get("juvenil")
            mayor=form.cleaned_data.get("mayor")
            normal=form.cleaned_data.get("normal")
            celiaco=form.cleaned_data.get("celiaco")
            vegano=form.cleaned_data.get("vegano")
            vegetariano=form.cleaned_data.get("vegetariano")
    
            Familia2 = FamiliaMenu.objects.get(nombrefamilia=tipofamilia)
            id_tipofamilia = Familia2.pk

                        
            #desactivo el plato, para luego activar los que corresponden

            Desactivar = CartaMenu.objects.filter(id_plato=categoria_id).update(activo=False)

            consultaSQL = "Insert Into administracion_cartamenu ([nombremenu],[detallemenu],[costomenu],[activo],[id_plato],[tipofamilia_id],[tipomenu_id],[tipomodalidad_id]) values (%s,%s,%s,%s,%s,%s,%s,%s)"

            cursor = connection.cursor()

            if juvenil == True:
                Tipo= TipoMenu.objects.get(tipodemenu='juvenil')
                idtipo=Tipo.pk
                if normal == True:
                    Modalidad=ModalidadMenu.objects.get(modalidaddemenu='normal')
                    idmodalidad=Modalidad.pk
                    existe=CartaMenu.objects.filter(id_plato=categoria_id,tipofamilia_id=id_tipofamilia,tipomenu_id=idtipo,tipomodalidad_id=idmodalidad)
                    if existe:
                        activar=CartaMenu.objects.filter(id_plato=categoria_id,tipofamilia_id=id_tipofamilia,tipomenu_id=idtipo,tipomodalidad_id=idmodalidad).update(activo=True)
                    else:
                        #consultaSQL = "Insert Into CartaMenu ([nombremenu],[fotomenu],[detallemenu],[costomenu],[activo],[id_plato],[tipofamilia_id],[tipomenu_id],[tipomodalidad_id]) values (nombremenu2,fotomenu2,detallemenu2,costomenu2,'True',categoria_id,id_tipofamilia,idtipo,idmodalidad)"
                        cursor.execute(consultaSQL,[nombremenu2,detallemenu2,costomenu2,'True',categoria_id,id_tipofamilia,idtipo,idmodalidad])
                if celiaco == True:
                    Modalidad=ModalidadMenu.objects.get(modalidaddemenu='celiaco')
                    idmodalidad=Modalidad.pk
                    existe=CartaMenu.objects.filter(id_plato=categoria_id,tipofamilia_id=id_tipofamilia,tipomenu_id=idtipo,tipomodalidad_id=idmodalidad)
                    if existe:
                        activar=CartaMenu.objects.filter(id_plato=categoria_id,tipofamilia_id=id_tipofamilia,tipomenu_id=idtipo,tipomodalidad_id=idmodalidad).update(activo=True)
                    else:
                        #consultaSQL = "Insert Into CartaMenu ([nombremenu],[fotomenu],[detallemenu],[costomenu],[activo],[id_plato],[tipofamilia_id],[tipomenu_id],[tipomodalidad_id]) values (nombremenu2,fotomenu2,detallemenu2,costomenu2,'True',categoria_id,id_tipofamilia,idtipo,idmodalidad)"
                        cursor.execute(consultaSQL,[nombremenu2,detallemenu2,costomenu2,'True',categoria_id,id_tipofamilia,idtipo,idmodalidad])
                if vegano == True:
                    Modalidad=ModalidadMenu.objects.get(modalidaddemenu='vegano')
                    idmodalidad=Modalidad.pk
                    existe=CartaMenu.objects.filter(id_plato=categoria_id,tipofamilia_id=id_tipofamilia,tipomenu_id=idtipo,tipomodalidad_id=idmodalidad)
                    if existe:
                        activar=CartaMenu.objects.filter(id_plato=categoria_id,tipofamilia_id=id_tipofamilia,tipomenu_id=idtipo,tipomodalidad_id=idmodalidad).update(activo=True)
                    else:
                        #consultaSQL = "Insert Into CartaMenu ([nombremenu],[fotomenu],[detallemenu],[costomenu],[activo],[id_plato],[tipofamilia_id],[tipomenu_id],[tipomodalidad_id]) values (nombremenu2,fotomenu2,detallemenu2,costomenu2,'True',categoria_id,id_tipofamilia,idtipo,idmodalidad)"
                        cursor.execute(consultaSQL,[nombremenu2,detallemenu2,costomenu2,'True',categoria_id,id_tipofamilia,idtipo,idmodalidad])
                if vegetariano == True:
                    Modalidad=ModalidadMenu.objects.get(modalidaddemenu='vejetariano')
                    idmodalidad=Modalidad.pk
                    existe=CartaMenu.objects.filter(id_plato=categoria_id,tipofamilia_id=id_tipofamilia,tipomenu_id=idtipo,tipomodalidad_id=idmodalidad)
                    if existe:
                        activar=CartaMenu.objects.filter(id_plato=categoria_id,tipofamilia_id=id_tipofamilia,tipomenu_id=idtipo,tipomodalidad_id=idmodalidad).update(activo=True)
                    else:
                        #consultaSQL = "Insert Into CartaMenu ([nombremenu],[fotomenu],[detallemenu],[costomenu],[activo],[id_plato],[tipofamilia_id],[tipomenu_id],[tipomodalidad_id]) values (nombremenu2,fotomenu2,detallemenu2,costomenu2,'True',categoria_id,id_tipofamilia,idtipo,idmodalidad)"
                        cursor.execute(consultaSQL,[nombremenu2,detallemenu2,costomenu2,'True',categoria_id,id_tipofamilia,idtipo,idmodalidad])
            if mayor == True:
                Tipo= TipoMenu.objects.get(tipodemenu='mayor')
                idtipo=Tipo.pk
                if normal == True:
                    Modalidad=ModalidadMenu.objects.get(modalidaddemenu='normal')
                    idmodalidad=Modalidad.pk
                    existe=CartaMenu.objects.filter(id_plato=categoria_id,tipofamilia_id=id_tipofamilia,tipomenu_id=idtipo,tipomodalidad_id=idmodalidad)
                    if existe:
                        activar=CartaMenu.objects.filter(id_plato=categoria_id,tipofamilia_id=id_tipofamilia,tipomenu_id=idtipo,tipomodalidad_id=idmodalidad).update(activo=True)
                    else:
                        #consultaSQL = "Insert Into CartaMenu ([nombremenu],[fotomenu],[detallemenu],[costomenu],[activo],[id_plato],[tipofamilia_id],[tipomenu_id],[tipomodalidad_id]) values (nombremenu2,fotomenu2,detallemenu2,costomenu2,'True',categoria_id,id_tipofamilia,idtipo,idmodalidad)"
                        cursor.execute(consultaSQL,[nombremenu2,detallemenu2,costomenu2,'True',categoria_id,id_tipofamilia,idtipo,idmodalidad])
                if celiaco == True:
                    Modalidad=ModalidadMenu.objects.get(modalidaddemenu='celiaco')
                    idmodalidad=Modalidad.pk
                    existe=CartaMenu.objects.filter(id_plato=categoria_id,tipofamilia_id=id_tipofamilia,tipomenu_id=idtipo,tipomodalidad_id=idmodalidad)
                    if existe:
                        activar=CartaMenu.objects.filter(id_plato=categoria_id,tipofamilia_id=id_tipofamilia,tipomenu_id=idtipo,tipomodalidad_id=idmodalidad).update(activo=True)
                    else:
                        #consultaSQL = "Insert Into CartaMenu ([nombremenu],[fotomenu],[detallemenu],[costomenu],[activo],[id_plato],[tipofamilia_id],[tipomenu_id],[tipomodalidad_id]) values (nombremenu2,fotomenu2,detallemenu2,costomenu2,'True',categoria_id,id_tipofamilia,idtipo,idmodalidad)"
                        cursor.execute(consultaSQL,[nombremenu2,detallemenu2,costomenu2,'True',categoria_id,id_tipofamilia,idtipo,idmodalidad])
                if vegano == True:
                    Modalidad=ModalidadMenu.objects.get(modalidaddemenu='vegano')
                    idmodalidad=Modalidad.pk
                    existe=CartaMenu.objects.filter(id_plato=categoria_id,tipofamilia_id=id_tipofamilia,tipomenu_id=idtipo,tipomodalidad_id=idmodalidad)
                    if existe:
                        activar=CartaMenu.objects.filter(id_plato=categoria_id,tipofamilia_id=id_tipofamilia,tipomenu_id=idtipo,tipomodalidad_id=idmodalidad).update(activo=True)
                    else:
                        #consultaSQL = "Insert Into CartaMenu ([nombremenu],[fotomenu],[detallemenu],[costomenu],[activo],[id_plato],[tipofamilia_id],[tipomenu_id],[tipomodalidad_id]) values (nombremenu2,fotomenu2,detallemenu2,costomenu2,'True',categoria_id,id_tipofamilia,idtipo,idmodalidad)"
                        cursor.execute(consultaSQL,[nombremenu2,detallemenu2,costomenu2,'True',categoria_id,id_tipofamilia,idtipo,idmodalidad])
                if vegetariano == True:
                    Modalidad=ModalidadMenu.objects.get(modalidaddemenu='vejetariano')
                    idmodalidad=Modalidad.pk
                    existe=CartaMenu.objects.filter(id_plato=categoria_id,tipofamilia_id=id_tipofamilia,tipomenu_id=idtipo,tipomodalidad_id=idmodalidad)
                    if existe:
                        activar=CartaMenu.objects.filter(id_plato=categoria_id,tipofamilia_id=id_tipofamilia,tipomenu_id=idtipo,tipomodalidad_id=idmodalidad).update(activo=True)
                    else:
                        #consultaSQL = "Insert Into CartaMenu ([nombremenu],[fotomenu],[detallemenu],[costomenu],[activo],[id_plato],[tipofamilia_id],[tipomenu_id],[tipomodalidad_id]) values (nombremenu2,fotomenu2,detallemenu2,costomenu2,'True',categoria_id,id_tipofamilia,idtipo,idmodalidad)"
                        cursor.execute(consultaSQL,[nombremenu2,detallemenu2,costomenu2,'True',categoria_id,id_tipofamilia,idtipo,idmodalidad])

                #grabo los datos comunes al plato
                grabar= CartaMenu.objects.filter(id_plato=categoria_id).update(nombremenu=nombremenu2,costomenu=costomenu2,tipofamilia_id=id_tipofamilia,detallemenu=detallemenu2,fotomenu=fotomenu2)
            


                cursor.execute("EXEC GenerarTablaCartaMenuenLinea")
       
                cursor.close()


        Carta = CartaMenu_enFila.objects.filter(tipofamilia_id=id_tipofamilia).order_by("id_plato")


        return render(request, 'administracion/cartamenu.html', {"Sector": Sect, "Familia": Familia,"Carta":Carta,"Tipo":tipofamilia})



   
   
   
    Carta = CartaMenu_enFila.objects.get(id_plato=categoria_id)
   
    TipoFamilia= Carta.tipofamilia.pk

    NombreMenu= Carta.nombremenu

    CostoMenu=Carta.costomenu


    CostoMenu=round(CostoMenu)
            
       
       
    initial_data_Tarjeta = {'nombremenu':Carta.nombremenu,'costomenu':CostoMenu,'tipofamilia':Carta.tipofamilia,'fotomenu':Carta.fotomenu,'detallemenu':Carta.detallemenu,'juvenil': Carta.juvenil,'mayor':Carta.mayor,'normal':Carta.normal,'celiaco':Carta.celiaco,'vegano':Carta.vegano,'vegetariano':Carta.vegetariano}

    FormMenu = GenerarFormMenuUpdate(initial=initial_data_Tarjeta)
    FormMenu.order_fields(field_order=['nombremenu','costomenu','tipofamilia','fotomenu','detallemenu','juvenil','mayor','normal','celiaco','vegano','vegetariano'])

    return render(request, 'administracion/formmenuupdate.html', {"formMenu":FormMenu,"Sector": Sect,"TipoFamilia":TipoFamilia,"Menu":NombreMenu})



def TotalGasto(categoria_id,clienteid):
    
    TotalGastos.objects.filter(contrato_id= categoria_id).delete()

    consultaSQL = DetalleGastos.objects.raw("Select DISTINCT administracion_familiamenu.id,administracion_familiamenu.nombrefamilia from usuarios_detallegastos INNER JOIN administracion_familiamenu ON usuarios_detallegastos.familiamenu_id = administracion_familiamenu.id")
    
   
    if consultaSQL:

        for Fam in consultaSQL:
            gastos= DetalleGastos.objects.filter(contrato_id= categoria_id, familiamenu_id=Fam.id)
            if gastos:
                sumagasto=0
                for Gas in gastos:
            
                    sumagasto = sumagasto+Gas.montogasto
    
                gasto=list()
                gasto.append(TotalGastos(
                contrato_id=categoria_id,
                cliente_id=clienteid,
                familiamenu_id=Fam.id,
                montogasto=sumagasto,
                montoingreso=0
                ))

                TotalGastos.objects.bulk_create(gasto)

        totalgasto=TotalGastos.objects.filter(contrato_id= categoria_id,cliente_id=clienteid)
        sumagasto=0
        if totalgasto:
            for Tot in totalgasto:
                sumagasto=sumagasto+Tot.montogasto

            borrar=SumaGastos.objects.filter(contrato_id= categoria_id,cliente_id=clienteid).delete()

            gastocontrato=list()
            gastocontrato.append(SumaGastos(
            contrato_id=categoria_id,
            cliente_id=clienteid,
            totalgastos=sumagasto
            ))

            SumaGastos.objects.bulk_create(gastocontrato)

            monto=Contrato2.objects.filter(id=categoria_id)
            for mon in monto:
                montoact=mon.montoactualizado

            actualiza=Contrato2.objects.filter(id=categoria_id).update(TotalGastos=sumagasto,Diferencia=montoact-sumagasto,porcentaje=((montoact-sumagasto)*100)/montoact)

    
    #actualiza la Tabla TotalGastos con los ingresos y gastos por tipo de familia
    tarjetas = Contrato2.objects.filter(id=categoria_id)

    cant=1
    for Tar in tarjetas:
        cant=Tar.cant_tarj_contratadas

    #query= "SELECT sum(usuarios_menu.costo_item) as suma,usuarios_menu.id_familiamenu_id as id,usuarios_menu.id_contrato_id as contrato,usuarios_tarjeta.cant_tarjetas as cant FROM usuarios_menu INNER JOIN usuarios_tarjeta ON usuarios_menu.id_tarjeta_id = usuarios_tarjeta.id WHERE usuarios_menu.id_contrato_id = " + str(categoria_id) + " GROUP BY usuarios_menu.id_familiamenu_id ORDER BY usuarios_menu.id_familiamenu_id"

    query= "SELECT familia as id, sum(suma) as sumatotal FROM (SELECT sum(usuarios_menu.costo_item)*usuarios_tarjeta.cant_tarjetas as suma,usuarios_menu.id_familiamenu_id as familia,usuarios_menu.id_tarjeta_id as tarjeta,usuarios_tarjeta.cant_tarjetas as cant "
    query=query + "FROM usuarios_menu INNER JOIN usuarios_tarjeta ON usuarios_menu.id_tarjeta_id = usuarios_tarjeta.id WHERE usuarios_menu.id_contrato_id = " + str(categoria_id) + " GROUP BY usuarios_menu.id_familiamenu_id,usuarios_menu.id_tarjeta_id,usuarios_tarjeta.cant_tarjetas) as tarjetas "
    query = query + "GROUP BY familia"


    ingresomenu = Menu.objects.raw(query)    

    if ingresomenu:
        for Ing in ingresomenu:
            existe=TotalGastos.objects.filter(familiamenu_id=Ing.id,contrato_id=categoria_id)
            if existe:
                actualiza=TotalGastos.objects.filter(contrato_id=categoria_id,familiamenu_id=Ing.id).update(montoingreso=Ing.sumatotal)
            else:
                reg=list()
                reg=list()
                reg.append(TotalGastos(
                contrato_id=categoria_id,
                cliente_id=clienteid,
                familiamenu_id=Ing.id,
                montogasto=0,
                montoingreso=Ing.sumatotal

                ))

                TotalGastos.objects.bulk_create(reg)

    
    ingresomenu= ServicioContratado.objects.filter(id_contrato_id=categoria_id) 

    if ingresomenu:
        for Ing in ingresomenu:
            existe=TotalGastos.objects.filter(familiamenu_id=Ing.id_familiamenu.pk,contrato_id=Ing.id_contrato.pk)
            if existe:
                actualiza=TotalGastos.objects.filter(contrato_id=Ing.id_contrato.pk,familiamenu_id=Ing.id_familiamenu.pk).update(montoingreso=Ing.costo_item*cant)
            else:
                reg=list()
                reg.append(TotalGastos(
                contrato_id=categoria_id,
                cliente_id=clienteid,
                familiamenu_id=Ing.id_familiamenu.pk,
                montogasto=0,
                montoingreso=Ing.costo_item*cant

                ))

                TotalGastos.objects.bulk_create(reg)

    ingresomenu= ServicioAdicional.objects.filter(id_contrato_id=categoria_id) 
    if ingresomenu:
        for Ing in ingresomenu:
            existe=TotalGastos.objects.filter(familiamenu_id=Ing.id_familiamenu.pk,contrato_id=Ing.id_contrato.pk)
            if existe:
                actualiza=TotalGastos.objects.filter(contrato_id=Ing.id_contrato.pk,familiamenu_id=Ing.id_familiamenu.pk).update(montoingreso=Ing.costo_item)
            else:
                reg=list()
                reg.append(TotalGastos(
                contrato_id=categoria_id,
                cliente_id=clienteid,
                familiamenu_id=Ing.id_familiamenu.pk,
                montogasto=0,
                montoingreso=Ing.costo_item

                ))

                TotalGastos.objects.bulk_create(reg)

     #Actualizar diferencia en TotalGastos
    
    cursor = connection.cursor()

    cursor.execute("UPDATE usuarios_totalgastos SET diferencia = montoingreso - montogasto WHERE contrato_id = " + str(categoria_id))

           
    transaction.commit()

    cursor.execute("UPDATE usuarios_totalgastos SET porcentaje = (diferencia*100)/montoingreso WHERE contrato_id = " + str(categoria_id))
    
    transaction.commit()
    
    cursor.close()

   
       
            

def cargarmenu(request, categoria_id):
    
    
    
    Sect = Tablas.objects.all()
    tarjeta= Tarjeta.objects.filter(id= categoria_id)
    
    if tarjeta:
        for Tar in tarjeta:
            contrato = Tar.contrato.pk
            cliente = Tar.cliente.pk
            tipo = Tar.tipodemenu.pk
            modalidad=Tar.modalidaddelmenu.pk

        actualizar = Actualizacion(contrato,cliente)
            
        Contrato = Contrato2.objects.filter(id= contrato)
    
        Cli = Cliente2.objects.filter(user_id= cliente)

        TipodeMenu= TipoMenu.objects.filter(id=tipo)

        ModalidaddeMenu= ModalidadMenu.objects.filter(id=modalidad)

        CartaEntrada = CartaMenu.objects.filter(tipofamilia_id=2,tipomenu_id=tipo,tipomodalidad_id=modalidad,activo=True)

        CartaPrincipal = CartaMenu.objects.filter(tipofamilia_id=3,tipomenu_id=tipo,tipomodalidad_id=modalidad,activo=True)

        CartaPostre = CartaMenu.objects.filter(tipofamilia_id=7,tipomenu_id=tipo,tipomodalidad_id=modalidad,activo=True)
        
        CartaBebida = CartaMenu.objects.filter(tipofamilia_id=11,tipomenu_id=tipo,tipomodalidad_id=modalidad,activo=True)

        MenuExiste = Menu.objects.filter(id_tarjeta_id=categoria_id)

        MenuEntrada = Menu.objects.filter(id_tarjeta_id=categoria_id,id_familiamenu_id='2').select_related("id_item")

        MenuPrincipal = Menu.objects.filter(id_tarjeta_id=categoria_id,id_familiamenu_id='3').select_related("id_item")

        MenuPostre = Menu.objects.filter(id_tarjeta_id=categoria_id,id_familiamenu_id='7').select_related("id_item")
        
        MenuBebida = Menu.objects.filter(id_tarjeta_id=categoria_id,id_familiamenu_id='11').select_related("id_item")
        
        
        
        TotalTarjeta = 0

        for men in MenuExiste:
            TotalTarjeta = TotalTarjeta + men.costo_item

        
        return render(request, 'administracion/menu.html', {"Sector": Sect,"Cliente":Cli,"Contrato":Contrato,"Con":categoria_id,"Tarjeta":tarjeta,"TipodeMenu":TipodeMenu,"ModalidaddeMenu":ModalidaddeMenu,"Entrada":CartaEntrada,"Principal":CartaPrincipal,"Postre":CartaPostre,"Bebida":CartaBebida,"MenuEntrada":MenuEntrada,"MenuPrincipal":MenuPrincipal,"MenuPostre":MenuPostre,"MenuBebida":MenuBebida,"MenuExiste":MenuExiste,"TotalTarjeta":TotalTarjeta})    
            
            

def grabarmenu(request,categoria_id, familia, item):

    #Menuitem = Menu.objects.filter(id_tarjeta_id= categoria_id,id_familiamenu_id=familia)

    tarjeta= Tarjeta.objects.filter(id= categoria_id)
    for Tar in tarjeta:
        contrato = Tar.contrato.pk
    Carta = CartaMenu.objects.filter(id= item)
    if Carta:
        for Car in Carta:
            costomenu=Car.costomenu
            tipofamilia=Car.tipofamilia.pk
    
        #if Menuitem:
        #Existe= Menu.objects.filter(id_tarjeta_id= categoria_id,id_familiamenu_id=familia,id_item_id=item)
        #if not Existe:
        menuborrado= Menu.objects.filter(id_tarjeta_id= categoria_id,id_familiamenu_id=familia).delete()

        menuacargar=list()
        menuacargar.append(Menu(
        id_tarjeta_id=categoria_id,
        costo_item=costomenu,
        id_familiamenu_id=tipofamilia,
        id_item_id=item,
        id_contrato_id=contrato
        ))

        Menu.objects.bulk_create(menuacargar)  

    #cargarmenu(categoria_id)   
    ruta = "/administracion/cargarmenu/"+ str(categoria_id) 

    return redirect(ruta)

def grabarservicio(request,categoria_id, familia, item):

    #Menuitem = Menu.objects.filter(id_tarjeta_id= categoria_id,id_familiamenu_id=familia)

    
    Carta = CartaMenu.objects.filter(id= item)
    if Carta:
        for Car in Carta:
            costomenu=Car.costomenu
            
    
        #if Menuitem:
        Existe= ServicioContratado.objects.filter(id_contrato_id= categoria_id,id_familiamenu_id=familia,id_item_id=item)
        if not Existe:
            menuborrado= ServicioContratado.objects.filter(id_contrato_id= categoria_id,id_familiamenu_id=familia).delete()

            menuacargar=list()
            menuacargar.append(Menu(
            costo_item=costomenu,
            id_familiamenu_id=familia,
            id_item_id=item,
            id_contrato_id=categoria_id
            ))

            ServicioContratado.objects.bulk_create(menuacargar)  

    #cargarmenu(categoria_id)   
    ruta = "/administracion/formtarjetas/"+ str(categoria_id) 

    return redirect(ruta)


def cargarservicios(request,categoria_id,familia):

    if request.method == "POST":

        form = GenerarFormServicio(request.POST)
        
        if form.is_valid():
                    
            menuacargar=list()
            menuacargar.append(ServicioAdicional(
            id_contrato_id = categoria_id,
            id_familiamenu_id = familia,
            costo_item = request.POST.get("costo_item"),
            detalleservicio = request.POST.get("detalleservicio")
            ))

            costo = request.POST.get("costo_item")
            detalle = request.POST.get("detalleservicio")


            ServicioExiste=ServicioAdicional.objects.filter(id_contrato_id=categoria_id,id_familiamenu_id=familia)
            
            if ServicioExiste:
                ServicioAdicional.objects.filter(id_contrato_id=categoria_id,id_familiamenu_id=familia).update(costo_item=costo,detalleservicio=detalle)
            else:
                ServicioAdicional.objects.bulk_create(menuacargar)
    
 
    ruta = "/administracion/formtarjetas/"+ str(categoria_id) 

    return redirect(ruta)


def Total_Contrato(categoria_id,cli):
    
    Contrato=Contrato2.objects.filter(id=categoria_id)

    if Contrato:
    
        tarjetas=Tarjeta.objects.filter(contrato_id=categoria_id)

        servicio=ServicioContratado.objects.filter(id_contrato_id=categoria_id)

        familia = 9
        servicioadicional=ServicioAdicional.objects.filter(id_contrato_id=categoria_id,id_familiamenu_id=familia)

        familia = 10
        serviciologistica=ServicioAdicional.objects.filter(id_contrato_id=categoria_id,id_familiamenu_id=familia)

        cant_tarjetas2=0
        tot_tarjetas2=0
        if tarjetas:
            for Tar in tarjetas:
                cant_tarjetas2=cant_tarjetas2+Tar.cant_tarjetas
                tot_tarjetas2=tot_tarjetas2+Tar.costo_tarjeta

        serv_comunes=0
        if servicio:
            for serv in servicio:
                serv_comunes=serv_comunes+serv.costo_item
            serv_comunes=serv_comunes*cant_tarjetas2

        serv_adicional=0
        if servicioadicional:
            for serv in servicioadicional:
                serv_adicional=serv.costo_item

        serv_logistica=0
        if serviciologistica:
            for serv in serviciologistica:
                serv_logistica=serv.costo_item     

        tot_contrato2=  tot_tarjetas2+serv_comunes+serv_adicional+serv_logistica

        cost_tarjeta = tot_contrato2 / cant_tarjetas2

       
        #controltarjeta=ControlTarjetas.objects.filter(contrato_id=categoria_id,pago_id=1).delete()

        #control_tarjeta=list()
        #control_tarjeta.append(ControlTarjetas(
        #cant_tarjetas_pagas=0,
        #cant_tarjetas_pendientes=cant_tarjetas2,
        #costo_tarjeta_actualizado=cost_tarjeta,
        #contrato_id=categoria_id,
        #pago_id=1
        #))

        #ControlTarjetas.objects.bulk_create(control_tarjeta) 

       
        
        Existe= TotalContrato.objects.filter(id_contrato_id= categoria_id)
        if Existe:
            menuborrado= TotalContrato.objects.filter(id_contrato_id= categoria_id).delete()

        menuacargar=list()
        menuacargar.append(TotalContrato(
        cant_tarjetas=cant_tarjetas2,
        tot_tarjetas=tot_tarjetas2,
        costo_tarjeta=cost_tarjeta,
        tot_comunes=serv_comunes,
        tot_adicionales=serv_adicional,
        tot_logistica=serv_logistica,
        tot_contrato=tot_contrato2,
        id_contrato_id=categoria_id
        ))

        TotalContrato.objects.bulk_create(menuacargar) 

        #Actualiza el monto original del Contrato en la Tabla Contrato2

        Contrato2.objects.filter(id=categoria_id).update(montooriginal=tot_contrato2)

        #Actualizar los pagos y el saldo pendiente de "Contrato2"

        actualizar = Actualizacion(categoria_id,cli)


def AjustarActualizaciones(contrato, categoria_id, diferencia):
    actualizacion = ActualizacionContrato2.objects.filter(contrato_id=contrato,id__gt=categoria_id)

    if actualizacion:
        for Tar in actualizacion:
            id2=Tar.pk
            saldopendiente = Tar.saldopendiente
            porcentaje = Tar.porcentaje
            
            saldopendiente2 = saldopendiente + diferencia
            incremento2 = (saldopendiente * porcentaje)/100
            diferencia = (diferencia + porcentaje)/100

            ActualizacionContrato2.objects.filter(id=id2).update(saldopendiente=saldopendiente2,incremento=incremento2)


def ActualizarTarjetas(categoria_id):
    
    limpiartarjetas = ControlTarjetas.objects.filter(contrato_id=categoria_id).delete()

    pagos= Pagos2.objects.filter(contrato_id=categoria_id)
    if pagos:
        for Pag in pagos:
            monto=Pag.monto
            cliente=Pag.cliente.pk
            costo_tarjeta=Pag.costo_tarjeta
            Pag_id=Pag.pk
            tarjetas = Pag.tarjetas_pend
            deuda = Pag.deuda_a_la_fecha

            tarjetas_pagas= monto/costo_tarjeta
            Tarjetas_pend = tarjetas - tarjetas_pagas
            deuda = deuda - monto
            costo_tarjeta = deuda/Tarjetas_pend

            controltarjeta=list()
            controltarjeta.append(ControlTarjetas(
            cant_tarjetas_pagas=tarjetas_pagas,
            cant_tarjetas_pendientes=Tarjetas_pend,
            costo_tarjeta_actualizado=costo_tarjeta,
            pago_id_id=Pag_id,
            contrato_id=categoria_id,
            cliente_id=cliente
            ))

            ControlTarjetas.objects.bulk_create(controltarjeta)




def modal(request):
    return render(request, 'administracion/modal.html')
