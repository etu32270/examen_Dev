import socket #pour la connection
import sys #pour les commandes systèmes

# Créer un socket pour initier une connection
def socket_creation():
    try:
        global host #variable global pour être utilisée plus tard dans une autre fonction
        global port
        global sock
        host = '' #l'ip ou le sever sera à l'écoute (lui même dans ce cas)
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

# Accepter la connection avec le client
def accept_socket():
    conn, address = sock.accept() #attendre que la connection se fasse et afficher le message qui suit avec les infos sur l'ip et le port du client
    print("Connection established on " + "IP " + address[0] + ":" + str(address[1]))
    send_commands(conn) #Fonction qui permettra d'envoyer des commandes
    conn.close()

