import socket
import sys
import json

BUFSIZE = 1024

def dtoj(dirt_data):
	json_data = json.dumps(dirt_data)
	return json_data.encode('utf-8')

def jtod(json_data):
	json_data.decode('utf-8')
	return json.loads(json_data)

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

host = socket.gethostname() 

port = 6666

clientsocket.connect((host, port))

# send a request to server:
start = True
recv_msg = {}
while start:

	post_msg = input("Enter >> ")
	if not post_msg or post_msg == 'Logout':
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
			'username' : 'newuser123',
			'password' : 'newpwd1',
			'firstname' : '',
			'lastname' : '',
			'email' : '',
			'phone' : ''
		}

	elif post_msg == 'ReqAcc':
		action = 'ReqAcc'
		dicData = {
			'Action' : action,
			'username' : 'Name2'
		}

	elif post_msg == 'UpdAcc':
		if recv_msg['Action'] == 'ReqAcc':
			# change action from ReqAcc to UpdAcc
			recv_msg['Action'] = 'UpdAcc'

			if recv_msg['flag']:
				recv_msg['phone'] = recv_msg['phone'] + 'C'
				dicData = recv_msg
			else:
				dicData = recv_msg

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




	# receive handler.
	msg = clientsocket.recv(BUFSIZE)
	# handler.
	recdata = jtod(msg)
	if recdata['Action'] == 'ReqAcc':
		recv_msg = recdata



	print(msg.decode('utf-8'))

clientsocket.close()


