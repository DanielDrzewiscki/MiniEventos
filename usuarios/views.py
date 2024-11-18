from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import intcomma

from usuarios.models import Cliente2,Contrato2,Pagos2,SumaContrato2,ActualizacionContrato2,SumaActualizacion2,Tarjeta,ServicioContratado,Menu,TotalContrato,ServicioAdicional,ControlTarjetas
from administracion.models import TipoMenu,ModalidadMenu
from administracion.forms import GenerarFormServicio
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta

# Create your views here.

def usuarios(request):
   
    Usu= request.user.id
    Cli=Cliente2.objects.filter(user_id=Usu)
    
    #Pag=Pagos.objects.all()

    if Cli:
        Cli=Cliente2.objects.get(user_id=Usu)
        Contr=Contrato2.objects.filter(cliente_id=Cli)
        
        anos = CalcularEdad(Cli.fecha_nacimiento)
        
        if Contr:
            for con in Contr:
                
                actualizar = Actualizacion(con.id,Cli.id)
                 
            contrtarjetas=ControlTarjetas.objects.filter(cliente_id=Cli.id).select_related("pago_id")
            Pag=Pagos2.objects.filter(cliente_id=Cli.id)
            SumContr=SumaContrato2.objects.filter(cliente_id=Cli.id)
            SumIncrem=SumaActualizacion2.objects.filter(cliente_id=Cli.id)
            Contr=Contrato2.objects.filter(cliente_id=Cli.id)
            Actualizar=ActualizacionContrato2.objects.filter(cliente_id=Cli.id,aplicado=True)

            return render(request, 'usuarios/usuarios.html', {"Cliente":Cli,"Contrato": Contr,"Pago": Pag,"ControlTarjetas":contrtarjetas,"Total":SumContr,"Actualizacion":Actualizar,"TotalIncremento": SumIncrem,"Años": anos})
        else:
            return render(request, 'usuarios/usuarios.html', {"Cliente":Cli,"Contrato": Contr,"Años": anos})
    else:
        return render(request, 'usuarios/nousuarios.html')

def CalcularEdad(fecha_inicial):
    
    Fechahoy = date.today()

    fecha_fin = Fechahoy.strftime('%d-%m-%Y')

    fecha_fin = datetime.strptime(fecha_fin, '%d-%m-%Y')

    tiempo_transc = relativedelta(fecha_fin, fecha_inicial)

    anos = tiempo_transc.years

    return anos


def Actualizacion(categoria_id,cli):
    
    TotalPagos=ControlPagos(categoria_id,cli)
    
    ControlActualizacion(categoria_id,cli)
    
    TotActualz=ActualizarContrato(categoria_id,cli)

    
    tarjetas=Tarjeta.objects.filter(contrato_id=categoria_id)
    canttarjetas_orig=0
    for cant in tarjetas:
        canttarjetas_orig=canttarjetas_orig+cant.cant_tarjetas

    
    contrato=Contrato2.objects.filter(id=categoria_id)

    for con in contrato:
        saldo=con.montooriginal

    Saldo=saldo+TotActualz-TotalPagos
    
    if Saldo<1:
        EstadoPago="Pagado"
    else:
        EstadoPago="Saldo Pendiente"
    MontoActual=saldo+TotActualz
    
    controltarjeta=ControlTarjetas.objects.filter(contrato_id=categoria_id)
    if controltarjeta:
        canttarjetas=0
        costotarjeta=0
        for Tar in controltarjeta:
            canttarjetas=Tar.cant_tarjetas_pendientes
        costotarjeta=Saldo/canttarjetas
        canttarjetas_pagas=canttarjetas_orig-canttarjetas
    else:
        canttarjetas_pagas=0
        canttarjetas=canttarjetas_orig
        costotarjeta=Saldo/canttarjetas_orig
    
     
    
    ActualizacionContrato2.objects.filter(contrato_id=con.id,aplicado=False).update(saldopendiente=Saldo)
    Contrato2.objects.filter(id=con.id).update(montoactualizado=MontoActual,saldopendiente=Saldo,estadopago=EstadoPago,TarjetasPagadas=canttarjetas_pagas,TarjetasPendientes=canttarjetas,Valortarj_actualizado=costotarjeta,cant_tarj_contratadas=canttarjetas_orig)
    TotalContrato.objects.filter(id_contrato_id=con.id).update(costo_tarjeta=costotarjeta)
    
