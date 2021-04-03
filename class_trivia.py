from socket import *
import socket
import select
IP = '127.0.0.1'
PORT = 8822

SERVER_SOCKET = socket.socket()
SERVER_SOCKET.bind((IP, PORT))
print(f"server is up on port: {PORT}, IP: {IP}")
SERVER_SOCKET.listen(5)
open_client_sockets = []
messages_to_send = []
while True:
    r_list, w_list, x_list = select.select([SERVER_SOCKET] + open_client_sockets, open_client_sockets, [])
    for current_socket in r_list:
        if current_socket is SERVER_SOCKET:
            (new_socket, address) = SERVER_SOCKET.accept()
            print("new socket connected to server: ", new_socket.getpeername())
            open_client_sockets.append(new_socket)
        else:
            print("new data from client!")
            data = current_socket.recv(1024)
            if data == b'end':
                p_id = current_socket.getpeername()
                open_client_sockets.remove(current_socket)
                print(f"connection with client {p_id} is closed.")
                messages_to_send.append(current_socket, data)
            else:
                p_id = current_socket.getpeername()
                print(f'client: {p_id}', data.decode())
                messages_to_send.append((current_socket, b'hello, ' + data))
send_waiting_messages(w_list)

def send_waiting_messages(wlist):
    for message in messages_to_send:
        current_socket, data = message
        if current_socket in wlist:
            current_socket.send(data.encode())
            messages_to_send.remove(message)