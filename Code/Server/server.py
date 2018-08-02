# -!Server!-
import sys

# import multi-threads module.
from _thread import *
import threading
# import socket programming module.
import socket
# import time.
import time
# import sqlite3 Database service.
import sqlite3
# import json protocol.
import json

from handler import *
# socket buffer size(bytes).
# and port number.
BUFSIZE = 1024
PORT = 6666

'''
Goal: a function that a new thread should execute.
Pre : thread is created and take clientsocket and addr infos(identify) as input.
Post: server service start here.
'''
def threaded(cskt,addr):
	# for each thread(client), creating a new connection to target database.
	try:
		database = sqlite3.connect('ooad.db')
	except:
		print('Database connection failed.')
		exit()
	print('Database is connected!')
	
	print('Thread is created.' + str(addr))

	while True:		
		# receive message from client.
		data = cskt.recv(BUFSIZE)
		# transfrom to dictionary type data.
		dicData = jtod(data)

		action = dicData['Action']
		if action == 'Quit':
			print("%s Quit" % str(addr))
			break
		# call handler.
		response_msg = handler(dicData,database)
		# save response message as history (log).
		history = response_msg
		# transform dict type to json type.
		response_msg = dtoj(response_msg)


		# print history to server screen( It can be written to server log file.).
		now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		print("[%s] FORM %s : %s" % (str(now), addr, dicData))
		print("[%s] TO   %s : %s" % (str(now), addr, history))

		# send message to client.
		cskt.send(response_msg)

		# disconnect.
		if dicData['Action'] == 'Logout':
			print("%s Logout" % str(addr))
			break

	# close database connection after client logout.
	database.close()
	# close client socket. (recycle)
	cskt.close()
	print('Thread is abort.' + str(addr))

	


'''
Goal: transfrom json type data to dict type data.
Pre : json type data as Input.
Post: return dict type data.
'''
def jtod(json_data):
	json_data.decode('utf-8')
	dict_data = json.loads(json_data)
	return dict_data

'''
Goal: transfrom dict type data to json type data.
Pre : dict type data as Input.
Post: return json type data.
'''
def dtoj(dict_data):
	json_data = json.dumps(dict_data)
	return json_data.encode('utf-8')

'''
Goal: Main function.
Pre : N/A
Post: N/A
'''
def Main():


	# Server set up.
	host = socket.gethostname()
	port = PORT
	sskt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sskt.bind((host,port))
	sskt.listen(5)
	print("Movie ticket booking management system.\nWaiting for connection.....")
	# server socket is already listening.
	
	while True:
		# accepet new client.
		cskt,addr = sskt.accept()
		print("%s Connected!" % str(addr))

		# try to create a new thread.
		try:
			start_new_thread(threaded, (cskt,addr))
		except:
			print('Error to create a new thread.\n')

	sskt.close()

# Start program.
if __name__ == '__main__':
	Main()

