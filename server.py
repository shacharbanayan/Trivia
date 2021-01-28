import socket
import select

SERVER_IP = "0.0.0.0"
SERVER_PORT = 5555
MAX_MSG_SIZE = 1024

def main():
    print("Setting up server...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen()
    print("Listening for clients...")
    client_sockets = []
    messeges_to_send = []
    while True:
        ready_to_read, ready_to_write, in_error = select.select([server_socket]+client_sockets, client_sockets, [])
        for current_socket in ready_to_read:
            if current_socket is server_socket:
                (client_socket, client_address) = current_socket.accept()
                print("New client joined!", client_address)
                client_sockets.append(client_socket)
                print_client_sockets(client_sockets)
            else:
                try:
                    print("New data from client")
                    data = current_socket.recv(MAX_MSG_SIZE).decode()
                except:
                    client_sockets.remove(current_socket)
                    current_socket.close()
                    print("One of the clients failed, The clients connected are:")
                    print_client_sockets(client_sockets)
                if data == "":
                    print("Connection closed", )
                    client_sockets.remove(current_socket)
                    current_socket.close()
                    print_client_sockets(client_sockets)
                else:
                    messeges_to_send.append((current_socket, data))
        for messege in messeges_to_send:
            current_socket , data = messege
            if current_socket in ready_to_write:
                current_socket.send(data.encode())
                messeges_to_send.remove(messege)



def print_client_sockets(client_sockets):
    for c in client_sockets:
        print("\t", c.getpeername())

main()