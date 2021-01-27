import socket
from chatlib_skeleton import *  # To use chatlib functions or consts, use chatlib.****

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678
# a way to verify proccesses with the server's and the client's protocols
KEY_LIST = list(PROTOCOL_SERVER.keys())    
VAL_LIST = list(PROTOCOL_SERVER.values())
# ---------------exc 2-----------------
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
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# defining the socket
    my_socket.connect(("127.0.0.1", 5678))# connect to the server
    # server_socket.listen()# the time it listen to client until closing the socket
    print("Connected to server on port %d" % SERVER_PORT)
    return my_socket


def error_and_exit(msg):
    print(msg)
    exit()


def login(conn):
    """login the client to the server keeps runing until succeeds

    Args:
        conn (socket)
    """
    print("Login...")
    cnfrm = "start"
    
    while cnfrm != "login_ok_msg":
        if cnfrm != "start":
            print("Wrong username or password please try again!")
        username = input("Please enter username: \n")
        password = input("Please enter password: \n")
        data = username + '#' + password  # used for the protocol
        build_and_send_message(conn, PROTOCOL_CLIENT["login_msg"], data)
        print("Data: " + data)
        answer = conn.recv(2048).decode()# get the answer from the server
        answer_cmd = split_msg(answer)[0]# takes the specific command
        cnfrm = KEY_LIST[VAL_LIST.index(answer_cmd)]# finds the matching key to the answer value
    
    print("Login succeed")



def logout(conn):
    print("Logging out...")
    build_and_send_message(conn, PROTOCOL_CLIENT["logout_msg"], "")


# ---------------exc 3-----------------
def build_send_recv_parse(conn, cmd, data):
    """send a message to the server and return his response

    Args:
        conn (socket):connection to the server
        cmd (str): the protocol's command
        data (str): the protocol's data

    Returns:
        msg_code(str): the server's response's command
        msg(str): the server's response's data
    """
    build_and_send_message(conn, cmd, data)
    msg_code, msg = recv_message_and_parse(conn)
    return msg_code, msg


def get_score(conn):
    """ask for the current player's score, prints if succeeds or not

    Args:
        conn (socket)
    """
    print("Getting score...")
    cmd, data = build_send_recv_parse(conn, PROTOCOL_CLIENT["get_score_msg"], "")
    if KEY_LIST[VAL_LIST.index(cmd)] == "score_ok_msg":
        print(f'Your current score is: {data}')
    else:
        print("The system could not find your score")


def main():
    conn_sock = connect()
    print("Connected...")
    login(conn_sock)
    options = -1# if the client wants to continue playing
    
    while options != 0:
        options = int(input("For logout press: 0 \nFor getting your score press: 1\n"))
        if options == 1:
            get_score(conn_sock)

    logout(conn_sock)


if __name__ == '__main__':
    main()
