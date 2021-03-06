# imports
import socket
from chatlib_skeleton import *  # To use chatlib functions or consts, use chatlib.

# CONSTANTS
SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678
# a way to verify proccesses with the server's and the client's protocols
KEY_LIST = list(PROTOCOL_SERVER.keys())
VAL_LIST = list(PROTOCOL_SERVER.values())

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
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # defining the socket
    my_socket.connect(("127.0.0.1", 5678))  # connect to the server
    print("Connected to server on port %d" % SERVER_PORT)
    return my_socket


# an error was caused
def error_and_exit(msg):
    print(msg)
    exit()


def login(conn):
    """login the client to the server keeps runing until succeeds
    Args:
        conn (socket)
    """
    global user_name
    global pswrd
    print("Login...")
    cnfrm = "start"

    while cnfrm != "login_ok_msg":
        if cnfrm != "start": # wrong user name or password
            print("Wrong username or password please try again!")
        username = input("Please enter username: \n")
        password = input("Please enter password: \n")
        data = username + '#' + password  # used for the protocol
        build_and_send_message(conn, PROTOCOL_CLIENT["login_msg"], data)
        print("Data: " + data)
        answer = conn.recv(2048).decode()  # get the answer from the server
        print("the answer is: " + answer)
        answer_cmd = split_msg(answer)[0]  # takes the specific command
        cnfrm = KEY_LIST[VAL_LIST.index(answer_cmd)]  # finds the matching key to the answer value

    user_name = username
    pswrd = password
    print("Login succeed")


# log the client out
def logout(conn):
    print("Logging out...")
    cmd, data = build_send_recv_parse(conn, PROTOCOL_CLIENT["logout_msg"], "")
    if cmd == "LOGOUT_OK":
        print("SERVER RESPONSE: " + data)
        print("Logout Succeeded!")


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
    global user_name

    print("Getting score...")
    cmd, data = build_send_recv_parse(conn, PROTOCOL_CLIENT["get_score_msg"], user_name)
    if KEY_LIST[VAL_LIST.index(cmd)] == "score_ok_msg":
        print(f'Your current score is: {data}')
    else: # a problem occured
        print("The system could not find your score")


def play_question(conn):
    """ask for a question fro, the server then tell if he was right or wrong
    Args:
        conn (socket)
    """
    cmd, data = build_send_recv_parse(conn, PROTOCOL_CLIENT["get_question_msg"], "")  # asking for a question

    if cmd == PROTOCOL_SERVER["no_questions_msg"]: # if a user played all the questions
        print("There are no questions left...")
        return

    elif cmd == PROTOCOL_SERVER["ok_get_questions_msg"]:
        dev_data = data.split('#')  # the data of a question from the server is devided by '#'
        print(f'Question Id: {dev_data[0]} The question: {dev_data[1]}\n1.{dev_data[2]}\n2.{dev_data[3]}\n3.{dev_data[4]}\n4.{dev_data[5]}')  # shows the question to the client
        answ_chosen = input("Enter your selected answer number: ") # the client chooses an answer
        cmd, data = build_send_recv_parse(conn, PROTOCOL_CLIENT["send_answer_msg"],
                                          dev_data[0] + '#' + answ_chosen)  # sending the client's answer

        if cmd == PROTOCOL_SERVER["ok_correct_answer"]:  # the answer was right
            print(f'Excellent! You were right, the answer was: {dev_data[int(answ_chosen) + 1]}')

        if cmd == PROTOCOL_SERVER["wrong_answer"]: # the answer was wrong
            print(
                f'You were wrong, the right answer was: {dev_data[int(data) + 1]} and you chose {dev_data[int(answ_chosen) + 1]}')

    else:
        print("ERROR")

    return


# prints the highest score
def get_highscore(conn):
    cmd, data = build_send_recv_parse(conn, PROTOCOL_CLIENT["get_highscore_msg"], "")  # asking for highscore table
    if cmd == PROTOCOL_SERVER["ok_get_highscore_msg"]:
        print(data)
    else: # if there's a problem
        print("A problem occured")
        return


# prints the users that are logged in this moment
def get_loggeed_users(conn):
    cmd, data = build_send_recv_parse(conn, PROTOCOL_CLIENT["get_logged_msg"], "")  # asking for logged users
    if cmd == PROTOCOL_SERVER["ok_get_logged_msg"]:
        print(data)
    else: # if there's a problem
        print("A problem occured")
        return


"""the game itself, you can
play question, get your score,
get highscores, get logged users
and log out"""


def main():
    global user_name
    global pswrd
    conn_sock = connect()
    print("Connected...")
    login(conn_sock) # log in the client
    options = -1  # if the client wants to continue playing

    while options != 0:
        print("-------------------------------------------------")
        options = int(input(
            "For logout press: 0 \nFor getting your score press: 1\nFor question press: 2 \nFor highscores press: 3 \nFor logged users press: 4\n"))
        if options == 1:
            get_score(conn_sock)
        elif options == 2:
            play_question(conn_sock)
        elif options == 3:
            get_highscore(conn_sock)
        elif options == 4:
            get_loggeed_users(conn_sock)

    logout(conn_sock)


if __name__ == '__main__':
    main()
