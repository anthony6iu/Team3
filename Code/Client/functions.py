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

def Main():
	global clientsocket
	clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	host = socket.gethostname() 
	port = 6666
	clientsocket.connect((host, port))

	#测试每一个函数：
	print('Check_account:')
	print(Check_account(clientsocket, 'liu', '123'))
	print('Add_account:')
	print(Add_account(clientsocket, 'alex', 'pwdalex'))
	print('Update_account:')
	print(Update_account(clientsocket, 'alex', 'fn', 'ln', 'npwd', '1@1.com', '911'))
	print('Search_name:')
	print(Search_name(clientsocket, 'Chirstopher Robin'))
	print('Search_type:')
	print(Search_type(clientsocket, 'Action'))
	print('Check_seat:')
	print(Check_seat(clientsocket, 6))
	print('Update_seat:')
	print(Update_seat(clientsocket, 6, {'r0' : 1, 'r1' : 2, 'r2' : 3, 'r3' : 4, 'r4' : 5}))
	print('movie_info:')
	print(movie_info(clientsocket, 'Chirstopher Robin'))
	print('~Logout~')
	Logout(clientsocket)
	clientsocket.close()


# 下面的所有函数都需要传入client socket， 上面的main函数里有建立socket的过程。
def Check_account(cskt, username, password):
	data = {
		'Action' : 'Login',
		'username' : username,
		'password' : password
	}
	json_data = dtoj(data)
	cskt.send(json_data)

	msg = cskt.recv(BUFSIZE)
	recdata = jtod(msg)

	if recdata['flag']:
		# 保存到全局变量User, 以保证之后的各种操作。
		global User
		User = recdata['user']
		return True
	else:
		return False

def Logout(cskt):
	data = {
		'Action' : 'Logout',
		'username' : User,
		'user' : User
	}
	json_data = dtoj(data)
	cskt.send(json_data)


def Add_account(cskt, username, password):
	data = {
		'Action' : 'Signup',
		'username' : username,
		'password' : password
	}
	json_data = dtoj(data)
	cskt.send(json_data)

	msg = cskt.recv(BUFSIZE)
	recdata = jtod(msg)

	if recdata['flag']:
		return True
	else:
		return False

# username 不许再修改了。
def Update_account(cskt, old_username, first_name, last_name, new_password, new_email, new_home_phone):
	data = {
		'Action' : 'UpdAccount',
		'user' : old_username,
		'firstname' : first_name,
		'lastname' : last_name,
		'password' : new_password,
		'email' : new_email,
		'phone' : new_home_phone
	}
	json_data = dtoj(data)
	cskt.send(json_data)

	msg = cskt.recv(BUFSIZE)
	recdata = jtod(msg)

	if recdata['flag']:
		return True
	else:
		return False

# 这两个函数中你需要的location 和 cinema 是一回事。
# 针对每一条信息， 里面的5个key分别是： movie, cinema, showtime, screenid, sid. 和手册里写的是一样的。
def Search_name(cskt, text):
	data = {
		'Action' : 'Search',
		'user' : User,
		'text' : text,
		'filter' : 'Name'
	}
	json_data = dtoj(data)
	cskt.send(json_data)

	msg = cskt.recv(BUFSIZE)
	recdata = jtod(msg)

	if recdata['flag']:
		return recdata['content']
	else:
		return False

def Search_type(cskt, text):
	data = {
		'Action' : 'Search',
		'user' : User,
		'text' : text,
		'filter' : 'Type'
	}
	json_data = dtoj(data)
	cskt.send(json_data)

	msg = cskt.recv(BUFSIZE)
	recdata = jtod(msg)

	if recdata['flag']:
		return recdata['content']
	else:
		return False

def Check_seat(cskt, show_id):
	data = {
		'Action' : 'DisSeat',
		'user' : User,
		'sid' : show_id,
	}
	json_data = dtoj(data)
	cskt.send(json_data)

	msg = cskt.recv(BUFSIZE)
	recdata = jtod(msg)

	if recdata['flag']:
		seat_info = {
			'r0' : recdata['r0'],
			'r1' : recdata['r1'],
			'r2' : recdata['r2'],
			'r3' : recdata['r3'],
			'r4' : recdata['r4']
		}
		return seat_info
	else:
		return False

def Update_seat(cskt, show_id, new_seat_info):
	data = {
		'Action' : 'UpdSeat',
		'user' : User,
		'sid' : show_id,
		'r0' : new_seat_info['r0'],
		'r1' : new_seat_info['r1'],
		'r2' : new_seat_info['r2'],
		'r3' : new_seat_info['r3'],
		'r4' : new_seat_info['r4']
	}
	json_data = dtoj(data)
	cskt.send(json_data)

	msg = cskt.recv(BUFSIZE)
	recdata = jtod(msg)

	return recdata['flag']


def movie_info(cskt, movie_name):
	data = {
		'Action' : 'MovieInfo',
		'user' : User,
		'moviename' : movie_name
	}
	json_data = dtoj(data)
	cskt.send(json_data)

	msg = cskt.recv(BUFSIZE)
	recdata = jtod(msg)

	if recdata['flag']:
		send = {
			'Type' : recdata['type'], 
			'Description' : recdata['description'], 
			'Actors': recdata['actors']
		}
		return send
	else:
		return False

if __name__ == "__main__":
	Main()












