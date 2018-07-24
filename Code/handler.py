# handler different actions.
# data is a dictionary.
import sqlite3
import json
import sys


def handler(receive,database):
    action = receive['Action']
    if action == 'Login':
        return Login(receive,database)
    elif action  == 'Signup':
        return Signup(receive,database)
    elif action == 'MakeRes':
        return MakeRes(receive,database)

# Login handler.
def Login(receive,database):
    cur = database.cursor()
    cur = database.execute("SELECT Password FROM Customer WHERE Username = ?",(receive['username'],))
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

# Signup handler.
def Signup(receive,database):
    cur = database.cursor()
    cur.execute("INSERT INTO Customer (Username, Password, Firstname, Lastname, Email, Phone) \
        VALUES (?, ?, ?, ?, ?, ?)",
         (receive['username'],receive['password'],receive['firstname'],
            receive['lastname'],receive['email'],receive['phone']))
    send = {
        'Action' : 'Signup',
        'flag' : 'True'
    }
    database.commit()
    return send

# MakeRes handler.
def MakeRes(receive,database):
    cur = database.cursor()
    cur.execute("INSERT INTO Reservation (Resid, Username, Moviename, Location, Showtime, Seat) \
        VALUES (?, ?, ?, ?, ?, ?)",
         (None,receive['username'],receive['moviename'],
            receive['location'],receive['showtime'],receive['seat']))
    send = {
        'Action' : 'MakeRes',
        'flag' : 'True'
    }
    database.commit()
    return send


