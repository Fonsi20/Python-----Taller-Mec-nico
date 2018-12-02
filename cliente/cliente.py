import os
import zipfile
import getpass
import gi
import GestionClientes
import datos
import re
import datetime
import time

gi.require_version('Gtk', '3.0')
from gi.repository import Gdk, Gtk
from os.path import abspath, dirname, join

WHERE_AM_I = abspath(dirname(__file__))


class Cliente:
    def __init__(self):
        # iniciamos la libreria GTK
        b = Gtk.Builder()
        b.add_from_file('cliente.glade')

        # Cargar el aspecto de la  app
        self.set_style()

        # Eventos de Clientes y Generales
        self.venprincipal = b.get_object("venprincipal")
        self.venDialog = b.get_object("winDialog")
        self.venCalendario = b.get_object("winCalendar")
        self.altacliente = b.get_object("altacliente")
        self.modificarcliente = b.get_object("modificarcliente")
        self.bajacliente = b.get_object("bajacliente")
        self.btnsalir = b.get_object("salir")
        self.lblaviso = b.get_object("lblaviso")
        self.entdni = b.get_object("entdni")
        self.entnome = b.get_object("entnome")
        self.entapel = b.get_object("entapel")
        self.entmail = b.get_object("entmail")
        self.entmat = b.get_object("entmat")
        self.entmovil = b.get_object("entmovil")
        self.entradafecha = b.get_object('entfecha')
        self.treeclientes = b.get_object("treeclientes")
        self.listclientes = b.get_object("listclientes")
        self.calendario = b.get_object('entCalendario')
        self.notebook = b.get_object('notebook')

        # Eventos de Servicios
        self.entManoObra = b.get_object("entmanoObra")
        self.entFactu = b.get_object("entFactu")
        self.chkBateria = b.get_object("chkBateria")
        self.bateria = '0'
        self.chkAceite = b.get_object("chkAceite")
        self.chkNeumo = b.get_object("chkNeumo")
        self.chkPasti = b.get_object("chkPasti")
        self.chkFiltro = b.get_object("chkFiltro")
        self.edLitros = b.get_object("edLitros")
        self.cmboxNeuma = b.get_object("cmbNeuma")
        self.cmboxPasti = b.get_object("cmbPasti")
        self.cmboxFiltro = b.get_object("cmbFiltro")
        self.treeservicios = b.get_object("treeservicios")
        self.listservicios = b.get_object("listservicios")

        # Eventos de Facturas
        self.lblResultadoFac = b.get_object("facResuFac")
        self.edMatriculaFac = b.get_object("facMatri")
        self.fechaFac = b.get_object("facFecha")
        self.treefacturas = b.get_object("treefacturas")
        self.listfacturas = b.get_object("listfacturas")

        # Tupla que maneja los meses del año
        self.meses = (
            'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre',
            'Noviembre',
            'Diciembre')

        # Diccionario de eventos

        dic = {'on_venprincipal_destroy': self.salir,
               'on_altacliente_clicked': self.alta,
               'on_modificarcliente_clicked': self.modificar,
               'on_bajacliente_clicked': self.baja,
               'on_salir_clicked': self.salir,
               'on_salirToolbar_activate': self.salir,
               'on_btnCalendar_clicked': self.abrirCalendar,
               'on_btnCalendar2_clicked': self.abrirCalendar,
               'on_entCalendario_destroy': self.salirCalendar,
               'on_entCalendario_day_selected_double_click': self.guardarfecha,
               'on_treeclientes_cursor_changed': self.seleccionarCLiente,
               'on_treefacturas_cursor_changed': self.seleccionarFactura,
               'on_treeservicios_cursor_changed': self.seleccionarServicio,
               'on_chkAceite_toggled': self.inizializarservicioAceite,
               'on_chkNeumo_toggled': self.inizializarservicioNeumo,
               'on_irToolbarDialog_activate': self.abrirDialog,
               'on_btnSalirDialog_clicked': self.salirDialog,
               'on_btnLimpiar_clicked': self.limpiarCampos,
               'on_zipBBDDToolbar_activate': self.comprimir,
               }

        b.connect_signals(dic)
        self.venCalendario.connect('delete-event', lambda w, e: w.hide() or True)
        datos
        self.venprincipal.show()
        datos.cargarClientes(self.listclientes, self.treeclientes)
        numero = datos.cargarFacturas(self.listfacturas, self.treefacturas)
        datos.cargaServicios(self.listservicios, self.treeservicios)
        self.lblResultadoFac.set_text(str(numero + 1))
        # self.venprincipal.maximize()

    # Cargamos el tema oscuro para nuestra app
    def set_style(self):
        provider = Gtk.CssProvider()
        provider.load_from_path(join(WHERE_AM_I, 'gtk-dark.css'))
        screen = Gdk.Display.get_default_screen(Gdk.Display.get_default())
        GTK_STYLE_PROVIDER_PRIORITY_APPLICATION = 600
        Gtk.StyleContext.add_provider_for_screen(
            screen, provider,
            GTK_STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def limpiarCampos(self, witget, Data=None):
        panel=self.notebook.get_current_page()

        if panel == 0:
            self.limpiarServ()
            datos.cargaServicios(self.listservicios,self.treeservicios)
        if panel == 1:
            self.limpiarcli()
            datos.cargarClientes(self.listclientes,self.treeclientes)
        if panel == 2:
            self.limpiarFactu()
            datos.cargarFacturas(self.listfacturas,self.treefacturas)

    def inizializarservicioAceite(self, witget, Data=None):
        self.edLitros.set_text('')

    def inizializarservicioNeumo(self, witget, Data=None):
        self.cmboxNeuma.current(1)

    def seleccionarCLiente(self, witget, Data=None):
        model, iter = self.treeclientes.get_selection().get_selected()

        if iter != None:
            sdni = model.get_value(iter, 0)
            matri = model.get_value(iter, 1)
            sapel = model.get_value(iter, 2)
            snome = model.get_value(iter, 3)
            email = model.get_value(iter, 4)
            movil = model.get_value(iter, 5)
            sfecha = model.get_value(iter, 6)
            self.entdni.set_text(sdni)
            self.entmat.set_text(matri)
            self.entapel.set_text(sapel)
            self.entnome.set_text(snome)
            self.entmail.set_text(email)
            self.entmovil.set_text(movil)
            self.entradafecha.set_text(sfecha)
            self.edMatriculaFac.set_text(matri)
            datos.CargarDatosUnCliente(self.listfacturas,self.treefacturas,self.listservicios,self.treeservicios,matri)


    def seleccionarFactura(self, witget, Data=None):
        model, iter = self.treefacturas.get_selection().get_selected()

        if iter != None:
            nfactura = model.get_value(iter, 0)
            matricula = model.get_value(iter, 1)
            fecha = model.get_value(iter, 2)
            self.lblResultadoFac.set_text(str(nfactura))
            self.edMatriculaFac.set_text(matricula)
            self.fechaFac.set_text(fecha)
            self.entFactu.set_text(str(nfactura))

    def seleccionarServicio(self, witget, Data=None):
        model, iter = self.treeservicios.get_selection().get_selected()

        if iter != None:
            manodeobra = model.get_value(iter, 0)
            bateria = model.get_value(iter, 1)
            aceite = model.get_value(iter, 2)
            filtro = model.get_value(iter, 3)
            neumatico = model.get_value(iter, 4)
            pastilla = model.get_value(iter, 5)
            numeroFactura = model.get_value(iter, 6)
            self.codigoVenta = model.get_value(iter, 7)
            self.entManoObra.set_text(str(manodeobra))

            if str(bateria) == "si":
                self.chkBateria.set_active(True)
            else:
                self.chkBateria.set_active(False)

            if str(aceite) == "0.0":
                self.chkAceite.set_active(False)
                self.edLitros.set_text("")
            else:
                self.chkAceite.set_active(True)
                self.edLitros.set_text(str(aceite))

            if pastilla == "DELANTEROS":
                self.chkPasti.set_active(True)
                self.cmboxPasti.set_active(0)
            elif pastilla == "TRASEROS":
                self.chkPasti.set_active(True)
                self.cmboxPasti.set_active(1)
            elif pastilla == "AMBOS":
                self.chkPasti.set_active(True)
                self.cmboxPasti.set_active(2)
            else:
                self.chkPasti.set_active(False)

            if neumatico == "DELANTEROS":
                self.chkNeumo.set_active(True)
                self.cmboxNeuma.set_active(0)
            elif neumatico == "TRASEROS":
                self.chkNeumo.set_active(True)
                self.cmboxNeuma.set_active(1)
            elif neumatico == "AMBOS":
                self.chkNeumo.set_active(True)
                self.cmboxNeuma.set_active(2)
            else:
                self.chkNeumo.set_active(False)

            if filtro == "AIRE":
                self.chkFiltro.set_active(True)
                self.cmboxFiltro.set_active(0)
            elif filtro == "ACEITE":
                self.chkFiltro.set_active(True)
                self.cmboxFiltro.set_active(1)
            elif filtro == "GASOLINA":
                self.chkFiltro.set_active(True)
                self.cmboxFiltro.set_active(2)
            else:
                self.chkFiltro.set_active(False)
            self.entFactu.set_text(str(numeroFactura))

    def abrirCalendar(self, widget, data=None):
        self.venCalendario.show()

    def salirCalendar(self, widget, data=None):
        self.venCalendario.hide()

    def abrirDialog(self, widget, data=None):
        self.venDialog.show()

    def salirDialog(self, widget, data=None):
        self.venDialog.hide()

    def guardarfecha(self, widget, data=None):

        panel = self.notebook.get_current_page()
        # obtenemos el panel actual
        if panel == 1:
            # Capturar los datos del calendario y presentarlos en las etiquetas
            agno, mes, dia = self.calendario.get_date()
            texto_agno = "Año:  %s" % agno
            texto_mes = "Mes: %s" % self.meses[mes]
            texto_dia = "Dia: %s" % dia
            fechafinal = (texto_dia + " " + texto_mes + " " + texto_agno)
            self.entradafecha.set_text(fechafinal)
            self.venCalendario.hide()

        if panel == 2:
            # Capturar los datos del calendario y presentarlos en las etiquetas
            agno, mes, dia = self.calendario.get_date()
            texto_agno = "Año:  %s" % agno
            texto_mes = "Mes: %s" % self.meses[mes]
            texto_dia = "Dia: %s" % dia
            fechafinal = (texto_dia + " " + texto_mes + " " + texto_agno)
            self.fechaFac.set_text(fechafinal)
            self.venCalendario.hide()

    def salir(self, widget, data=None):
        datos.cerrarConexion()
        Gtk.main_quit()

    def alta(self, widget, data=None):

        panel = self.notebook.get_current_page()
        # obtenemos el panel actual
        if panel == 0:
            self.entManoObra2 = self.entManoObra.get_text()
            self.entFactu2 = self.entFactu.get_text()

            if self.chkBateria.get_active():
                self.bateria2 = "si"
            else:
                self.bateria2 = "no"

            if self.chkAceite.get_active():
                self.edLitros2 = self.edLitros.get_text().upper()

            else:
                self.edLitros2 = "0"

            if self.chkNeumo.get_active():
                self.cmboxNeuma2 = self.cmboxNeuma.get_active_text().upper()

            else:
                self.cmboxNeuma2 = "No"

            if self.chkPasti.get_active():
                self.cmboxPasti2 = self.cmboxPasti.get_active_text().upper()

            else:
                self.cmboxPasti2 = "No"

            if self.chkFiltro.get_active():
                self.cmboxFiltro2 = self.cmboxFiltro.get_active_text().upper()

            else:
                self.cmboxFiltro2 = "No"

            if self.entFactu2 != '' and self.entManoObra2 != '':
                self.fila = (self.entManoObra2, self.bateria2, self.edLitros2, self.cmboxFiltro2, self.cmboxNeuma2,
                             self.cmboxPasti2, self.entFactu2)
                datos.altaServicios(self.fila)
                datos.cargaServicios(self.listservicios, self.treeservicios)
                self.limpiarServ()
                self.lblaviso.set_text("Servicio: " + self.entFactu2 + " dado de alta")

            else:
                self.lblaviso.set_text("Faltan datos")

        elif panel == 1:
            self.dni = self.entdni.get_text().upper()
            self.mat = self.entmat.get_text().upper()
            self.apel = self.entapel.get_text().title()
            self.nome = self.entnome.get_text().title()
            self.mail = self.entmail.get_text()
            self.movil = self.entmovil.get_text()
            self.fecha = self.entradafecha.get_text()

            valido = self.validoDNI(self.dni)

            if valido:
                if self.mail == '':
                    if self.dni != '' and self.mat != '' and self.apel != '':
                        self.fila = (self.dni, self.mat, self.apel, self.nome, self.mail, self.movil, self.fecha)
                        datos.altaCliente(self.fila)
                        datos.cargarClientes(self.listclientes, self.treeclientes)
                        # GestionClientes.altacli(self.treeclientes, self.listclientes, self.fila)
                        self.limpiarcli()
                        self.lblaviso.set_text("Cliente: " + self.mat + " dado de alta")

                    else:
                        self.lblaviso.set_text("Faltan datos")
                else:
                    valido2 = self.validarEmail(self.mail)
                    if valido2:
                        if self.dni != '' and self.mat != '' and self.apel != '':
                            self.fila = (self.dni, self.mat, self.apel, self.nome, self.mail, self.movil, self.fecha)
                            datos.altaCliente(self.fila)
                            datos.cargarClientes(self.listclientes, self.treeclientes)
                            # GestionClientes.altacli(self.treeclientes, self.listclientes, self.fila)
                            self.limpiarcli()
                            self.lblaviso.set_text("Cliente: " + self.mat + " dado de alta")

                        else:
                            self.lblaviso.set_text("Faltan datos")
                    else:
                        self.lblaviso.set_text("EMAIL NO VALIDO")
            else:
                self.lblaviso.set_text("DNI NO VALIDO")

        elif panel == 2:
            matfac = self.edMatriculaFac.get_text().upper()
            fechfac = self.fechaFac.get_text()

            if matfac != '' and fechfac != '':
                self.fila = (fechfac, matfac)
                datos.altaFactura(self.fila)
                numero = datos.cargarFacturas(self.listfacturas, self.treefacturas)
                self.lblResultadoFac.set_text(str(numero + 1))
                self.limpiarFactu()
                self.lblaviso.set_text("Factura: " + self.mat + " dada de alta")

            else:
                self.lblaviso.set_text("Faltan datos")

    def validoDNI(self, dni):

        tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
        dig_ext = "XYZ"
        reemp_dig_ext = {'X': '0', 'Y': '1', 'Z': '2'}
        numeros = "1234567890"
        dni = str(dni).upper()
        # dni="12345678Z"
        if len(dni) == 9:
            dig_control = dni[8]
            dni = dni[:8]
            if dni[0] in dig_ext:
                dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
            return len(dni) == len([n for n in dni if n in numeros]) and tabla[int(dni) % 23] == dig_control
        return False

    def validarEmail(self, mail):
        if re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$', self.mail.lower()):
            return True
        else:
            return False

    def modificar(self, widget, data=None):

        panel = self.notebook.get_current_page()
        if panel == 0:
            self.entManoObra2 = self.entManoObra.get_text()
            self.entFactu2 = self.entFactu.get_text()

            if self.chkBateria.get_active():
                self.bateria2 = "si"
            else:
                self.bateria2 = "no"

            if self.chkAceite.get_active():
                self.edLitros2 = self.edLitros.get_text().upper()

            else:
                self.edLitros2 = "0"

            if self.chkNeumo.get_active():
                self.cmboxNeuma2 = self.cmboxNeuma.get_active_text().upper()

            else:
                self.cmboxNeuma2 = "No"

            if self.chkPasti.get_active():
                self.cmboxPasti2 = self.cmboxPasti.get_active_text().upper()

            else:
                self.cmboxPasti2 = "No"

            if self.chkFiltro.get_active():
                self.cmboxFiltro2 = self.cmboxFiltro.get_active_text().upper()

            else:
                self.cmboxFiltro2 = "No"

            if datos.comprobarEntero(self.entManoObra2) and datos.comprobarEntero(self.edLitros2):
                if self.entFactu2 != '' and self.entManoObra2 != '':

                    self.fila = (round(self.entManoObra2,2), self.bateria2, round(self.edLitros2,2), self.cmboxFiltro2, self.cmboxNeuma2,
                                 self.cmboxPasti2, self.codigoVenta)
                    datos.modificarServicio(self.fila)
                    datos.cargaServicios(self.listservicios, self.treeservicios)
                    self.limpiarServ()
                    self.lblaviso.set_text("Servicio: " + str(self.entFactu) + " dado de alta")

                else:
                    self.lblaviso.set_text("Faltan datos")
            else:
                self.lblaviso.set_text("Introduce numeros en mano de obra y litros.")

        if panel == 1:
            self.dni = self.entdni.get_text().upper()
            self.mat = self.entmat.get_text().upper()
            self.apel = self.entapel.get_text().title()
            self.nome = self.entnome.get_text().title()
            self.mail = self.entmail.get_text()
            self.movil = self.entmovil.get_text()
            self.fecha = self.entradafecha.get_text()

            valido = self.validoDNI(self.dni)

            if valido:
                if self.mail == '':
                    if self.dni != '' and self.mat != '' and self.apel != '':
                        self.fila = (self.dni, self.mat, self.apel, self.nome, self.mail, self.movil, self.fecha)
                        datos.modificarCliente(self.fila)
                        datos.cargarClientes(self.listclientes, self.treeclientes)
                        # GestionClientes.altacli(self.treeclientes, self.listclientes, self.fila)
                        self.limpiarcli()
                        self.lblaviso.set_text("Cliente: " + self.mat + " dado de alta")

                    else:
                        self.lblaviso.set_text("Faltan datos")
                else:
                    valido2 = self.validarEmail(self.mail)
                    if valido2:
                        if self.dni != '' and self.mat != '' and self.apel != '':
                            self.fila = (self.dni, self.mat, self.apel, self.nome, self.mail, self.movil, self.fecha)
                            datos.modificarCliente(self.fila)
                            datos.cargarClientes(self.listclientes, self.treeclientes)
                            # GestionClientes.altacli(self.treeclientes, self.listclientes, self.fila)
                            self.limpiarcli()
                            self.lblaviso.set_text("Cliente: " + self.mat + " dado de alta")

                        else:
                            self.lblaviso.set_text("Faltan datos")
                    else:
                        self.lblaviso.set_text("EMAIL NO VALIDO")
            else:
                self.lblaviso.set_text("DNI NO VALIDO")

            self.lblaviso.set_text("Cliente modificado - Recuerda que no puedes cambiar el DNI")

        if panel == 2:
            fechacargada = self.fechaFac.get_text()
            matfac = self.edMatriculaFac.get_text().upper()
            print(self.lblResultadoFac)

            if matfac != '' and fechacargada != '':
                self.fila = (self.lblResultadoFac.get_text(), fechacargada, matfac)
                datos.modificarFactura(self.fila)
                datos.cargarFacturas(self.listfacturas, self.treefacturas)
                self.limpiarFactu()
                self.lblaviso.set_text("Factura: " + self.matfac + " modificada")

            else:
                self.lblaviso.set_text("Faltan datos")

            self.lblaviso.set_text("Fecha de la factura modificada")

    def baja(self, widget, data=None):

        panel = self.notebook.get_current_page()
        if panel == 0:
            datos.BorrarServicio(self.codigoVenta)
            datos.cargaServicios(self.listservicios, self.treeservicios)
            self.limpiarServ()
            self.lblaviso.set_text("Servicio dado de baja")

        if panel == 1:
            self.dni = self.entdni.get_text().upper()
            self.borradoClienteCascade()
            datos.BorrarCliente(self.dni)
            datos.cargarClientes(self.listclientes, self.treeclientes)
            self.limpiarcli()
            self.lblaviso.set_text("Cliente dado de baja")

        if panel == 2:
            ressssfac =self.lblResultadoFac.get_text()
            datos.BorrarFactura(ressssfac,)
            datos.cargaServicios(self.listservicios,self.treeservicios)
            datos.cargarFacturas(self.listfacturas, self.treefacturas)
            self.limpiarFactu()
            self.lblaviso.set_text("No se puede dar de baja un cliente")

    def borradoClienteCascade (self):
        datos.BorrarFacturaCliente(self.entmat.get_text().upper(), )
        datos.cargaServicios(self.listservicios, self.treeservicios)
        datos.cargarFacturas(self.listfacturas, self.treefacturas)
        self.limpiarcli()
        self.lblaviso.set_text("No se puede dar de baja un cliente")

    def limpiarcli(self):
        self.limpiarfilas = (
            self.entdni, self.entmat, self.entapel, self.entnome, self.entmail, self.entmovil, self.entradafecha)
        GestionClientes.limpiarclie(self.limpiarfilas)

    def limpiarServ(self, data=None):
        self.limpiarServiciosLabel = (self.entManoObra, self.edLitros, self.entFactu)
        self.limpiarServiciosCheck = (self.chkBateria, self.chkFiltro, self.chkNeumo, self.chkPasti, self.chkAceite)
        self.limpiarServiciosCombo = (self.cmboxFiltro, self.cmboxNeuma, self.cmboxPasti)
        GestionClientes.limpiarServ(self.limpiarServiciosLabel, self.limpiarServiciosCheck, self.limpiarServiciosCombo)

    def limpiarFactu(self, data=None):
        self.limpiarfilas = (self.lblResultadoFac, self.edMatriculaFac, self.fechaFac)
        GestionClientes.limpiarFac(self.limpiarfilas)

    def comprimir(self, widget, data = None):

             #If para comprobar si existe en mi carpeta personal una carpeta que ya se llama copias
             #si no existe la crea en la instruccion mkdir
             if not os.path.exists('/home/' + getpass.getuser() + '/copias'):
                os.mkdir('/home/' + getpass.getuser() + '/copias', mode=0o777, dir_fd=None)

             #comento esta linea pues es la version simple de la de arriba, guardaria la copia
             #en la misma carpeta del proyecto
             fichzip = zipfile.ZipFile("copia.zip", "w")
             fichzip.write("database","./database", zipfile.ZIP_DEFLATED)
             fichzip.close()



if __name__ == '__main__':
    main = Cliente()
    Gtk.main()