def ControlPagos(con,cli):
    Total = 0
    Pag=Pagos2.objects.filter(contrato_id=con)
    if Pag:
        for p in Pag:
            Total = Total + p.monto
                
        SumContr=SumaContrato2.objects.filter(contrato_id=con)
        if SumContr:
            SumaContrato2.objects.filter(contrato_id=con).update(monto=Total)
        else:
            pagos=list()
            pagos.append(SumaContrato2(
            contrato_id=con,
            cliente_id=cli,
            monto=Total
            ))
            SumaContrato2.objects.bulk_create(pagos)

    else:
        SumContr=SumaContrato2.objects.filter(contrato_id=con)
        if SumContr:
            SumaContrato2.objects.filter(contrato_id=con).update(monto=0)

        


    return Total
    


def ActualizarContrato(con,cli):
    Actualizacion=ActualizacionContrato2.objects.filter(contrato_id=con)
    TotActualz=0
    reg=list()
    if Actualizacion:
        for act in Actualizacion:
            if act.aplicado:
                TotActualz=TotActualz+act.incremento
    else:
        reg.append(ActualizacionContrato2(
        contrato_id=con,
        saldopendiente=0,
        porcentaje=0,
        incremento=0,
        cliente_id=cli
        ))
        ActualizacionContrato2.objects.bulk_create(reg)
    
    #Comprobar si existe al menos un registro no activo
    Actualizacion=ActualizacionContrato2.objects.filter(contrato_id=con,aplicado=False)
    if not Actualizacion:
        reg.append(ActualizacionContrato2(
        contrato_id=con,
        saldopendiente=0,
        porcentaje=0,
        incremento=0,
        cliente_id=cli
        ))
        ActualizacionContrato2.objects.bulk_create(reg)



    return TotActualz


def ControlActualizacion(con,cli):
    Total = 0
    Pag=ActualizacionContrato2.objects.filter(contrato_id=con)
    if Pag:
        for p in Pag:
            Total = Total + p.incremento
                
        SumContr=SumaActualizacion2.objects.filter(contrato_id=con)
        if SumContr:
            SumaActualizacion2.objects.filter(contrato_id=con).update(monto=Total)
        else:
            pagos=list()
            pagos.append(SumaActualizacion2(
            cliente_id=cli,
            contrato_id=con,
            monto=Total
            ))
            SumaActualizacion2.objects.bulk_create(pagos)


