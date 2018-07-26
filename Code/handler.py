# handler different actions.
# data is a dictionary.
import sqlite3
import json
import sys


def handler(receive,database):
    action = receive['Action']
    if action == 'Login':
        return Login(receive,database)
    elif action == 'Signup':
        return Signup(receive,database)
    elif action == 'ReqAcc':
        return ReqAcc(receive,database)
    elif action == 'UpdAcc':
        return UpdAcc(receive,database)
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


# ManAcc handler.
#  step 1: Request account information.
def ReqAcc(receive,database):
    cur = database.cursor()

    try:
        cur = database.execute("SELECT Firstname, Lastname, Email, Phone FROM Customer WHERE Username = ?", (receive['username'],))
        row = cur.fetchone()
        send = {
            'Action' : 'ReqAcc',
            'flag' : True,
            'username' : receive['username'],
            'firstname' : row[0],
            'lastname' : row[1],
            'email' : row[2],
            'phone' : row[3]
        }
    except:
        send = {
            'Action' : 'ReqAcc',
            'flag' : False,
            'username' : receive['username'],
            'firstname' : None,
            'lastname' : None,
            'email' : None,
            'phone' : None
        }
    database.commit()
    return send

# step 2: update account information.
def UpdAcc(receive,database):
    cur = database.cursor()

    flag = True
    if not receive['flag']:
        send = {
            'Action' : 'UpdAcc',
            'flag' : False
        }
        return send

    try:
        cur.execute("UPDATE Customer SET Firstname = ?, Lastname = ?, Email = ?, Phone = ? WHERE Username = ?",
            (receive['firstname'], receive['lastname'], receive['email'], receive['phone'], receive['username'],))
    except:
        flag = False

    database.commit()
    send = {
        'Action' : 'UpdAcc',
        'flag' : flag
    }
    return send


# Signup handler.
def Signup(receive,database):
    cur = database.cursor()

    flag = True
    try:
        cur.execute("INSERT INTO Customer (Username, Password, Firstname, Lastname, Email, Phone) \
            VALUES (?, ?, ?, ?, ?, ?)",
             (receive['username'],receive['password'],receive['firstname'],
                receive['lastname'],receive['email'],receive['phone']))
    except:
        flag = False

    database.commit()
    send = {
        'Action' : 'Signup',
        'flag' : flag
    }
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


