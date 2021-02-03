##############################################################################
# server.py
##############################################################################

import socket
from chatlib_skeleton import *

# GLOBALS
users = {
	"abc|123|0|",
	"test|test|0|",
	"admin|AaBbCcDd#|0|",
	"blabla|hello|0|",
	"super|trooper|0|",
	"super2|trooper2|0|",
	"bilby|m0unt41ns|0|",
	"trivia_king|KING|0|",
	"hackerman|TriCeRaCop|0|",
	"mrhemulin|flowerz|0|0",
	"bambababy|peanuts|5|0,2",
	}
questions = {
            "What is the capital city of USA?|Washington DC|New York|Los Angeles|Detroit|1",
	    "Who wrote the song ""Yellow submarine""?|Elvis Presley|The Beatles|Led Zeppelin|Britney Spears|2",
	    "How much is 1+1?|5|6|7|2|4"
	    }
logged_users = {}  # a dictionary of client hostnames to usernames - will be used later

ERROR_MSG = "Error! "
SERVER_PORT = 5678
SERVER_IP = "127.0.0.1"


# HELPER SOCKET METHODS

def build_and_send_message(conn, code, msg):
	message = build_message(code, msg)
	conn.send(message.encode())
	print("[SERVER] ", message)	  # Debug print


def recv_message_and_parse(conn):
	data = conn.recv(2048).decode()
	print("Client Response: " + data)
	cmd, msg = parse_message(data)

	if cmd is None:
		print("Problem Occurred")

	return cmd, msg
	

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
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# defining the socket
    server_socket.bind((SERVER_IP, SERVER_PORT))# setting the current ip and port
    server_socket.listen()# the time it listen to client until closing the socket
    print("Listening for connections on port %d" % SERVER_PORT)
    
    return server_socket
	

		
def send_error(conn, error_msg):
	"""
	Send error message with given message
	Recieves: socket, message error string from called function
	Returns: None
	"""
	build_and_send_message(conn, PROTOCOL_SERVER["error_cmd"], error_msg)
	
	


	
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
	
	# Implement code ...


def handle_login_message(conn, data):
	"""
	Gets socket and message data of login message. Checks  user and pass exists and match.
	If not - sends error and finished. If all ok, sends OK message and adds user and address to logged_users
	Recieves: socket, message code and data
	Returns: None (sends answer to client)
	"""
	global users  # This is needed to access the same users dictionary from all functions
	global logged_users	 # To be used later
	server_response = ""
	login_details = data.split("#")
	
	if len(login_details) != 2:
		server_response = "Invalid Data For Login"
	
	else: 
		client_user_name = login_details[0]
		if client_user_name in users.keys():# if the user name exists
			client_password = login_details[1]
			
			if client_password == users[client_user_name]:# if the password exists
				build_and_send_message(conn, PROTOCOL_SERVER["login_ok_msg"], "")
				logged_users[client_user_name] = client_password# add the user to the logged dictionary
				return
		
		server_response = "User Name Or Password Does Not Exists"		
	
	send_error(server_response)
	return







def handle_client_message(conn, cmd, data):
	"""
	Gets message code and data and calls the right function to handle command
	Recieves: socket, message code and data
	Returns: None
	"""
	global logged_users	 # To be used later
	if cmd == "LOGIN":
		handle_login_message(conn,data)
	elif cmd == "LOGOUT":
		handle_logout_message(conn)
	elif cmd == "LOGGED":
		pass
	elif cmd == "GET_QUESTION":
		pass
	elif cmd == "SEND_ANSWER":
		pass
	elif cmd == "MY_SCORE":
		handle_getscore_message(conn,data.split("#")[0])
	elif cmd == "HIGHSCORE":
		pass
	elif cmd == "" and data == "":
		conn.close()
	else:
		send_error()

	

def main():
	# Initializes global users and questions dicionaries using load functions, will be used later
	global users
	global questions
	
	print("Welcome to Trivia Server!")
	server_socket = setup_socket()
	while True:
        client_socket, client_address = server_socket.accept()# accept the request
        print('New connection received')
		cmd, data = recv_message_and_parse(client_socket)
        handle_client_message(client_socket, cmd, data)


if __name__ == '__main__':
	main()
