
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Pango
from sqlite3 import dbapi2
from GraficaSexos import Grafica

# nome das columnas do TreeView
columns = ["Cod. Cliente   ",
           "Nome",
           "Sexo",
           "Telefono"]

# opcións do ComboBox
sexo=[['M'],['F']]

# variables:
# bbdd -> conecta ca Base de Datos
# cursor -> executa as sentencias query e recolle os datos
bbdd = dbapi2.connect("PeluqueriaBD.dat")
cursor = bbdd.cursor()

class XestionClientes(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Ventana Xestión de clientes")

        self.set_default_size(600,230)

        # caixa -> é o Gtk.Box principal
        caixa = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(caixa)

        # stack -> é un StackSwitcher que nos separará "Mostrar clientes" e "Agregar clientes"
        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)  # que sea de un lado a otro
        stack.set_transition_duration(1000)  # cuanto queremos que dure

        # os datos do modelo
        self.listmodel = Gtk.ListStore(str, str, str, str)

        cursorClientes = cursor.execute("select * from clientes")
        # engadimos os valores no modelo
        for rexistro in cursorClientes:
            self.listmodel.append(rexistro)

        # engadimos o modelo para o ComboBox do campo sexo
        self.sexoModel = Gtk.ListStore(str)
        for f in range(len(sexo)):
            self.sexoModel.append(sexo[f])

        # unha vista en árbore para ver os datos no modelo
        self.view = Gtk.TreeView(model=self.listmodel)

        # celda -> para cada columna:
        celda = Gtk.CellRendererText() # creo un tipo de celda

        celdaCod = Gtk.CellRendererText(xalign=0.9) # creo un tipo de celda
        columnaCod = Gtk.TreeViewColumn(columns[0], celdaCod, text=0)  # creo unha columna
        columnaCod.set_sort_column_id(0)
        self.view.append_column(columnaCod) # añado a columna á vista

        columnaNombre = Gtk.TreeViewColumn(columns[1], celda, text=1)  # creo unha columna
        columnaNombre.set_sort_column_id(1)
        self.view.append_column(columnaNombre) # añado a columna á vista

        celdaSexo=Gtk.CellRendererText(xalign=0.5) # creo un tipo de celda
        columnaSexo = Gtk.TreeViewColumn(columns[2], celdaSexo, text=2)  # creo unha columna
        columnaSexo.set_sort_column_id(2)
        self.view.append_column(columnaSexo) # añado a columna á vista

        columnaTelf = Gtk.TreeViewColumn(columns[3], celda, text=3)  # creo unha columna
        columnaTelf.set_sort_column_id(3)
        self.view.append_column(columnaTelf) # añado a columna á vista

        # cando seleccionemos unha fila, emite un sinal
        seleccion = self.view.get_selection()
        seleccion.connect("changed", self.on_seleccion_changed)

        # este label mostra a selección da fila seleccionada
        self.label = Gtk.Label(xalign=0.5)
        self.label.set_text("")

        # boton borrar, borra a fila seleccionada
        btnBorrar = Gtk.Button() #label="Borrar",xalign=0.5
        image = Gtk.Image()
        image.set_from_file("./images/borrar_fila.png")
        btnBorrar.add(image)
        btnBorrar.connect("clicked", self.on_btnBorrar_clicked)

        # engadimos a vista, o label e o botón a un Gtk.Box
        boxMostrar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        boxMostrar.pack_start(self.view, False, True, 0)
        boxMostrar.pack_start(self.label, False, False, 0)
        boxMostrar.pack_start(btnBorrar, False, False, 0)

        # engadimos o anterior Gtk.Box a outro Gtk.Box
        boxMostrarClientes= Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        boxMostrarClientes.pack_start(boxMostrar,False,False,0)

        # insertamos o Gtk.Box a o StackSwitcher
        stack.add_titled(boxMostrarClientes, "Mostrar", "Mostrar clientes")


        # creo uns labels
        lblCod = Gtk.Label("    Cod. Cliente:  ")
        lblNome = Gtk.Label("    Nome:  ")
        lblSexo = Gtk.Label("    Sexo:  ")
        lblTelf = Gtk.Label("    Telefono:  ")

        # creo uns entry
        self.txtCod = Gtk.Entry()
        self.txtNome = Gtk.Entry()
        self.cmbSexo = Gtk.ComboBoxText(model=self.sexoModel)
        self.txtTelf = Gtk.Entry()

        # creo un Gtk.Grid e engadolle os labels e os entry anteriores
        grid = Gtk.Grid()
        lblCod.set_justify(Gtk.Justification.RIGHT)
        grid.attach(lblCod, 0, 0, 1, 1)
        grid.attach(self.txtCod, 1, 0, 1, 1)

        lblNome.set_justify(Gtk.Justification.RIGHT)
        grid.attach(lblNome, 2, 0, 1, 1)
        grid.attach(self.txtNome, 3, 0, 1, 1)

        lblSexo.set_justify(Gtk.Justification.RIGHT)
        grid.attach(lblSexo, 0, 1, 1, 1)
        grid.attach(self.cmbSexo, 1, 1, 1, 1)

        lblTelf.set_justify(Gtk.Justification.RIGHT)
        grid.attach(lblTelf, 2, 1, 1, 1)
        grid.attach(self.txtTelf, 3, 1, 1, 1)

        # creo tres botóns
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

        btnCrearGrafica = Gtk.Button()  # label="Limpar"
        image = Gtk.Image()
        image.set_from_file("./images/crear_grafica.png")
        btnCrearGrafica.add(image)
        btnCrearGrafica.connect("clicked", self.on_btnCrearGrafica_clicked)  # , self.listmodel

        # engado os botóns ao Gtk.Grid
        grid.attach(btnEngadir, 2, 4, 1, 1)
        grid.attach(btnLimpar, 3, 4, 1, 1)
        grid.attach(btnCrearGrafica, 3, 5, 1, 1)

        # engado o Gtk.Grid nun Gtk.Box
        boxAgregar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        boxAgregar.pack_start(grid, True, True, 0)

        # introduzco o Gtk.Box ao StackSwitcher
        stack.add_titled(boxAgregar, "Agregar", "Agregar clientes")

        # creo a selección do StarckSwitcher
        selector_stack = Gtk.StackSwitcher()
        selector_stack.set_stack(stack)

        # engado o selector e o stack ao Gtk.Box principal
        caixa.pack_start(selector_stack, True, True, 0)
        caixa.pack_start(stack, True, True, 0)

        self.connect("delete-event", self.destroyed)
        self.show_all()


    # función "on_seleccion_changed":
    # selecciona a fila seleccionada no TreeView e mostrar dita fila nun label
    def on_seleccion_changed(self,seleccion):
        modelo,punteiro=seleccion.get_selected() # get_selected -> nos va a dar unha tupla donde vamos a tener por un lado o punteiro e por outro lado ...
        if punteiro is not None:
            self.label.set_text("%s %s %s %s" %
                (modelo[punteiro][0], modelo[punteiro][1], modelo[punteiro][2], modelo[punteiro][3]))
            self.codCliente=modelo[punteiro][0]

    # función "on_btnBorrar_clicked":
    # ao clickar o botón, borra a fila seleccionada no TreeView e na Base de Datos
    def on_btnBorrar_clicked(self,modelo):#modelo,selection
        cursor.execute("""delete from clientes where codCliente='"""+self.codCliente+"""'""") #'DELETE FROM tabla1 WHERE valor = 2018')+self.txtCod.get_text()+
        bbdd.commit()
        self.label.set_text("")
        self.refrescar(self.listmodel)

    # función "refrescar":
    # refresca as filas do TreeView cando hai algunha modificación na Base de Datos
    def refrescar(self,modelo):
        cursorClientes = cursor.execute("select * from clientes")
        modelo.clear()
        for rexistro in cursorClientes:
            modelo.append(rexistro)

    # función "on_btnEngadir_clicked":
    # engade na Base de Datos e no TreeView o novo cliente introducido
    def on_btnEngadir_clicked(self,cotrol,modelo):
        fila = self.cmbSexo.get_active_iter()  # get_active_iter -> indica/recoge cual está seleccionado
        cursor.execute("""insert into clientes values ('"""+self.txtCod.get_text()+"""','"""+self.txtNome.get_text()+"""','"""+self.cmbSexo.get_model()[fila][0]+"""','"""+self.txtTelf.get_text()+"""')""")
        bbdd.commit()
        self.txtCod.set_text("")
        self.txtNome.set_text("")
        self.txtTelf.set_text("")
        self.refrescar(self.listmodel)

    # función "on_btnLimpar_clicked":
    # ao pulsar no botón limpa o texto dos entry
    def on_btnLimpar_clicked(self,modelo):
        fila = self.cmbSexo.get_active_iter()  # get_active_iter -> indica/recoge cual está seleccionado
        self.txtCod.set_text("")
        self.txtNome.set_text("")
        self.txtTelf.set_text("")

    # función "on_btnCrearGrafica_clicked":
    # ao pulsao o botón crea un arquivo.pdf que mostra unha gráfica co porcentaxe de clientes homes e mulleres
    def on_btnCrearGrafica_clicked(self,modelo):
        self.xGrafica = Grafica()


if __name__=="__main__":
    XestionClientes()
    Gtk.main()


print("ACABAS DE ENTRAR NA CLASE DE XESTION DE CLIENTES")