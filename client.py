import socket
import threading

HOST = 'localhost'
PORT = 8002

#incoming messages
def receive_messages(sock):
    while True:
        data = sock.recv(1024).decode('utf-8')
        print(f"{data}")


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Enter your name and your friend name: ")
client_socket.connect((HOST, PORT))

receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
receive_thread.start()

while True:
    message = input()
    if message == "exit":
        break
    client_socket.sendall(message.encode('utf-8'))
