import socket
import time
import random

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 8820))
server_socket.listen()
print("Server is up and running")

(client_socket, client_address) = server_socket.accept()
print("Client connected")

while True:
    data = client_socket.recv(1024).decode()
    print("Client sent: " + data)
    if data == "Quit":
        print("Closing client socket now...")
        client_socket.send("Bye".encode())
        break
    elif data == "NAME":
        ret = "My name is Shachar :)"
        client_socket.send(ret.encode())
    elif data == "TIME":
        ret = "The current time is: " + time.asctime()
        client_socket.send(ret.encode())
    elif data == "RAND":
        ret = "Your random number is: " + str(random.uniform(1,10))
        client_socket.send(ret.encode())
    else:
        ret = "Invalid input! Pleas try again"
        client_socket.send(ret.encode())

client_socket.close()
server_socket.close()