def contratos(request, categoria_id):
    
    Contrato = Contrato2.objects.filter(id= categoria_id)
    
    if Contrato:
        for Con in Contrato:
            Cli_id = Con.cliente.pk
            tarpend = Con.TarjetasPendientes
            valortarj = Con.Valortarj_actualizado
            

        Cli = Cliente2.objects.filter(user_id=Cli_id)

               
        tarjeta= Tarjeta.objects.filter(contrato_id= categoria_id)
   
        ServicioExiste = ServicioContratado.objects.filter(id_contrato_id=categoria_id)

        MesaDulce = ServicioContratado.objects.filter(id_contrato_id=categoria_id,id_familiamenu_id='4').select_related("id_item")

        MesaCaliente = ServicioContratado.objects.filter(id_contrato_id=categoria_id,id_familiamenu_id='5').select_related("id_item")

        Cierre = ServicioContratado.objects.filter(id_contrato_id=categoria_id,id_familiamenu_id='6').select_related("id_item")

        Cotillon = ServicioContratado.objects.filter(id_contrato_id=categoria_id,id_familiamenu_id='8').select_related("id_item")
        
        totaltarjeta = 0
        totaltarjetas = 0
        totalservicio=0
        costoservicio=0
               
        if tarjeta:
            totaltarjeta = 0
            totaltarjetas = 0
            for Tar in tarjeta:
                totaltarjeta = totaltarjeta + Tar.cant_tarjetas
                totaltarjetas=totaltarjetas+Tar.costo_tarjeta
                
                            
            if ServicioExiste:
                totalservicio=0
                costoservicio=0
                for Ser in ServicioExiste:
                    totalservicio=totalservicio+Ser.costo_item
                costoservicio=totalservicio*totaltarjeta


            #Grabar la Tabla "TotalContrato" con el total del contrato

                      
            total_contrato=TotalContrato.objects.filter(id_contrato_id=categoria_id)

            


            familiamenu=9
            servicioadicional= ServicioAdicional.objects.filter(id_contrato_id= categoria_id,id_familiamenu_id=familiamenu)
            if servicioadicional:
                for adi in servicioadicional:
                    costo=round(adi.costo_item)
                    detalle=adi.detalleservicio
                costo=intcomma(costo)
                initial_data = {'costo_item':costo,'detalleservicio':detalle}
                formshow = GenerarFormServicio(initial=initial_data)
            else:
                
                formshow = GenerarFormServicio()

            familiamenu=10
            servicioadicional= ServicioAdicional.objects.filter(id_contrato_id= categoria_id,id_familiamenu_id=familiamenu)
            if servicioadicional:
                for adi in servicioadicional:
                    costo=round(adi.costo_item)
                    detalle=adi.detalleservicio
                costo=intcomma(costo)
                initial_data = {'costo_item':costo,'detalleservicio':detalle}
                formlogistica = GenerarFormServicio(initial=initial_data)
            else:
               formlogistica = GenerarFormServicio()

            #return redirect("/usuarios//")
            return render(request, 'usuarios/contrato.html', {"formShow": formshow,"formServicio": formlogistica,"Cliente":Cli,"Con":categoria_id,"Contrato":Contrato,"Tarjeta":tarjeta,"Total":totaltarjeta, "TarjPend":tarpend,"ValorTarj":valortarj,"TotalTarjeta":totaltarjetas,"TotalServicio":costoservicio,"TotalContrato":total_contrato,"ServicioExiste":ServicioExiste,"MesaDulce":MesaDulce,"MesaCaliente":MesaCaliente,"Cierre":Cierre,"Cotillon":Cotillon})    
            #return render(request, 'usuarios/contrato.html')
        else:
           
            return render(request, 'usuarios/nousuarios.html')
    else:
        
        return render(request, 'usuarios/nousuarios.html')
        
def vermenu(request, categoria_id):
    tarjeta= Tarjeta.objects.filter(id= categoria_id)
    
    if tarjeta:
        for Tar in tarjeta:
            contrato = Tar.contrato.pk
            cliente = Tar.cliente.pk
            tipo = Tar.tipodemenu.pk
            modalidad=Tar.modalidaddelmenu.pk
            
        Contrato = Contrato2.objects.filter(id= contrato)
    
        Cli = Cliente2.objects.filter(user_id= cliente)

        TipodeMenu= TipoMenu.objects.filter(id=tipo)

        ModalidaddeMenu= ModalidadMenu.objects.filter(id=modalidad)

        MenuExiste = Menu.objects.filter(id_tarjeta_id=categoria_id)

        MenuEntrada = Menu.objects.filter(id_tarjeta_id=categoria_id,id_familiamenu_id='2').select_related("id_item")

        MenuPrincipal = Menu.objects.filter(id_tarjeta_id=categoria_id,id_familiamenu_id='3').select_related("id_item")

        MenuPostre = Menu.objects.filter(id_tarjeta_id=categoria_id,id_familiamenu_id='7').select_related("id_item")
        
        MenuBebida = Menu.objects.filter(id_tarjeta_id=categoria_id,id_familiamenu_id='11').select_related("id_item")

        TotalTarjeta = 0

        for men in MenuExiste:
            TotalTarjeta = TotalTarjeta + men.costo_item

        
        return render(request, 'usuarios/menu.html', {"Cliente":Cli,"Contrato":Contrato,"Con":categoria_id,"Tarjeta":tarjeta,"TipodeMenu":TipodeMenu,"ModalidaddeMenu":ModalidaddeMenu,"MenuEntrada":MenuEntrada,"MenuPrincipal":MenuPrincipal,"MenuPostre":MenuPostre,"MenuBebida":MenuBebida,"MenuExiste":MenuExiste,"TotalTarjeta":TotalTarjeta})    
    
    else:
        return render(request, 'usuarios/nousuarios.html')