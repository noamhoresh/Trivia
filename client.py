import socket
from chatlib_skeleton import *  # To use chatlib functions or consts, use chatlib.****

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678


# HELPER SOCKET METHODS

def build_and_send_message(conn, code, msg):
    """
    Builds a new message using chatlib, wanted code and message.
    Prints debug info, then sends it to the given socket.
    Paramaters: conn (socket object), code (str), msg (str)
    Returns: Nothing
    """


# Implement Code

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
    # Implement Code
    pass
    return socket


def error_and_exit(msg):
    # Implement code
    pass


def login(conn):
    username = input("Please enter username: \n")
    # Implement code

    build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["logout_msg"], "")


# Implement code

pass


def logout(conn):
    # Implement code
    pass


def main():
    # Implement code
    pass


if __name__ == '__main__':
    main()