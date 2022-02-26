import socket
from threading import Thread

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

host = "10.0.0.67"
port = 9999

server.bind((host, port))
server.listen(100)

list_of_clients = []
names = {}

def clientthread(conn, addr):
    while True:
        try:
            message = conn.recv(2048).decode()
            if message[:7] == "!name: ":
                name = message[7:]
                names[conn] = name
                message = "\n" + name + " has joined the chat!" + "\n"
                print(message)
                broadcast(message, conn)
            else:
                message_to_send = names[conn] + ": " + message
                broadcast(message_to_send, conn)
        except:
            message = "\n" + names[conn] + " has left the chat!" + "\n"
            broadcast(message, conn)
            del names[conn]
            conn.close()
            remove(conn)


def broadcast(message, connection):
    for clients in list_of_clients:
        if clients != connection:
            try:
                clients.send(message.encode())
            except:
                clients.close()
                remove(clients)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

while True:
    conn, addr = server.accept()

    list_of_clients.append(conn)
    print(addr[0] + " connected")

    t = Thread(target=clientthread, args=(conn, addr))
    t.daemon = True
    t.start()

conn.close()
server.close()