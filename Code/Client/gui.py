import socket
import sys
import json
from tkinter import *

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
	# send a request to server:
	start = True
	recv_msg = {}
	WelcomeGUI()
	clientsocket.close()

def WelcomeGUI():
	global usernameInput, passwordInput, welcomeWindow, wc_label1
	welcomeWindow = Tk()
	welcomeWindow.title('Movie Ticket Booking Online')
	welcomeWindow.geometry('640x480')
	for i in range(4):
		welcomeWindow.rowconfigure(i, weight = 5)
		welcomeWindow.columnconfigure(i, weight = 5)

	wc_label1 = Label(welcomeWindow, text='Please Login')
	wc_label1.grid(row=0, column=1, columnspan=2)

	usernameText = Label(welcomeWindow, text='Username:')
	usernameText.grid(row=1, column=1)
	usernameInput = Entry(welcomeWindow)
	usernameInput.grid(row=1, column=2)

	passwordText = Label(welcomeWindow, text='Password:')
	passwordText.grid(row=2, column=1)
	passwordInput = Entry(welcomeWindow)
	passwordInput.grid(row=2, column=2)

	loginButton = Button(welcomeWindow, text='Login', command = lambda: Login(clientsocket))
	loginButton.grid(row=3, column=1)
	cancelButton = Button(welcomeWindow, text='Cancel', command = welcomeWindow.destroy)
	cancelButton.grid(row=3, column=2)

	welcomeWindow.mainloop()

def HomeGUI():
	global homeWindow
	welcomeWindow.destroy()
	homeWindow = Tk()
	homeWindow.title("HomePage")
	homeWindow.geometry('640x480')
	homeWindow.mainloop()

def Login(cskt):
	global account, logininfo
	logininfo = usernameInput.get()
	password = passwordInput.get()
	dicData = {
	'Action' : 'Login',
	'username' : logininfo,
	'password' : password
	}
	recdata = ClientHandler(cskt,dicData)
	if recdata['flag']:
		HomeGUI()
	else:
		wc_label1['text'] = recdata['note']

def ClientHandler(cskt,dicData):
	jsoData = dtoj(dicData)
	cskt.send(jsoData)

	msg = cskt.recv(BUFSIZE)
	recdata = jtod(msg)

	return recdata




if __name__ == '__main__':
	Main()

