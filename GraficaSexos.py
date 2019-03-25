from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.shapes import Drawing
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate,Spacer,Image
from sqlite3 import dbapi2
from reportlab.lib.units import inch

# variables:
# bbdd -> conecta ca Base de Datos
# cursor -> executa as sentencias query e recolle os datos
bbdd = dbapi2.connect("PeluqueriaBD.dat")
cursor = bbdd.cursor()

class Grafica():
    def __init__(self):
        guion=[]
        d=Drawing(400,200)

        # cursorSexoM -> recolle os homes que hay na Base de Datos
        cursorSexoM = cursor.execute("select sexo from clientes where sexo='M'")
        numH=0
        # engadimos os valores no modelo
        for rexistro in cursorSexoM:
            sexo=rexistro[0]
            numH=numH+1
            print(sexo)
        print("Número de clientes homes: ",numH)

        # # cursorSexoF -> recolle as mulleres que hay na Base de Datos
        cursorSexoF = cursor.execute("select sexo from clientes where sexo='F'")
        numF=0
        # engadimos os valores no modelo
        for rexistro in cursorSexoF:
            sexo=rexistro[0]
            numF=numF+1
            print(sexo)
        print("Número de clientes mulleres: ",numF)

        # pasamoslle os valores ao gráfico
        datos=[(numH,numF)]
        grafica=VerticalBarChart()
        grafica.x=50
        grafica.y=50
        grafica.height=125
        grafica.width=300
        grafica.data=datos #le decimos cuales son los datos.
        grafica.strokeColor=colors.black
        grafica.valueAxis.valueMin=0
        grafica.valueAxis.valueMax=20
        grafica.valueAxis.valueStep=4
        grafica.categoryAxis.labels.boxAnchor='ne' #etiquetas dos exes
        grafica.categoryAxis.labels.dx=8
        grafica.categoryAxis.labels.dy=-2
        grafica.categoryAxis.labels.angle=30 #le damos un angulo
        grafica.categoryAxis.categoryNames=['HOMES','MULLERES']
        grafica.groupSpacing=10
        grafica.barSpacing=2

        d.add(grafica)

        # engadimos o logo da Perruquería e o gráfico
        logo="./images/logo_barber_grafica.png"
        img=Image(logo,5.7*inch,2.5*inch) # damoslle unhas medidas á imaxe
        guion.append(img)
        guion.append(d)
        guion.append(Spacer(0,20))

        # lle damos un nome ao documento
        doc=SimpleDocTemplate("graficoSexo.pdf",pagesize=A4)
        doc.build(guion)

if __name__=="__main__":
    Grafica()