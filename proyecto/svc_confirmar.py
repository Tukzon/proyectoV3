#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('socket', 5000)
server.connect(server_address)
server.send(bytes('00010sinitconde','utf-8'))

def fill(data):
    data = str(data)
    aux = str(len(data))
    while len(aux) < 5:
        aux = '0' + aux
    return aux

print("Iniciado servicio de confirmacion de despachos")
recibido=server.recv(4096)

while True:
    datos=server.recv(4096)
    if datos.decode('utf-8').find('conde')!=-1:
        datos = datos[10:]
        target = datos.decode()
        data = target.split()
        session_mail = data[0]
        idDesp = data[1]

        query = "UPDATE despachos SET estado = '1' WHERE id = '" + idDesp
        query = query.replace(" ", "-")
        conde_data = "confirmar "+query

        aux = fill(len(conde_data+ 'dbset'))
        msg = aux + 'dbset' + conde_data

        server.sendall(bytes(msg,'utf-8'))
        recibido=server.recv(4096)
        if recibido.decode('utf-8').find('dbset')!=-1:
            recibido = recibido[12:]
            if recibido.decode('utf-8') == 'confirmado':
                print("Despacho confirmado")
                server.sendall(bytes('00010conde1','utf-8'))
            elif recibido.decode('utf-8') == 'fallo_confirmacion':
                print("Error al confirmar despacho")
                server.sendall(bytes('00010conde0','utf-8'))
