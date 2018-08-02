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

welcome = True
homepage = False
recv_msg = {}

while welcome:
	command = input("Enter >> ")
	if command == 'Login':
		dicData = {
			'Action' : 'Login',
			'username' : 'AnotherGuy',
			'password' : '345'
		}
	elif command == 'Signup':
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
	elif command == 'Quit':
		dicData = {
			'Action' : 'Quit'
		}
		jsoData = dtoj(dicData)
		clientsocket.send(jsoData)
		break
	else:
		print('Please Login first.')
		command = ''
		continue

	jsoData = dtoj(dicData)
	clientsocket.send(jsoData)

	msg = clientsocket.recv(BUFSIZE)
	recdata = jtod(msg)

	if recdata['Action'] == 'Login':
		if recdata['flag']:
			homepage = True
			command = ''
			break
		else:
			homepage = False
			command = ''
			continue

while homepage:

	post_msg = input("Enter >> ")
	if post_msg == 'Logout':
		action = 'Logout'
		dicData = {
			'Action' : action,
			'username' : 'AnotherGuy'
		}
	elif post_msg == '':
		continue

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

	elif post_msg == 'Search':
		action = 'Search'
		dicData = {
			'Action' : action,
			'text' : 'Action',
			'filter' : 'Type'
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

	jsoData = dtoj(dicData)
	clientsocket.send(jsoData)

	msg = clientsocket.recv(BUFSIZE)
	recdata = jtod(msg)

	if recdata['Action'] == 'ReqAcc':
		recv_msg = recdata
		print(recv_msg)

	elif recdata['Action'] == 'Search':
		if recdata['flag']:
			for movie in recdata['content']:
				print(movie)
	if recdata['Action'] == 'Logout':
		if recdata['flag']:
			break
		else:
			post_msg = ''
			print('Logout failed.')

clientsocket.close()


