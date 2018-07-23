# handler different actions.
# data is a dictionary.
import sqlite3
import json
import sys

def handler(receive,database):
    action = receive['Action']
    if action == 'Login':
        send = Login(receive,database)
        return send
    elif action  == 'Signup':
        return '666'


def Login(receive,database):
    cur = database.cursor()
    cur = database.execute("SELECT Password FROM Customer WHERE Name = ?",(receive['username'],))
    rows = cur.fetchone()

    if rows[0] == receive['password']:
        flag = 'True'
    else:
        flag = 'False'
    send = {
        'Action' : 'Login',
        'flag' : flag
    }
    return send


