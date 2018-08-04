import socket
import sys
import json

global user
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
		dicData = {
			'Action' : 'Signup',
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
			user = recdata['user']
			break
		else:
			homepage = False
			command = ''
			continue

while homepage:

	post_msg = input("Enter >> ")
	if post_msg == 'Logout':
		dicData = {
			'Action' : 'Logout',
			'user' : user,
			'username' : 'AnotherGuy'
		}
	elif post_msg == '':
		continue

	elif post_msg == 'ReqAcc':
		dicData = {
			'Action' : 'ReqAcc',
			'user' : user,
			'username' : user
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
		dicData = {
			'Action' : 'Search',
			'user' : user,
			'text' : 'Action',
			'filter' : 'Type'
		}

	elif post_msg == 'dis1':
		dicData = {
			'Action' : 'DisShow',
			'user' : user,
			'text' : 'Chirstopher Robin',
			'filter' : 'moviename'
		}
	elif post_msg == 'dis2':
		dicData = {
			'Action' : 'DisShow',
			'user' : user,
			'text' : '201808021630',
			'filter' : 'showtime'
		}
	elif post_msg == 'dis3':
		dicData = {
			'Action' : 'DisShow',
			'user' : user,
			'text' : 'Bow Tie Criterion Cinemas',
			'filter' : 'cinemaname'
		}

	elif post_msg == 'MakeRes':
		dicData = {
			'Action' : 'MakeRes',
			'user' : user,
			'username' : 'newuser1',
			'moviename' : 'movie1',
			'location' : 'location1',
			'showtime' : '201801011250',
			'seat' : '12'
		}
	else:
		print('Wrong Command.')
		post_msg = ''
		continue

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

	elif recdata['Action'] == 'DisShow':
		if recdata['flag']:
			for show in recdata['content']:
				print(show)

	elif recdata['Action'] == 'Logout':
		if recdata['flag']:
			break
		else:
			post_msg = ''
			print('Logout failed.')

clientsocket.close()


