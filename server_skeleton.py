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
    # client_socket, client_address = server_socket.accept()# accept the request
	return client_socket
	

		
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
	for i in users:
		user_details = i.split(DELIMITER)
		if login_details[0] != user_details[0] or login_details[1] != user_details[1]:
			server_response = "User Does Not Exists"

	if len(login_details) != 2:
		server_response = "Invalid Data For Login"
	else:
		logged_users
		build_and_send_message(conn,"LOGIN_OK","")
		return
	build_and_send_message(conn, "ERROR", server_response)







def handle_client_message(conn, cmd, data):
	"""
	Gets message code and data and calls the right function to handle command
	Recieves: socket, message code and data
	Returns: None
	"""
	global logged_users	 # To be used later
	
	# Implement code ...
	

def main():
	# Initializes global users and questions dicionaries using load functions, will be used later
	global users
	global questions
	
	print("Welcome to Trivia Server!")
	
	# Implement code ...


if __name__ == '__main__':
	main()
