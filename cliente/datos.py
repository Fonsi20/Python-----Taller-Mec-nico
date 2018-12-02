import os
import sqlite3
import GestionClientes
import cliente


try:
    bbdd = 'database'
    conex = sqlite3.connect(bbdd)
    cur = conex.cursor()
    print('BASE DE DATOS CONECTADA')

except sqlite3.OperationalError as e:
    print(e)

def cerrarConexion():
    try:
        conex.commit()
        conex.close()
        print('cerrando base de datos')
    except sqlite3.OperationalError as e:
        print(e)


def altaCliente(fila):
    try:
        cur.execute("INSERT INTO CLIENTES(dni,matricula,apellidos,nombre,email,movil,calendario) values(?,?,?,?,?,?,?)", fila)
        conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conex.rollback()


def altaFactura(fila):
    try:
        cur.execute("INSERT INTO FACTURACION(matricula,fecha) values(?,?)", fila)
        conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conex.rollback()


def altaServicios(fila):
    try:
        cur.execute("INSERT INTO SERVICIOS(manodeobra,bateria,aceite,filtro,neumatico,pastilla,numerofactura) values(?,?,?,?,?,?,?)", fila)
        conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conex.rollback()

def modificarServicio(fila):
    try:
        cur.execute("UPDATE SERVICIOS "
                    "set manodeobra=? ,bateria=?,aceite=?,filtro=?,neumatico=?,pastilla=?"
                    "where codigoventa=?", (fila[0],fila[1],fila[2],fila[3],fila[4],fila[5],fila[6]))
        conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conex.rollback()

def modificarFactura(fila):
    try:
        print(fila)
        cur.execute("UPDATE FACTURACION "
                    "set fecha=? ,matricula=?"
                    "where idFactuacion=?", (fila[1],fila[2],fila[0]))
        conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conex.rollback()

def modificarCliente(listclientes,treeclientes):
    try:
        cur.execute("UPDATE CLIENTES "
                    "set matricula=? ,apellidos=?,nombre=?,email=?,movil=?,calendario=?"
                    "where dni=?", (fila[1],fila[2],fila[3],fila[4],fila[5],fila[6],fila[0]))
        conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conex.rollback()

def cargarClientes(listclientes,treeclientes):
    try:
        listclientes.clear()
        cur.execute("SELECT * FROM CLIENTES")
        cursor=cur.fetchall()
        for row in cursor:
         GestionClientes.altacli(treeclientes, listclientes, row)

    except sqlite3.OperationalError as e:
        print(e)

def CargarDatosUnCliente(listfactura,treefactura,listservicios,treeservicios,matri):
    try:
        listfactura.clear()
        listservicios.clear()
        cur.execute("SELECT * FROM FACTURACION where fecha=?",(matri,))
        cursor = cur.fetchall()
        for row in cursor:
            GestionClientes.altaFactura(treefactura, listfactura, row)

        idf = ""
        cur.execute("SELECT idFactuacion from FACTURACION where (fecha=?)", (matri,))
        conex.commit()
        for i in cur:
            idf = i[0]

        cur.execute("SELECT * FROM SERVICIOS where numerofactura=?", (idf,))
        cursor = cur.fetchall()
        for row in cursor:
            GestionClientes.altaServicios(treeservicios, listservicios, row)

    except sqlite3.OperationalError as e:
        print(e)

def cargarFacturas(listfacturas,treefacturas):
    try:
        listfacturas.clear()
        cur.execute("SELECT * FROM FACTURACION")
        cursor=cur.fetchall()
        for row in cursor:
         GestionClientes.altaFactura(treefacturas, listfacturas, row)

        cur.execute("select count(*) from facturacion")
        cursor = cur.fetchall()
        num = cursor[0]
        num = num[0]
        a = num
        return a
    except sqlite3.OperationalError as e:
        print(e)

def cargaServicios (listservicios,treeservicios):
    try:
        listservicios.clear()
        cur.execute("SELECT * FROM SERVICIOS")
        cursor=cur.fetchall()
        for row in cursor:
         GestionClientes.altaServicios(treeservicios, listservicios, row)
    except sqlite3.OperationalError as e:
        print(e)

def BorrarCliente(dni):
    try:
        cur.execute("DELETE FROM CLIENTES "
                    "where (dni=?)", (dni,))
        conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conex.rollback()

def BorrarServicio(codigoVenta):
    try:
        cur.execute("DELETE FROM SERVICIOS "
                    "where (codigoventa=?)", (codigoVenta,))
        conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conex.rollback()

def BorrarFactura(idfactura):
    try:
        cur.execute("DELETE FROM FACTURACION "
                    "where (idFactuacion=?)", (idfactura,))
        conex.commit()

        cur.execute("DELETE FROM SERVICIOS "
                    "where (numerofactura=?)", (idfactura,))
        conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conex.rollback()

def BorrarFacturaCliente(matricula):
    try:
        idf=""
        cur.execute("SELECT idFactuacion from FACTURACION where (fecha=?)",(matricula,))
        conex.commit()
        for i in cur:
            idf =i[0]

        cur.execute("DELETE FROM SERVICIOS "
                    "where (numerofactura=?)", (idf,))
        conex.commit()

        cur.execute("DELETE FROM FACTURACION "
                    "where (fecha=?)", (matricula,))
        conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conex.rollback()


def comprobarEntero(numero):
        try:
            valor = int(numero)
            return True
        except ValueError:
            return False