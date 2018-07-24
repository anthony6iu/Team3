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
		dicData = {
			'Action' : action
		}

	elif post_msg == 'Login':
		action = 'Login'
		dicData = {
			'Action' : action,
			'username' : 'AnotherGuy',
			'password' : '345'
		}

	elif post_msg == 'Signup':
		action = 'Signup'
		dicData = {
			'Action' : action,
			'username' : 'newuser1',
			'password' : 'newpwd1',
			'firstname' : '',
			'lastname' : '',
			'email' : '',
			'phone' : ''
		}
	elif post_msg == 'MakeRes':
		action = 'MakeRes'
		dicData = {
			'Action' : action,
			'username' : 'newuser1',
			'moviename' : 'movie1',
			'location' : 'location1',
			'showtime' : '201801011250',
			'seat' : '12'
		}
	else:
		post_msg = ''
		continue

	jsoData = dtoj(dicData)
	clientsocket.send(jsoData)

	if action == 'Logout':
		break

	msg = clientsocket.recv(BUFSIZE)
	"""
	if msg.decode('utf-8') == 'YES':
		print("Code is correct.\n")
	elif msg.decode('utf-8') == 'NO':
		print("Code is wrong.\n")
	"""
	print(msg.decode('utf-8'))

clientsocket.close()


