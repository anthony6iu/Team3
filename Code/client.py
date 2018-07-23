import socket
import sys
import json

BUFSIZE = 1024

def dtoj(dirt_data):
	json_data = json.dumps(dirt_data)
	return json_data.encode('utf-8')

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

host = socket.gethostname() 

port = 6666

clientsocket.connect((host, port))

# send a request to server:
start = True
while start:
	post_msg = input("Enter >> ")
	if not post_msg:
		action = 'Logout'
	else:
		action = 'Login'
	dicData = {
		'Action' : action,
		'username' : 'AnotherGuy',
		'password' : "345"
	}
	jsoData = dtoj(dicData)
	clientsocket.send(jsoData)

	#clientsocket.send(post_msg.encode('utf-8'))

	msg = clientsocket.recv(BUFSIZE)
	"""
	if msg.decode('utf-8') == 'YES':
		print("Code is correct.\n")
	elif msg.decode('utf-8') == 'NO':
		print("Code is wrong.\n")
	"""
	print(msg.decode('utf-8'))

clientsocket.close()


