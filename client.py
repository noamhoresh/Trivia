import socket
from chatlib_skeleton import *  # To use chatlib functions or consts, use chatlib.****

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678

"""
Builds a new message using chatlib, wanted code and message. 
Prints debug info, then sends it to the given socket.
Paramaters: conn (socket object), code (str), msg ( .str)
Returns: Nothing
"""


def build_and_send_message(conn, code, msg):
    message = build_message(code, msg)
    conn.send(message.encode())


"""
Recieves a new message from given socket.
Prints debug info, then parses the message using chatlib.
Paramaters: conn (socket object)
Returns: cmd (str) and data (str) of the received message.
If error occured, will return None, None
"""


def recv_message_and_parse(conn):

    data = conn.recv(2048).decode()
    print("Server Response: " + data)
    cmd, msg = parse_message(data)

    if cmd is None:
        print("Problem Occurred")

    return cmd, msg


def connect():
    """connect the client to the server
    Returns:
        socket[socket]:
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# defining the socket
    server_socket.bind((SERVER_IP, SERVER_PORT))# setting the current ip and port
    server_socket.listen()# the time it listen to client until closing the socket
    print("Listening for connections on port %d" % SERVER_PORT)
    socket, client_address = server_socket.accept()# accept the request
    return socket


def error_and_exit(msg):
    print(msg)
    exit()


def login(conn):
    print("Login...")
    username = input("Please enter username: \n")
    password = input("Please enter password: \n")
    data = username + '#' + password  # used for the protocol

    message = build_message('LOGIN', data)
    print("Msg: " + message)
    # conn.send(message.encode())

    build_and_send_message(conn, PROTOCOL_CLIENT["logout_msg"], "")


def logout(conn):
    print("Logout...")
    build_and_send_message(conn, PROTOCOL_CLIENT["logout_msg"], "")


def main():
    conn_sock = connect()
    print("One Player Connected")
    login(conn_sock)
    logout(conn_sock)


if __name__ == '__main__':
    main()
