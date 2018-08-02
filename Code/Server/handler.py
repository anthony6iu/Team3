# handler different actions.
# data is a dictionary.
import sqlite3
import json
import sys
import time


def handler(receive,database):
    action = receive['Action']
    if action == 'Login':
        return Login(receive,database)
    elif action == 'Logout':
        return Logout(receive,database)
    elif action == 'Signup':
        return Signup(receive,database)
    elif action == 'ReqAcc':
        return ReqAcc(receive,database)
    elif action == 'UpdAcc':
        return UpdAcc(receive,database)
    elif action == 'Search':
        return Search(receive,database)
    elif action == 'MakeRes':
        return MakeRes(receive,database)

# Login handler.
def Login(receive,database):
    cur = database.cursor()
    cur = database.execute("SELECT Password FROM Customer WHERE Username = ?",(receive['username'],))
    rows = cur.fetchone()
    if rows is None:
        flag = False
        note = 'No username matched.'
    elif rows[0] == receive['password']:
        flag = True
        note = 'Logged in.'
    else:
        flag = False
        note = 'Wrong password.'
    send = {
        'Action' : 'Login',
        'flag' : flag,
        'note' : note
    }
    if flag:
        cur.execute("INSERT INTO Online (Username, Logintime) \
        VALUES(?, ?)", (receive['username'],time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),))
        database.commit()
    return send

def Logout(receive,database):

    try:
        cur = database.cursor()
        cur.execute("DELETE FROM Online WHERE Username = ?",(receive['username'],))
        database.commit()
        send = {
            'Action' : 'Logout',
            'flag' : True
        }
    except:
        send = {
            'Action' : 'Logout',
            'flag' : False
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


# Search handler.
def Search(receive,database):

    flag = True
    content = []
    try:
        for a,b,c,d,e in database.execute("SELECT * FROM Movie WHERE " + receive['filter'] + " = ?",(receive['text'],)):
            movie = {
                'name' : b,
                'type' : c,
                'description' : d,
                'actors' : e
            }
            print(movie)
            content.insert(len(content)+1,movie)
        send = {
            'Action' : 'Search',
            'flag' : flag,
            'content' : content
        }

    except:
        flag = False
        send = {
            'Action' : 'Search',
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
