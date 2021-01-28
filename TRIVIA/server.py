##############################################################################
# server.py
##############################################################################

import socket
import chatlib
import select



# GLOBALS
users = {"test" : "test"}
questions = {}
logged_users = {} # a dictionary of client hostnames to usernames - will be used later

ERROR_MSG = "Error! "
SERVER_PORT = 5678
SERVER_IP = "127.0.0.1"
MAX_MSG_SIZE = 1024

# HELPER SOCKET METHODS

def build_and_send_message(conn, code, data):
    """
    Builds a new message using chatlib, wanted code and message.
    Prints debug info, then sends it to the given socket.
    INPUT: conn (socket object), code (str), data (str)
    OUTPUT: Nothing
    """
    msg = chatlib.build_message(code, data)
    print("[SERVER]", conn.getpeername()," msg: ", msg)
    conn.send(msg.encode())


def recv_message_and_parse(conn):
    """
    Recieves a new message from given socket, then parses the message using chatlib.
    INPUT: conn (socket object)
    OUTPUT: cmd (str) and data (str) of the received message.
            If error occured, will return None, None
    """
    full_msg = conn.recv(1024).decode()
    cmd, data = chatlib.parse_message(full_msg)
    print("[CLIENT] ", conn.getpeername(), " msg: ", full_msg)  # Debug print
    return cmd, data

# Data Loaders #

def load_questions():
    """
    Loads questions bank from file	## FILE SUPPORT TO BE ADDED LATER
    Recieves: -
    Returns: questions dictionary
    """
    questions = {
                2313 : {"question":"How much is 2+2","answers":["3","4","2","1"],"correct":2},
                4122 : {"question":"What is the capital of France?","answers":["Lion","Marseille","Paris","Montpellier"],"correct":3}
                }

    return questions

def load_user_database():
    """
    Loads users list from file	## FILE SUPPORT TO BE ADDED LATER
    Recieves: -
    Returns: user dictionary
    """
    users = {
            "test"		:	{"password":"test","score":0,"questions_asked":[]},
            "yossi"		:	{"password":"123","score":50,"questions_asked":[]},
            "master"	:	{"password":"master","score":200,"questions_asked":[]}
            }
    return users


# SOCKET CREATOR

def setup_socket():
    """
    Creates new listening socket and returns it
    Recieves: -
    Returns: the socket object
    """
    # Implement code ...
    print("Setting up server...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen()
    print("Listening for clients...")
    return server_socket




def send_error(conn, error_msg):
    """
    Send error message with given message
    Recieves: socket, message error string from called function
    Returns: None
    """
    build_and_send_message(conn, chatlib.PROTOCOL_SERVER["login_failed_msg"], error_msg)




##### MESSAGE HANDLING


def handle_getscore_message(conn, username):
    global users
    # Implement this in later chapters


def handle_logout_message(conn):
    """
    Closes the given socket (in laster chapters, also remove user from logged_users dictioary)
    Recieves: socket
    Returns: None
    """
    global logged_users
    logged_users.remove(conn)
    conn.close()


def handle_login_message(conn, data):
    """
    Gets socket and message data of login message. Checks  user and pass exists and match.
    If not - sends error and finished. If all ok, sends OK message and adds user and address to logged_users
    Recieves: socket, message code and data
    Returns: None (sends answer to client)
    """
    global users  # This is needed to access the same users dictionary from all functions
    global logged_users	 # To be used later

    username, password = chatlib.split_data(data, 2)
    if username in users:
        if password == users[username]:
            build_and_send_message(conn, chatlib.PROTOCOL_SERVER["login_ok_msg"], "")
        else:
            build_and_send_message(conn, chatlib.PROTOCOL_SERVER["error_msg"], "Wrong password!")
    else:
        build_and_send_message(conn, chatlib.PROTOCOL_SERVER["error_msg"], "Wrong username!")


def handle_client_message(conn, cmd, data):
    """
    Gets message code and data and calls the right function to handle command
    Recieves: socket, message code and data
    Returns: None
    """
    global logged_users	 # To be used later

    if cmd == chatlib.PROTOCOL_CLIENT["login_msg"]:
        handle_login_message(conn, data)
    elif cmd == chatlib.PROTOCOL_CLIENT["logout_msg"]:
        handle_logout_message(conn)
    else:
        build_and_send_message(conn, chatlib.PROTOCOL_SERVER["error_msg"], "Unknown command!")



def main():
    # Initializes global users and questions dicionaries using load functions, will be used later
    global users
    global questions
    server_socket = setup_socket()
    client_sockets = []
    messeges_to_handle = []
    print("Welcome to Trivia Server!")
    while True:
        ready_to_read, ready_to_write, in_error = select.select([server_socket] + client_sockets, client_sockets, [])
        for current_socket in ready_to_read:
            if current_socket is server_socket:
                (client_socket, client_address) = current_socket.accept()
                print("New client joined! ", client_address)
                client_sockets.append(client_socket)
            else:
                try:
                    # print("New data from client")
                    cmd, data = recv_message_and_parse(current_socket)
                    if data == "":
                        print("Connection to ", current_socket.getpeername() ,"closed")
                        client_sockets.remove(current_socket)
                        current_socket.close()
                        # print_client_sockets(client_sockets)
                    else:
                        messeges_to_handle.append((current_socket, cmd, data))
                except:
                    print("Connection to ", current_socket.getpeername() ,"closed")
                    client_sockets.remove(current_socket)
                    current_socket.close()

        for messege in messeges_to_handle:
            current_socket, cmd, data = messege
            if current_socket in ready_to_write:
                handle_client_message(current_socket, cmd, data)
                messeges_to_handle.remove(messege)


def print_client_sockets(client_sockets):
    for c in client_sockets:
        print("\t", c.getpeername())


if __name__ == '__main__':
    main()

