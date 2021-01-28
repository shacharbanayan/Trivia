import socket
import chatlib  # To use chatlib functions or consts, use chatlib.****

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678


# HELPER SOCKET METHODS

def build_and_send_message(conn, code, data):
    """
    Builds a new message using chatlib, wanted code and message.
    Prints debug info, then sends it to the given socket.
    INPUT: conn (socket object), code (str), data (str)
    OUTPUT: Nothing
    """
    msg = chatlib.build_message(code, data)
    # print(msg)
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
    return cmd, data

def connect():
    """
    Creates a socket and makes connection to the server IP and port
    INPUT: NULL
    OUTPUT: a socket connected to the server
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))
    return client_socket

def error_and_exit(error_msg):
    """
    Exit the program due to an error and prints an error massage
    INPUT: the error massage
    OUTPUT: nothing
    """
    print(error_msg)
    exit()
    pass

def login(conn):
    """
    Loges the user to the system. Doesn't return till successful login is made.
    INPUT: conn (socket object)
    OUTPUT: nothing
    """
    username = input("Please enter username: \n")
    password = input("Please enter password: \n")
    while True:
        code = chatlib.PROTOCOL_CLIENT["login_msg"]
        data = username+'#'+password
        build_and_send_message(conn, code, data)
        cmd, data = recv_message_and_parse(conn)
        if cmd == "LOGIN_OK":
            print("Logged in!")
            return
        else:
            username = input("Wrong username or passward.\nPlease reenter username: \n")
            password = input("Please enter password: \n")

def logout(conn):
    """
    Loges the user out of the system.
    INPUT: conn (socket object)
    OUTPUT: nothing
    """
    build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["logout_msg"], "")
    print("Goodbye!")

def build_send_recv_parse(conn, cmd, data):
    """

    """
    build_and_send_message(conn, cmd, data)
    msg_code, msg_data = recv_message_and_parse(conn)
    return msg_code, msg_data

def get_score(conn):
    """

    """
    msg_code, msg_data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["my_score_msg"], "")
    if msg_code == chatlib.PROTOCOL_SERVER["my_score_ans"]:
        print("Your score is: " + msg_data)
    else:
        print("There was an error in GET_SCORE")
        return

def get_highscore(conn):
    """

    """
    msg_code, msg_data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["get_highest_score_msg"], "")
    if msg_code == chatlib.PROTOCOL_SERVER["get_highest_score_ans"]:
        print("The highest scores are:\n" + msg_data)
    else:
        print("There was an error in GET_HIGHSCORE")

def get_logged_users(conn):
    """

    """
    msg_code, msg_data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["who_is_logged_msg"], "")
    if msg_code == chatlib.PROTOCOL_SERVER["who_is_logged_ans"]:
        print("The users logged are: " + msg_data)
    else:
        print("There was an error in GET_LOGGED_USERS")

def play_questoin(conn):
    """

    """
    msg_code, msg_data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["get_question_msg"], "")
    if msg_code == chatlib.PROTOCOL_SERVER["no_questions_msg"]:
        print("No questions left in the game")
    elif msg_code == chatlib.PROTOCOL_SERVER["get_question_msg"]:
        data = chatlib.split_data(msg_data, 6)
        # print(data)
        id = data[0]
        print(data[1] + "\n")
        for i in range(2, len(data)):
            print("\t" + str(i-1) +". " + data[i]+"\n")
        answer = input("Please enter your answer: ")
        msg_code, msg_data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["send_answer_msg"], id + "#" + answer)
        if msg_code == chatlib.PROTOCOL_SERVER["correct_ans_msg"]:
            print("You are correct!\n")
        elif msg_code == chatlib.PROTOCOL_SERVER["wrong_ans_msg"]:
            print("Incorrect answer! The correct answer is " + msg_data +"\n")
        else:
            print("There was an error in CHECK_ANSWER")
            return
    else:
        print("There was an error in GET_QUESTION")
        return


def main():
    """
    The main function from where we will manage the game.
    INPUT: nothing
    OUTPUT: nothing
    """
    conn = connect()
    login(conn)
    while True:
        print("p\tPlay a trivia question\n"
              "s\tGet my score\n"
              "h\tGet high score\n"
              "l\tGet logged users\n"
              "q\tQuit\n")
        choice = input("Please enter your choice: ")
        if choice == "p":
            play_questoin(conn)
        elif choice == "s":
            get_score(conn)
        elif choice == "h":
            get_highscore(conn)
        elif choice == "l":
            get_logged_users(conn)
        elif choice == "q":
            break
        else:
            print("Invalide choise!\n")
    logout(conn)

if __name__ == '__main__':
    main()
