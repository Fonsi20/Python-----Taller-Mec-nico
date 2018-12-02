

def altacli(treeclientes,listclientes,fila):
    listclientes.append(fila)
    treeclientes.show()

def altaServicios(treeservicios,listservicios,fila):
    listservicios.append(fila)
    treeservicios.show()

def altaFactura(treefacturas,listfacturas,fila):
    listfacturas.append(fila)
    treefacturas.show()

def limpiarclie(listalimpiar):
    for fila in listalimpiar:
        fila.set_text('')

def limpiarServ(listalimpiarlabel,listalimpiarchk,lislalimpiarcombo):
    for fila in listalimpiarlabel:
        fila.set_text('')

    for fila in listalimpiarchk:
        fila.set_active(False)

    for fila in lislalimpiarcombo:
        fila.set_active(-1)

def limpiarFac(listalimpiar):
    for fila in listalimpiar:
        fila.set_text('')