
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Pango
from sqlite3 import dbapi2
from Facturas import Facturas

# nome das columnas do TreeView
columns = ["Num. Factura",
           "Cod. Cliente",
           "Cod. Servizo",
           "Cantidade"]

# opcións do ComboBox
sexo=[['M'],['F']]

# variables:
# bbdd -> conecta ca Base de Datos
# cursor -> executa as sentencias query e recolle os datos
bbdd = dbapi2.connect("PeluqueriaBD.dat")
cursor = bbdd.cursor()

class XestionFacturas(Gtk.Window):
    """Ventana da xestión das facturas

            **Métodos:**
                - __init__

                - on_seleccion_changed

                - on_btnBorrar_clicked

                - refrescar

                - on_btnEngadir_clicked

                - on_btnLimpar_clicked

                - on_btnCrearFactura_clicked

                """

    def __init__(self):
        Gtk.Window.__init__(self, title="Ventana Xestión de facturas")

        self.set_default_size(600,300)

        # caixa -> é o Gtk.Box principal
        caixa = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(caixa)

        # stack -> é un StackSwitcher que nos separará "Mostrar facturas" e "Agregar facturas"
        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)  # que sea de un lado a otro
        stack.set_transition_duration(1000)  # cuanto queremos que dure

        # os datos do modelo
        self.listmodel = Gtk.ListStore(int, str, str, int)

        cursorClientes = cursor.execute("select * from facturas")
        # engadimos os valores no modelo
        for rexistro in cursorClientes:
            self.listmodel.append(rexistro)

        # unha vista en árbore para ver os datos no modelo
        self.view = Gtk.TreeView(model=self.listmodel)

        # celda -> para cada columna:
        celda = Gtk.CellRendererText() # creo un tipo de celda

        celdaNumFactura = Gtk.CellRendererText(xalign=0.9) # creo un tipo de celda
        columnaNumFactura = Gtk.TreeViewColumn(columns[0], celdaNumFactura, text=0)  # creo unha columna
        columnaNumFactura.set_sort_column_id(0)
        self.view.append_column(columnaNumFactura)

        celdaCods = Gtk.CellRendererText(xalign=0.5) # creo un tipo de celda

        columnaCodCliente = Gtk.TreeViewColumn(columns[1], celdaCods, text=1)  # creo unha columna
        columnaCodCliente.set_sort_column_id(1)
        self.view.append_column(columnaCodCliente) # añado a columna á vista

        columnaCodServizo = Gtk.TreeViewColumn(columns[2], celdaCods, text=2)  # creo unha columna
        columnaCodServizo.set_sort_column_id(2)
        self.view.append_column(columnaCodServizo) # añado a columna á vista

        columnaCantidade = Gtk.TreeViewColumn(columns[3], celda, text=3)  # creo unha columna
        columnaCantidade.set_sort_column_id(3)
        self.view.append_column(columnaCantidade) # añado a columna á vista

        # cando seleccionemos unha fila, emite un sinal
        seleccion = self.view.get_selection()
        seleccion.connect("changed", self.on_seleccion_changed)


        # creo un Gtk.Box
        boxMostrar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        boxMostrar.pack_start(self.view, False, True, 0)

        #creo uns labels e un entry
        self.lblSpace=Gtk.Label("                        ")
        self.lblBorrar=Gtk.Label("Eliminar fila:   ",xalign=0.9)
        self.lblFilaSeleccionada = Gtk.Label(xalign=0.5)
        self.lblFilaSeleccionada.set_text("")

        self.lblSpace2 = Gtk.Label("                        ")
        self.lblNumFactura = Gtk.Label("  Num. factura:   ", xalign=0.9)
        self.txtNumFactura = Gtk.Entry()

        # creo un Gtk.Grid e lle engado os labels e o entry
        grid = Gtk.Grid()
        grid.attach(self.lblSpace, 0, 0, 1, 1)
        self.lblBorrar.set_justify(Gtk.Justification.RIGHT)
        grid.attach(self.lblBorrar, 1, 0, 1, 1)
        self.lblFilaSeleccionada.set_justify(Gtk.Justification.RIGHT)
        grid.attach(self.lblFilaSeleccionada, 2, 0, 1, 1)

        # creo uns botóns e os engado ao Gtk.Grid
        btnBorrar = Gtk.Button()  # label="Limpar"
        image = Gtk.Image()
        image.set_from_file("./images/borrar_fila.png")
        btnBorrar.add(image)
        btnBorrar.connect("clicked", self.on_btnBorrar_clicked)  # , self.listmodel
        grid.attach(btnBorrar, 3, 0, 1, 1)

        self.lblSpace2.set_justify(Gtk.Justification.RIGHT)
        grid.attach(self.lblSpace2, 0, 0, 1, 1)
        self.lblNumFactura.set_justify(Gtk.Justification.RIGHT)
        grid.attach(self.lblNumFactura, 1, 1, 1, 1)
        grid.attach(self.txtNumFactura, 2, 1, 1, 1)

        btnCrearFactura = Gtk.Button()  # label="Crear factura"
        image = Gtk.Image()
        image.set_from_file("./images/crear_factura.png")
        btnCrearFactura.add(image)
        btnCrearFactura.connect("clicked", self.on_btnCrearFactura_clicked)
        grid.attach(btnCrearFactura, 3, 1, 1, 1)

        # creo un GtkBox e lle engado o outro Gtk.Box e o Gtk.Grid
        boxMostrarFacturas= Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        boxMostrarFacturas.pack_start(boxMostrar,False,False,0)
        boxMostrarFacturas.pack_start(grid,False,False,0)#boxMostrar

        # insertamos o Gtk.Box a o StackSwitcher
        stack.add_titled(boxMostrarFacturas, "Mostrar", "Mostrar facturas")


        # recollo os nomes dos clientes da Base de Datos e os meto nun ComboBox
        cursorClientes = cursor.execute("select nomCliente from clientes")
        self.modeloClientes=Gtk.ListStore(str)
        # anexar los valores en el modelo
        for rexistro in cursorClientes:
            self.modeloClientes.append(rexistro)

        # recollo os nomes dos servizos da Base de Datos e os meto nun ComboBox
        cursorServizos = cursor.execute("select nomServizo from servizos")
        self.modeloServizos = Gtk.ListStore(str)
        # anexar los valores en el modelo
        for rexistro in cursorServizos:
            self.modeloServizos.append(rexistro)

        # creo uns labels e uns entrys
        lblNumFactura = Gtk.Label("    Número factura:  ")
        lblNomeCliente = Gtk.Label("    Nome cliente:  ")
        lblNomeServizo = Gtk.Label("    Nome servizo:  ")
        lblCantidade = Gtk.Label("    Cantidade:  ")

        self.txtNumFactura = Gtk.Entry()
        self.cmbNomeCliente = Gtk.ComboBoxText(model=self.modeloClientes)
        self.cmbNomeServizo = Gtk.ComboBoxText(model=self.modeloServizos)
        self.txtCantidade = Gtk.Entry()

        # creo un Gtk.Grid e lle engado os labels e entrys anteriores
        grid = Gtk.Grid()
        lblNumFactura.set_justify(Gtk.Justification.RIGHT)
        grid.attach(lblNumFactura, 0, 0, 1, 1)
        grid.attach(self.txtNumFactura, 1, 0, 1, 1)

        lblNomeCliente.set_justify(Gtk.Justification.RIGHT)
        grid.attach(lblNomeCliente, 0, 1, 1, 1)
        grid.attach(self.cmbNomeCliente, 1, 1, 1, 1)

        lblNomeServizo.set_justify(Gtk.Justification.RIGHT)
        grid.attach(lblNomeServizo, 0, 2, 1, 1)
        grid.attach(self.cmbNomeServizo, 1, 2, 1, 1)

        lblCantidade.set_justify(Gtk.Justification.RIGHT)
        grid.attach(lblCantidade, 2, 2, 1, 1)
        grid.attach(self.txtCantidade, 3, 2, 1, 1)

        # creo dous botóns
        btnEngadir = Gtk.Button()  # label="Engadir"
        image = Gtk.Image()
        image.set_from_file("./images/engadir.png")
        btnEngadir.add(image)
        btnEngadir.connect("clicked", self.on_btnEngadir_clicked, self.listmodel)

        btnLimpar = Gtk.Button()  # label="Limpar"
        image = Gtk.Image()
        image.set_from_file("./images/limpar.png")
        btnLimpar.add(image)
        btnLimpar.connect("clicked", self.on_btnLimpar_clicked)  # , self.listmodel

        # engado os botóns ao Gtk.Grid
        grid.attach(btnEngadir, 2, 4, 1, 1)
        grid.attach(btnLimpar, 3, 4, 1, 1)

        # engado o Gtk.Grid nun Gtk.Box
        boxAgregar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        boxAgregar.pack_start(grid, True, True, 0)

        # introduzco o Gtk.Box ao StackSwitcher
        stack.add_titled(boxAgregar, "Agregar", "Agregar facturas")

        # creo a selección do StarckSwitcher
        selector_stack = Gtk.StackSwitcher()
        selector_stack.set_stack(stack)

        # engado o selector e o stack ao Gtk.Box principal
        caixa.pack_start(selector_stack, True, True, 0)
        caixa.pack_start(stack, True, True, 0)

        self.connect("delete-event", self.destroyed)  # Gtk.main_quit
        self.show_all()


    # función "on_seleccion_changed":
    # selecciona a fila seleccionada no TreeView e mostrar dita fila nun label
    def on_seleccion_changed(self,seleccion):
        """selecciona a fila seleccionada no TreeView e mostrar dita fila nun label

                :param seleccion: selecciona a fila
                :type seleccion: Widget
                :return: None
                :raises: AttributeError, KeyError
                """
        modelo,punteiro=seleccion.get_selected() # get_selected -> nos va a dar unha tupla donde vamos a tener por un lado o punteiro e por outro lado ...
        if punteiro is not None:
            self.lblFilaSeleccionada.set_text("%s %s %s %s" %
                                              (modelo[punteiro][0], modelo[punteiro][1], modelo[punteiro][2], modelo[punteiro][3]))
            self.numFactura=modelo[punteiro][0]

    # función "on_btnBorrar_clicked":
    # ao clickar o botón, borra a fila seleccionada no TreeView e na Base de Datos
    def on_btnBorrar_clicked(self,modelo):#modelo,selection
        """ao clickar o botón, borra a fila seleccionada no TreeView e na Base de Datos

                :param modelo: modelo do TreeView (ListStore)
                :type modelo: ListStore
                :return: None
                :raises: AttributeError, KeyError
                """
        cursor.execute("""delete from facturas where numFactura=?""",(self.numFactura,)) #'DELETE FROM tabla1 WHERE valor = 2018')+self.txtCod.get_text()+
        bbdd.commit()
        self.lblFilaSeleccionada.set_text("")
        self.refrescar(self.listmodel)

    # función "refrescar":
    # refresca as filas do TreeView cando hai algunha modificación na Base de Datos
    def refrescar(self,modelo):
        """refresca as filas do TreeView cando hai algunha modificación na Base de Datos

                :param modelo: modelo do TreeView (ListStore)
                :type modelo: ListStore
                :return: None
                :raises: AttributeError, KeyError
                """
        cursorFacturas = cursor.execute("select * from facturas")
        modelo.clear()
        for rexistro in cursorFacturas:
            modelo.append(rexistro)

    # función "on_btnEngadir_clicked":
    # engade na Base de Datos e no TreeView o novo cliente introducido
    def on_btnEngadir_clicked(self,cotrol,modelo):
        """engade na Base de Datos e no TreeView o novo cliente introducido

                :param control: celda da táboa
                :type control: Widget
                :param modelo: modelo do TreeView (ListStore)
                :type modelo: ListStore
                :return: None
                :raises: AttributeError, KeyError
                """
        filaCliente = self.cmbNomeCliente.get_active_iter()  # get_active_iter -> indica/recoge cual está seleccionado
        filaServizo = self.cmbNomeServizo.get_active_iter()

        codCliente=cursor.execute("""select codCliente from clientes where nomCliente='"""+self.cmbNomeCliente.get_model()[filaCliente][0]+"""'""""")
        for rexistro in codCliente:
            codCliente=rexistro[0]
            print(codCliente)
        codServizo=cursor.execute("""select codServizo from servizos where nomServizo='""" + self.cmbNomeServizo.get_model()[filaServizo][0] + """'""""")
        for rexistro2 in codServizo:
            codServizo=rexistro2[0]
            print(codServizo)

        cursor.execute("""insert into facturas values ('""" + self.txtNumFactura.get_text() + """','""" +codCliente+ """','""" +codServizo+ """','""" + self.txtCantidade.get_text() + """')""")
        bbdd.commit()

        self.txtNumFactura.set_text("")
        self.txtCantidade.set_text("")

        self.refrescar(self.listmodel)

    # función "on_btnLimpar_clicked":
    # ao pulsar no botón limpa o texto dos entry
    def on_btnLimpar_clicked(self,modelo):
        """ao pulsar no botón limpa o texto dos entry

                :param modelo: modelo do TreeView (ListStore)
                :type modelo: ListStore
                :return: None
                :raises: AttributeError, KeyError
                """
        self.txtNumFactura.set_text("")
        self.txtCantidade.set_text("")

    # función "on_btnCrearFactura_clicked":
    # ao pulsar no botón chama á clase Facturas
    def on_btnCrearFactura_clicked(self,modelo):
        """ao pulsar no botón chama á clase Facturas, e crea un arquivo pdf que mostra as facturas dos clientes

                :param modelo: modelo do TreeView (ListStore)
                :type modelo: ListStore
                :return: None
                :raises: AttributeError, KeyError
                """
        self.xFacturas = Facturas()

if __name__=="__main__":
    XestionFacturas()
    Gtk.main()


print("ACABAS DE ENTRAR NA CLASE DE XESTION DE FACTURAS")