import os
import sqlite3
import cv2
import numpy as np

def data_conn(path):
	conn = sqlite3.connect(path)
	print("database connected successfully.")
	return conn

def update_img(mid,img):
	path = "ooad.db"
	conn = data_conn(path)
	img_blob = sqlite3.Binary(img)
	try:
		conn.execute("UPDATE Movie SET Img = ? WHERE ID = ?",(mid,img))
		conn.commit()
		conn.close()
	except IOError:
		print("write to database failed.")
		conn.close()

def retrieve_image_db(mid):
	path = 'ooad.db'
	conn = data_conn(path)
	cursor = conn.cursor()
	try:
		cursor.execute("SELECT Img FROM Movie WHERE ID = ?",(mid,))
		image = cursor.fetchone()
		image = np.array(image[0])
		conn.close()
		return image
	except IOError:
		print("operation failed.")
		conn.close()
'''
def Main():
	for var in range(1,10):
		img_str = 'img/' +str(var)+ '.jpg'
		print(img_str)
		img = cv2.imread(img_str)
		update_img(var,img)
'''
def access():
	for var in range(1,10):
		img = retrieve_image_db(var)
		img = img.reshape(img.shape)
		print(img)

if __name__ == '__main__':
	#Main()
	access()






