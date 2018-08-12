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
	passwordInput = Entry(welcomeWindow, show = '*')
	passwordInput.grid(row=2, column=2)

	loginButton = Button(welcomeWindow, text='Login', command = lambda: Login(clientsocket))
	loginButton.grid(row=3, column=1)
	cancelButton = Button(welcomeWindow, text='Quit', command = lambda: Quit(clientsocket,welcomeWindow))
	cancelButton.grid(row=3, column=2)

	welcomeWindow.mainloop()

def HomeGUI():
	global homeWindow
	welcomeWindow.destroy()
	homeWindow = Tk()
	homeWindow.title("HomePage")
	homeWindow.geometry('640x480')

	filt = StringVar()

	search_input = Entry(homeWindow)
	search_filter_1 = Radiobutton(homeWindow, text = 'By Name',variable = filt, value = 'Name')
	search_filter_2 = Radiobutton(homeWindow, text = 'By Location', variable = filt, value = 'Location')
	search_content = Text(homeWindow, width = 30, height = 5)
	search_button = Button(homeWindow, width = 14, height = 3, text = 'Search', command = lambda: Search(clientsocket, search_input.get(), filt.get(), search_content))
	cancel_button = Button(homeWindow, text = 'Quit', command = lambda: Quit(clientsocket,homeWindow))

	search_input.grid(row = 1)
	search_filter_1.grid(row = 2)
	search_filter_2.grid(row = 3)
	search_button.grid(row = 4)
	search_content.grid(row = 5)
	cancel_button.grid(row = 6)

	homeWindow.mainloop()

def Login(cskt):
	global user
	logininfo = usernameInput.get()
	password = passwordInput.get()
	dicData = {
	'Action' : 'Login',
	'username' : logininfo,
	'password' : password
	}
	recdata = ClientHandler(cskt,dicData)
	if recdata['flag']:
		user = logininfo
		HomeGUI()
	else:
		wc_label1['text'] = recdata['note']




def Search(cskt, text, filt, result):
	dicData = {
		'Action' : 'Search',
		'user' : user,
		'text' : text,
		'filter' : filt
	}
	recdata = ClientHandler(cskt,dicData)
	if recdata['flag']:
		recdata = recdata['content']
		result.insert(END,recdata)
	else:
		result = insert(END,'No result found.')




def Quit(cskt,window):
	dicData = {
	'Action' : 'Quit'
	}
	jsoData = dtoj(dicData)
	cskt.send(jsoData)
	window.destroy()

def ClientHandler(cskt,dicData):
	jsoData = dtoj(dicData)
	cskt.send(jsoData)

	msg = cskt.recv(BUFSIZE)
	recdata = jtod(msg)

	return recdata


if __name__ == '__main__':
	Main()

