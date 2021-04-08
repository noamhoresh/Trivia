##############################################################################
# server.py
##############################################################################

import socket
from chatlib_skeleton import *
import select

# GLOBALS
users = {
    "abc": ['123', 13],
    "test": ["test", 0],
    "admin": ["AaBbCcDd", 0],
    "blabla": ["hello", 0],
    "super": ["trooper", 0],
    "super2": ["trooper2", 0],
    "bilby": ["m0unt41ns", 0],
    "trivia_king": ["KING", 0],
    "hackerman": ["TriCeRaCop", 0],
    "mrhemulin": ["flowerz", 0],
    "bambababy": ["peanuts", 5, (0, 2)]
}

questions = {
    "What is the capital city of USA?|Washington DC|New York|Los Angeles|Detroit|1",
    "Who wrote the song ""Yellow submarine""?|Elvis Presley|The Beatles|Led Zeppelin|Britney Spears|2",
    "How much is 1+1?|5|6|7|2|4"
}

logged_users = {}  # a dictionary of client hostnames to usernames - will be used later
messages_to_send = []# a list of tuples of all the messages are meant to be sent

ERROR_MSG = "Error! "
SERVER_PORT = 5678
SERVER_IP = "127.0.0.1"


# HELPER SOCKET METHODS

def build_and_send_message(conn, code, msg):
    global messages_to_send
    message = build_message(code, msg)
    messages_to_send.append((conn,message))
    print("[SERVER] ", message)  # Debug print


def recv_message_and_parse(conn):
    data = conn.recv(2048).decode()
    print("Client Response: " + data)
    cmd, msg = parse_message(data)
    # if msg == "":# if we got empty messages we know a client had diconnected
	#     return "", ""
    # if cmd is None:
    #     print("Problem Occurred")

    return cmd, msg


# Data Loaders #

def print_client_sockets():
	"""prints all the currently logged users details
	"""
	global logged_users
	for key in logged_users:
		print(key + " " + logged_users[key])

def load_questions():
    """
	Loads questions bank from file	## FILE SUPPORT TO BE ADDED LATER
	Recieves: -
	Returns: questions dictionary
	"""
    questions = {
        2313: {"question": "How much is 2+2", "answers": ["3", "4", "2", "1"], "correct": 2},
        4122: {"question": "What is the capital of France?", "answers": ["Lion", "Marseille", "Paris", "Montpellier"],
               "correct": 3}
    }

    return questions


# def load_user_database():
#     """
# 	Loads users list from file	## FILE SUPPORT TO BE ADDED LATER
# 	Recieves: -
# 	Returns: user dictionary
# 	"""
#     users = {
#         "test"	:	{"password" :"test" ,"score" :0 ,"questions_asked" :[]},
# 		"yossi"		:	{"password" :"123" ,"score" :50 ,"questions_asked" :[]},
# 		"master"	:	{"password" :"master" ,"score" :200 ,"questions_asked" :[]}
# 	}
# 	return users


# SOCKET CREATOR

def get_highscore(conn):
	
	scores_file = open("score.txt", "r")
	top_five_users = []
	for line in scores_file:
		user_name, score = line.split(":")
		top_five_users.append((user_name, int(score)))
	scores_file.close()
	top_five_users.sort(key = arrange, reverse=True)
	final_top_five = "THE TOP FIVE USERS ARE: \n"
	for i in range(5):
		final_top_five += top_five_users[i][0] + ": " + str(top_five_users[i][1]) + "\n"
	build_and_send_message(conn,PROTOCOL_SERVER["ok_get_highscore_msg"],final_top_five)

def arrange(tup):
	return tup[1]

def get_logged_users(conn):
	global logged_users
	logged = ""
	
	for user in logged_users.values():
		logged += "User:" + user[0] + "\n"
	build_and_send_message(conn,PROTOCOL_SERVER["ok_get_logged_msg"],logged)

