
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Pango
from sqlite3 import dbapi2

# nome das columnas do TreeView
columns = ["Cod. Servizo   ",
           "Nome",
           "Prezo (€)"]

# opcións do ComboBox
sexo=[['M'],['F']]

# variables:
# bbdd -> conecta ca Base de Datos
# cursor -> executa as sentencias query e recolle os datos
bbdd = dbapi2.connect("PeluqueriaBD.dat")
cursor = bbdd.cursor()

class XestionServizos(Gtk.Window):
    """Ventana da xestión dos servizos

            **Métodos:**
                - __init__

                - on_seleccion_changed

                - on_btnBorrar_clicked

                - refrescar

                - on_btnEngadir_clicked

                - on_btnLimpar_clicked

                """

    def __init__(self):
        Gtk.Window.__init__(self, title="Ventana Xestión de servizos")

        self.set_default_size(600,230)

        # caixa -> é o Gtk.Box principal
        caixa = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(caixa)

        # stack -> é un StackSwitcher que nos separará "Mostrar servizos" e "Agregar servizos"
        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)  # que sea de un lado a otro
        stack.set_transition_duration(1000)  # cuanto queremos que dure

        # os datos do modelo
        self.listmodel = Gtk.ListStore(str, str, int)

        cursorServizos = cursor.execute("select * from servizos")
        # engadimos os valores no modelo
        for rexistro in cursorServizos:
            self.listmodel.append(rexistro)

        # unha vista en árbore para ver os datos no modelo
        self.view = Gtk.TreeView(model=self.listmodel)

        # celda -> para cada columna:
        celda = Gtk.CellRendererText() # creo un tipo de celda

        celdaCod = Gtk.CellRendererText(xalign=0.9) # creo un tipo de celda
        columnaCod = Gtk.TreeViewColumn(columns[0], celdaCod, text=0)  # creo unha columna
        columnaCod.set_sort_column_id(0)
        self.view.append_column(columnaCod) # añado a columna á vista

        celdaNombre = Gtk.CellRendererText(xalign=0.9) # creo un tipo de celda
        columnaNombre = Gtk.TreeViewColumn(columns[1], celdaNombre, text=1)  # creo unha columna
        columnaNombre.set_sort_column_id(1)
        self.view.append_column(columnaNombre) # añado a columna á vista

        columnaPrezo = Gtk.TreeViewColumn(columns[2], celda, text=2)  # creo unha columna
        columnaPrezo.set_sort_column_id(2)
        self.view.append_column(columnaPrezo) # añado a columna á vista

        # cando seleccionemos unha fila, emite un sinal
        seleccion = self.view.get_selection()
        seleccion.connect("changed", self.on_seleccion_changed)

        # este label mostra a selección da fila seleccionada
        self.label = Gtk.Label(xalign=0.5)
        self.label.set_text("")

        # boton borrar, borra a fila seleccionada
        btnBorrar = Gtk.Button()  # label="Engadir"
        image = Gtk.Image()
        image.set_from_file("./images/borrar_fila.png")
        btnBorrar.add(image)
        btnBorrar.connect("clicked", self.on_btnBorrar_clicked)  # , self.listmodel

        # engadimos a vista, o label e o botón a un Gtk.Box
        boxMostrar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        boxMostrar.pack_start(self.view, False, True, 0)
        boxMostrar.pack_start(self.label, False, False, 0)
        boxMostrar.pack_start(btnBorrar, False, False, 0)

        # engadimos o anterior Gtk.Box a outro Gtk.Box
        boxMostrarServizos= Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        boxMostrarServizos.pack_start(boxMostrar,False,False,0)

        # insertamos o Gtk.Box a o StackSwitcher
        stack.add_titled(boxMostrarServizos, "Mostrar", "Mostrar servizos")


        # creo uns labels
        lblCod = Gtk.Label("    Cod. Servizo:  ")
        lblNome = Gtk.Label("    Nome:  ")
        lblPrezo = Gtk.Label("    Prezo:  ")

        # creo uns entry
        self.txtCod = Gtk.Entry()
        self.txtNome = Gtk.Entry()
        self.txtPrezo = Gtk.Entry()

        # creo un Gtk.Grid e engadolle os labels e os entry anteriores
        grid = Gtk.Grid()
        lblCod.set_justify(Gtk.Justification.RIGHT)
        grid.attach(lblCod, 0, 0, 1, 1)
        grid.attach(self.txtCod, 1, 0, 1, 1)

        lblNome.set_justify(Gtk.Justification.RIGHT)
        grid.attach(lblNome, 2, 0, 1, 1)
        grid.attach(self.txtNome, 3, 0, 1, 1)

        lblPrezo.set_justify(Gtk.Justification.RIGHT)
        grid.attach(lblPrezo, 0, 1, 1, 1)
        grid.attach(self.txtPrezo, 1, 1, 1, 1)

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
        stack.add_titled(boxAgregar, "Agregar", "Agregar servizos")

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
        """selecciona a fila seleccionada no TreeView e mostrar dita fila nun label

                :param seleccion: selecciona a fila
                :type seleccion: Widget
                :return: None
                :raises: AttributeError, KeyError
                """
        modelo,punteiro=seleccion.get_selected() # get_selected -> nos va a dar unha tupla donde vamos a tener por un lado o punteiro e por outro lado ...
        if punteiro is not None:
            self.label.set_text("%s %s %s" %
                (modelo[punteiro][0], modelo[punteiro][1], modelo[punteiro][2]))
            self.codServizo=modelo[punteiro][0]

    # función "on_btnBorrar_clicked":
    # ao clickar o botón, borra a fila seleccionada no TreeView e na Base de Datos
    def on_btnBorrar_clicked(self,modelo):#modelo,selection
        """ao clickar o botón, borra a fila seleccionada no TreeView e na Base de Datos

                :param modelo: modelo do TreeView (ListStore)
                :type modelo: ListStore
                :return: None
                :raises: AttributeError, KeyError
                """
        cursor.execute("""delete from servizos where codServizo='""" + self.codServizo + """'""") #'DELETE FROM tabla1 WHERE valor = 2018')+self.txtCod.get_text()+
        bbdd.commit()
        self.label.set_text("")
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
        cursorSevizo = cursor.execute("select * from servizos")
        modelo.clear()
        for rexistro in cursorSevizo:
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
        cursor.execute("""insert into servizos values ('""" + self.txtCod.get_text() +"""','""" + self.txtNome.get_text() +"""','""" + self.txtPrezo.get_text() + """')""")
        bbdd.commit()
        self.txtCod.set_text("")
        self.txtNome.set_text("")
        self.txtPrezo.set_text("")
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
        self.txtCod.set_text("")
        self.txtNome.set_text("")
        self.txtPrezo.set_text("")

if __name__=="__main__":
    XestionServizos()
    Gtk.main()

print("ACABAS DE ENTRAR NA CLASE DE XESTION DE SERVIZOS")