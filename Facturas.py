
from reportlab.platypus import (SimpleDocTemplate,PageBreak,Image,Spacer,Table,TableStyle)
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch

from sqlite3 import dbapi2

# variables:
# bbdd -> conecta ca Base de Datos
# cursor -> executa as sentencias query e recolle os datos
bbdd=dbapi2.connect("PeluqueriaBD.dat")
cursor=bbdd.cursor()

class Facturas():
    def __init__(self):

        detalleFactura=[]
        facturas=[]

        # executamos un cursor para os numFactura
        cursorConsultaFacturas=cursor.execute("select numFactura from facturas")
        listaFacturas=list()
        for numFactura in cursorConsultaFacturas:
            if numFactura[0] not in listaFacturas:
                listaFacturas.append(numFactura[0])
                print(listaFacturas[0])

        # executamos un cursor e recollemos o codCliente, codServizo e cantidade
        for numFactura in listaFacturas:
            codigoCliente=None
            consultaFactura=None
            #es distinto al de arriba "cursorConsultaFactura"
            cursorConsultaFactura=cursor.execute("select codCliente,codServizo,cantidade from facturas where numFactura=?",(int(numFactura),))
            codigoCliente=cursorConsultaFactura.fetchone()[0]
            # insertamos o codCliente e o numFactura na Factura
            detalleFactura.append(['Cod Cliente:',codigoCliente,'','Num Factura:',numFactura]) #cada liña da factura vai ser unha lista

            # executamos un cursor e recollemos o nomCliente e o telfCliente do cliente dependendo do codCliente
            cursorConsultaFactura=cursor.execute("select nomCliente,telfCliente from clientes where codCliente='"+str(codigoCliente)+"'")
            rexistroCliente=cursorConsultaFactura.fetchone()

            # insertamos o nomCliente e o telfCliente na Factura
            detalleFactura.append(['Nome:',rexistroCliente[0],'','',''])
            detalleFactura.append(['Teléfono:',rexistroCliente[1],'','',''])

            # executamos un cursor e recollemos o codServizo e a cantidade do servizo dependendo do numFactura
            cursorConsultaDetalleFactura=cursor.execute("select codServizo,cantidade from facturas where numFactura=?",(numFactura,))
            lconsultaDetalleFactura=[]
            for elementoFactura in cursorConsultaDetalleFactura:
                # insertamos o codServizo e a cantidade nunha lista da Factura
                lconsultaDetalleFactura.append([elementoFactura[0],elementoFactura[1]])
                print(elementoFactura)

            detalleFactura.append(["", "", "", "", ""])
            # introducimos a cabeceira da lista da Factura:
            detalleFactura.append(["Código servizo","Descripción","Cantidade","Prezo unitario","Prezo"])
            prezoTotal=0
            for elemento in lconsultaDetalleFactura:
                # executamos o cursor e recollemos o nomServizo e o prezoServizo dos servizos dependendo do codServizo
                cursorConsultaServizo=cursor.execute("select nomServizo,prezoServizo from servizos where codServizo='"+str(elemento[0])+"'")
                rexistroServizo=cursorConsultaServizo.fetchone()
                print(elemento)

                # facemos o calculo do total da Factura
                prezo=elemento[1]*rexistroServizo[1]
                detalleFactura.append([elemento[0],rexistroServizo[0],elemento[1],rexistroServizo[1],prezo]) #calculo
                prezoTotal=prezoTotal+prezo

            # insertamos na lista da Factura o prezo total da Factura
            detalleFactura.append(["","","","Prezo total:",prezoTotal])
            facturas.append(list(detalleFactura))
            detalleFactura.clear()


        # lle damos un nome ao documento
        doc=SimpleDocTemplate("facturas.pdf",pagesize=A4)
        guion=[]

        for factura in facturas:
            taboa=Table(factura,colWidths=80,rowHeights=30)#colWidths=anchura dos cuadrados da taboa. rowHeights=altura dos cuadrados da taboa.
            taboa.setStyle(TableStyle([
                ('TEXTCOLOR',(0,0),(-1,2),colors.chocolate), #lle damos color á primeira fila.
                ('TEXTCOLOR',(0,4),(-1,-1),colors.green), #(fila,elemento)
                ('BACKGROUND',(0,4),(-1,-1),colors.lightgrey), #vai a coller toda a taboa menos la cabecera.     lightcyan
                ('ALIGN',(2,5),(-1,-1),'RIGHT'), #alinea o texto nas celdas á dereita.
                ('VALIGN',(0,0),(-1,-1),'MIDDLE'), #alineamiento ao medio do folio.
                ('BOX', (0,0),(-1,2), 1, colors.black), # creamos outro box para os datos de arriba
                ('BOX',(0,4),(-1,-2),1,colors.black), #pon unha caixa no contorno. (o "1" é o ancho da liña da taboa).
                ('INNERGRID',(0,4),(-1,-2),0.5,colors.grey) #o grid que hai no medio. (as liñas de dentro)
            ]))

            # poño una imaxe co logo da Perruquería
            logo="./images/logo_barber_factura.png"
            img=Image(logo,5.7*inch,2.5*inch) # damoslle unhas medidas á imaxe
            guion.append(img)
            guion.append(taboa)
            guion.append(Spacer(0,40))
            guion.append(PageBreak()) #cada factura nunha páxina (salto de páxina)

        doc.build(guion) #crea o documento.


if __name__=="__main__":
    Facturas()