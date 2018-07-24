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

#-----------------------------------------------------------
def threaded(cskt,addr):
	database = sqlite3.connect('ooad.db')
	while True:		
		# receive message from client.
		data = cskt.recv(BUFSIZE)
		dicData = jtod(data)
		action = dicData['Action']
		response_msg = handler(dicData,database)
		history = response_msg
		response_msg = dtoj(response_msg)

		if action == 'Logout':
			print("%s Disconnected" % str(addr))
			break

		now = time.strftime("%H:%M:%S")

		print("[%s] FORM %s : %s" % (str(now), addr, dicData))
		print("[%s] TO   %s : %s" % (str(now), addr, history))
		# send message to client.
		cskt.send(response_msg)

	database.close()
	cskt.close()
	

def jtod(json_data):
	json_data.decode('utf-8')
	dict_data = json.loads(json_data)
	return dict_data

def dtoj(dict_data):
	json_data = json.dumps(dict_data)
	return json_data.encode('utf-8')


def Main():
	# Database set up.
	database = sqlite3.connect('ooad.db')

	# Server set up.
	host = socket.gethostname()
	port = PORT
	sskt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sskt.bind((host,port))
	sskt.listen(5)
	print("Movie ticket booking management system.\nWaiting for connection.....")
	# server socket is already listening.
	
	while True:
		cskt,addr = sskt.accept()
		print("%s Connected!" % str(addr))

		start_new_thread(threaded, (cskt,addr))

	sskt.close()

if __name__ == '__main__':
	Main()
















'''
# Socket set up
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()

port = 6666

serversocket.bind((host,port))

serversocket.listen(5)
start = True
while start:
    # client connection.
    clientsocket,addr = serversocket.accept()      

    print("%s LOGIN!\n" % str(addr))
    
    #listen loop:
    while True:
    	data = clientsocket.recv(BUFSIZE)
    	u_data = data.decode('utf-8')
    	if not u_data:
    		break
    	now = time.strftime("%H:%M:%S")
    	print("[%s] %s : %s" % (str(now), str(addr), u_data))
    	"""
    	if u_data == '123':
    		response_msg = 'YES'
    	else:
    		response_msg = 'NO'
    	clientsocket.send(response_msg.encode('utf-8'))
    	"""
    	response_msg = '[' + now + '] ' + 'Server received: ' + u_data
    	clientsocket.send(response_msg.encode('utf-8'))

    print("%s LOGOUT\n" % str(addr))
    start = False

clientsocket.close()
serversocket.close()
'''

