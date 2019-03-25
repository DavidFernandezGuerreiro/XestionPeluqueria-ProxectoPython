import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from XestionClientes import XestionClientes
from XestionServizos import XestionServizos
from XestionFacturas import XestionFacturas

class VentanaPrincipal(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Ventana Principal")
        self.set_border_width(10)

        caixa = Gtk.Box(spacing=6)
        self.add(caixa)

        #introduzco unhas imaxes nos botóns
        #e chamo ás función de cada un deles
        image=Gtk.Image()
        image.set_from_file("./images/clientes.png")
        botonClientes=Gtk.Button()
        botonClientes.add(image)
        botonClientes.connect("clicked", self.on_clientes_clicked)
        caixa.pack_start(botonClientes,True,True,0)

        image = Gtk.Image()
        image.set_from_file("./images/servizos.png")
        botonServicios=Gtk.Button()
        botonServicios.add(image)
        botonServicios.connect("clicked", self.on_servizos_clicked)
        caixa.pack_start(botonServicios, True, True, 0)

        image = Gtk.Image()
        image.set_from_file("./images/facturas.png")
        botonServicios = Gtk.Button()
        botonServicios.add(image)
        botonServicios.connect("clicked", self.on_facturas_clicked)
        caixa.pack_start(botonServicios, True, True, 0)

        image = Gtk.Image()
        image.set_from_file("./images/exit.png")
        boton = Gtk.Button()
        boton.add(image)
        boton.connect("clicked", self.on_close_clicked)
        caixa.pack_start(boton, True, True, 0)

        self.connect("delete-event", Gtk.main_quit)
        self.show_all()


    #cada función chama a súa clase e a executa
    def on_clientes_clicked(self, button):
        print("Xestión de clientes")
        self.xClientes = XestionClientes()

    def on_servizos_clicked(self, button):
        print("Xestión de servizos")
        self.xServizos = XestionServizos()

    def on_facturas_clicked(self, button):
        print("Xestión de facturas")
        self.xFacturas = XestionFacturas()

    def on_close_clicked(self, button):
        print("Closing application")
        Gtk.main_quit()


if __name__=="__main__":
    VentanaPrincipal()
    Gtk.main()