def setup_socket():
	"""
	Creates new listening socket and returns it
	Recieves: -
	Returns: the socket object
	"""
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind((SERVER_IP, SERVER_PORT))
	server_socket.listen(5)# limting the number of clients can connect
	print("Listening for connections on port %d" % SERVER_PORT)
	return server_socket




def send_error(conn, error_msg):
	"""
	Send error message with given message
	Recieves: socket, message error string from called function
	Returns: None
	"""
	build_and_send_message(conn, PROTOCOL_SERVER["error_cmd"], error_msg)





#### MESSAGE HANDLING


def handle_getscore_message(conn, username):
	"""send the client his current score
	Args:
		conn (socket)
		username (str)
	"""
	scores_file = open("score.txt", "r")
	requested_score = "-1"
	user_name = ""
	score = ""
	for line in scores_file: # runs 
		user_name, score = line.split(":")
		if user_name == username:
			requested_score = score
	scores_file.close()

	build_and_send_message(conn, PROTOCOL_SERVER["score_ok_msg"], requested_score)


def handle_question_message(conn, user_name):
	"""send the client a random question
	Args:
		conn (socket):
		user_name (str): the client's username
	"""
	cmd = PROTOCOL_SERVER["ok_get_questions_msg"]
	data = create_random_question(user_name, conn)# the question generated in the protocol

	if data is None:
		cmd = PROTOCOL_SERVER["no_questions_msg"]
		data = ""

	build_and_send_message(conn, cmd, data)


def handle_logout_message(conn):
	"""
	Closes the given socket (in laster chapters, also remove user from logged_users dictioary)
	Recieves: socket
	Returns: None
	"""
	global logged_users
	global flag
	global open_client_sockets
	flag = False
	logged_users.pop(conn.getpeername(), None)
	conn.send(build_message(PROTOCOL_SERVER["logout_ok_msg"], ":(").encode())
	open_client_sockets.remove(conn) # remove the conn so it won't use it again
	conn.close()
	print("Client Logged Out...")


def handle_login_message(conn, data):
	"""
	Gets socket and message data of login message. Checks  user and pass exists and match.
	If not - sends error and finished. If all ok, sends OK message and adds user and address to logged_users
	Recieves: socket, message code and data
	Returns: None (sends answer to client)
	"""
	global users  # This is needed to access the same users dictionary from all functions
	global logged_users	 # To be used later
	global user_name
	global open_client_sockets

	server_response = ""
	login_details = data.split("#")
	if len(login_details) != 2:
		server_response = "Invalid Data For Login"

	else:
		client_user_name = login_details[0]
		logged_usernames_list = []
		for tup in logged_users.values():
			logged_usernames_list.append(tup[0])
		if client_user_name in logged_usernames_list: # if the client is already connected			
			send_error(conn, "User Name Already Connected, Try Another User...")
			return
		if client_user_name in users.keys(): # if the user name exists
			client_password = login_details[1]

			if client_password == users[client_user_name][0]  :# if the password exists
				user_name = client_user_name
				build_and_send_message(conn, PROTOCOL_SERVER["login_ok_msg"], "")
				logged_users[conn.getpeername()] = (client_user_name, []) # add the user to logged users dict
				return

		server_response = "User Name Or Password Does Not Exists"

	send_error(conn, server_response)
	return


def create_random_question(Username, conn):
	"""
	gets username and returns a question that
	wasn't played yet
	if there isn't such question - returns None
	"""
	global logged_users
	played_questions = logged_users[conn.getpeername()][1]
	questions = load_questions()
	questions_Id = questions.keys()
	for q in questions_Id:
		if q not in played_questions:# יש פונקציה בשביל ז לא צריך לבנות לבד
			played_questions.append(q)
			return str(str(q) + '#' + questions.get(q).get("question") + '#' + questions.get(q).get("answers")[0] + '#' + questions.get(q).get("answers")[1] + '#' + questions.get(q).get("answers")[2] + '#' + questions.get(q).get("answers")[3])
	return None


