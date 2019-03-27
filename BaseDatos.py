from sqlite3 import dbapi2

bbdd=dbapi2.connect("PeluqueriaBD.dat")
cursor=bbdd.cursor()

class BaseDatos():
    """Xenera a Base de Datos

            **Métodos:**
                - __init__
                - Neste módulo non hai ningún método, simpletemente crea a Base de Datos

                """

    def __init__(self):
        cursor.execute("""create table clientes (codCliente text,
                                        nomCliente text, sexo text, telfCliente text)""")

        cursor.execute("""create table servizos (codServizo text,
                                        nomServizo text, prezoServizo number)""")

        cursor.execute("""create table facturas (numFactura number,
                                        codCliente text, codServizo text, cantidade number)""")



        cursor.execute("""insert into clientes values ('111','David','M','654 321 987')""")
        cursor.execute("""insert into clientes values ('222','Kike','M','693 528 417')""")
        cursor.execute("""insert into clientes values ('333','Maria','F','685 214 953')""")
        cursor.execute("""insert into clientes values ('444','Eva','F','698 352 478')""")

        cursor.execute("""insert into servizos values ('S11','Corte',10)""")
        cursor.execute("""insert into servizos values ('S22','Corte Maquina',8)""")
        cursor.execute("""insert into servizos values ('S33','Depilacion',13)""")
        cursor.execute("""insert into servizos values ('S44','Lavar e peinar',6)""")
        cursor.execute("""insert into servizos values ('S55','Corte Barba',5)""")

        cursor.execute("""insert into facturas values (1,'222','S22',1)""")
        cursor.execute("""insert into facturas values (1,'222','S55',1)""")


        bbdd.commit()
        print("Pechando cursor e conexión base de datos")
        cursor.close()
        bbdd.close()

if __name__=="__main__":
    BaseDatos()