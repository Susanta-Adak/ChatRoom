import socket
import threading

HOST = 'localhost'
PORT = 8002

clients = []
names = []
connections = {}

# function to handle incoming messages from a client
def handle_client(conn, addr):
    print(f"New connection from {addr[0]}:{addr[1]}")
    #---------
    sender_name = conn.recv(1024).decode('utf-8')
    names.append(sender_name)

    recever_name = conn.recv(1024).decode('utf-8')
    client_to = ""
    client_from = ""

    is_busy = False
    while True:
        if recever_name in names and recever_name != sender_name:
            index_to = names.index(recever_name)
            client_to = clients[index_to]

            index_from = names.index(sender_name)
            client_from = clients[index_from]

            print(connections, client_from)

            # available condition
            if recever_name not in connections.keys() or recever_name in connections.keys() and connections[recever_name] == sender_name:
                connections[sender_name] = recever_name
                if recever_name in names:
                    ok_message = sender_name + " is now available."
                    client_to.sendall(ok_message.encode('utf-8'))

            # busy condition
            elif recever_name in connections.keys() and connections[recever_name] != sender_name:
                busy_message = recever_name+" is busy with other."
                client_from.sendall(busy_message.encode('utf-8'))
                is_busy = True
                while is_busy:
                    if recever_name not in connections.keys():
                        is_busy = False
                        continue

            break
    
    while True:
        data = conn.recv(1024).decode('utf-8')
        if data == "exit":
            del connections[client_from]
            del connections[client_to]
        if not data:
            print(f"{addr[0]}:{addr[1]} disconnected")
            break 
        print(f"Message from {addr[0]}:{addr[1]} - {data}")
        
        if client_to != conn:
            data = sender_name +" : "+ data
            client_to.sendall(data.encode('utf-8'))

    clients.remove(conn)
    conn.close()
        

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Server started on {HOST}:{PORT}")

while True:
    conn, addr= server_socket.accept()
    clients.append(conn)

    client_thread = threading.Thread(target=handle_client, args=(conn, addr))
    client_thread.start()
    