def handle_answer_message(conn, username, data):
	global questions
	questions = load_questions()
	quest_id, answr = data.split("#")
	if str(questions[int(quest_id)]["correct"]) == answr:
		scores_file = open("score.txt", "r")
		final_score_txt = ""
		user_name = ""
		score = ""
		for line in scores_file:
			user_name, score = line.split(":")
			if user_name == username:
				final_score_txt += user_name + ":" + str(int(score) + 10) + "\n"
			else:
				final_score_txt += line
		scores_file.close()
		scores_file = open("score.txt", "w")
		scores_file.write(final_score_txt)
		scores_file.close()
		build_and_send_message(conn, "CORRECT_ANSWER", "")
	else:
		build_and_send_message(conn, "WRONG_ANSWER", str(questions[int(quest_id)]["correct"]))


def handle_client_message(conn, cmd, data):
	"""
	Gets message code and data and calls the right function to handle command
	Recieves: socket, message code and data
	Returns: None
	"""
	global user_name
	global logged_users	 # To be used later
	if cmd == "LOGIN":
		handle_login_message(conn, data)
	elif cmd == "LOGOUT":
		handle_logout_message(conn)
	elif cmd == "LOGGED":
		get_logged_users(conn)
	elif cmd == "GET_QUESTION":
		handle_question_message(conn, user_name)
	elif cmd == "SEND_ANSWER":
		handle_answer_message(conn, user_name, data)
	elif cmd == "MY_SCORE":
		handle_getscore_message(conn, data.split("#")[0])# the user_name of the current user
	elif cmd == "HIGHSCORE":
		get_highscore(conn)
	elif cmd == "" and data == "":
		conn.close()
	else:
		send_error(conn,"??")


def main():
	"""Initializes global users and questions dicionaries using load functions, will be used later"""
	global users
	global flag
	global questions
	global messages_to_send
	global open_client_sockets

	print("Welcome to Trivia Server!")
	server_socket = setup_socket()
	open_client_sockets = []  # the sockets are currently connected to the server
	flag = True
	print("Started Server Listening Operation...")
	while True:
		r_list, w_list, x_list = select.select([server_socket] + open_client_sockets, open_client_sockets, [])
		for current_socket in r_list:
			if current_socket is server_socket:  # if it is a new client
				(new_socket, address) = server_socket.accept()
				print("new socket connected to server: ", new_socket.getpeername())
				open_client_sockets.append(new_socket)
			else:
				try:
					cmd, msg = recv_message_and_parse(current_socket)
					print("new data from client!")
					messages_to_send.append((current_socket, str(cmd) + '|' + str(msg)))
				except ConnectionResetError:
					print("[Client Disconnected Surprisingly]")
					logged_users.pop(current_socket.getpeername())
					open_client_sockets.remove(current_socket)
					# still in logged users dictionary
				
		
		send_waiting_messages(w_list)
                                                      

# def send_waiting_messages(w_list):
# 	global messages_to_send

# 	for message in messages_to_send:
# 		current_socket = message[0]
# 		msg_parts = split_msg(message[1])
# 		cmd = msg_parts[0]
# 		if msg_parts[1] == '0000':
# 			data = ""
# 		else:
# 			data = msg_parts[2]
		
# 		print(f'CMD: {cmd}; DATA: {data}')
# 		if current_socket in w_list:
# 			print("good")
# 			handle_client_message(current_socket, cmd, data)
# 			messages_to_send.remove(message)


def send_waiting_messages(wlist):
	for message in messages_to_send:
		current_socket, data = message
		cmd = data.split(DELIMITER)[0]
		msg = ""

		if cmd in PROTOCOL_CLIENT.values():
			if len(data.split(DELIMITER)) != 1:
				msg = data.split(DELIMITER)[1]
			handle_client_message(current_socket,cmd,msg)
		elif current_socket in wlist:
			current_socket.send(data.encode())
		messages_to_send.remove(message)



if __name__ == '__main__':
	main()
