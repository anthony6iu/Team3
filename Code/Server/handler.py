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
    elif action == 'Signup':
        return Signup(receive,database)
    elif action == 'Logout' and isOnline(receive['user'],database):
        return Logout(receive,database)
    elif action == 'ReqAcc' and isOnline(receive['user'],database):
        return ReqAcc(receive,database)
    elif action == 'UpdAcc' and isOnline(receive['user'],database):
        return UpdAcc(receive,database)
    elif action == 'Search' and isOnline(receive['user'],database):
        return Search(receive,database)
    elif action == 'MovieInfo' and isOnline(receive['user'],database):
        return MovieInfo(receive,database)
    elif action == 'UpdAccount' and isOnline(receive['user'],database):
        return UpdAccount(receive,database)
    elif action == 'DisShow' and isOnline(receive['user'],database):
        return DisShow(receive,database)
    elif action == 'DisSeat' and isOnline(receive['user'],database):
        return DisSeat(receive,database)
    elif action == 'UpdSeat' and isOnline(receive['user'],database):
        return UpdSeat(receive,database)
    elif action == 'MakeRes' and isOnline(receive['user'],database):
        return MakeRes(receive,database)
    elif action == 'Pay' and isOnline(receive['user'],database):
        return Pay(receive,database)
    elif action == 'ShowRes'and isOnline(receive['user'],database):
        return ShowRes(receive,database)
    elif action == 'CancRes' and isOnline(receive['user'],database):
        return CancRes(receive,database)
    else:
        return {
            'Action' : 'Logout',
            'flag' : True
        }

def isOnline(user,database):
    try:
        cur = database.cursor()
        cur = database.execute("SELECT * FROM Online WHERE Username = ?",(user,))
        obj = cur.fetchone()
        if obj is None:
            flag = False
        else:
            flag = True
    except:
        flag = False
    return flag

# Login handler.
def Login(receive,database):
    cur = database.cursor()
    cur = database.execute("SELECT Password FROM Customer WHERE Username = ?",(receive['username'],))
    rows = cur.fetchone()
    if rows is None:
        flag = False
        note = 'No username matched.',
        user = None
    elif rows[0] == receive['password']:
        flag = True
        note = 'Logged in.',
        user = receive['username']
    else:
        flag = False
        note = 'Wrong password.',
        user = None
    send = {
        'Action' : 'Login',
        'flag' : flag,
        'note' : note,
        'user' : user
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
            'user' : receive['username'],
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
            'user' : receive['username'],
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
            'user' : receive['user'],
            'flag' : False
        }
        return send

    try:
        cur.execute("UPDATE Customer SET Firstname = ?, Lastname = ?, Email = ?, Phone = ? WHERE Username = ?",
            (receive['firstname'], receive['lastname'], receive['email'], receive['phone'], receive['username'],))
    except:
        flag = False

    database.commit()
    print('6666666')
    send = {
        'Action' : 'UpdAcc',
        'user' : receive['user'],
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

'''
Search handler.
Demo for searching by Type.
'''
def Search(receive,database):
    content = []
    cur = database.cursor()
    try:
        cur.execute("SELECT ID, Name FROM Movie WHERE " + receive['filter'] + " = ?",(receive['text'],))
        movies = cur.fetchall()
        if len(movies) == 0:
            send = {
                'Action' : 'Search',
                'flag' : False,
                'content' : None
            }
            return send
        for movie in movies:
            try:
                cur.execute("SELECT Cinema.Cinemaname, Show.Showtime, Show.Screenid, Show.Showid FROM Show INNER JOIN Cinema ON Show.Cinemaid = Cinema.Cinemaid WHERE Show.Movieid = ?",(movie[0],))
                shows = cur.fetchall()
                for show in shows:
                    case = {
                    'movie' : movie[1],
                    'cinema' : show[0],
                    'showtime' : show[1],
                    'screen' : show[2],
                    'sid' : show[3]
                    }
                    content.insert(len(content)+1,case)
            except:
                case = {
                    'movie' : movie[1],
                    'cinema' : None,
                    'showtime' : None,
                    'screen' : None,
                    'sid' : None
                }
                content.insert(len(content)+1, case)
        send = {
            'Action' : 'Search',
            'flag' : True,
            'content' : content
        }
    except:
        send = {
            'Action' : 'Search',
            'flag' : False,
            'content' : None
        }
    return send


'''
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
            'flag' : flag,
            'content' : None
        }
    return send
'''
'''
Check Show table, and response wtih all attributes in Show table.
receive message json format:
{
    'Action'  : 'DisShow',
    'filter'    : 'moviename', # can be showtime, cinemaname as well.
    'text' : 'keyword'
}
'''

def DisSeat(receive,database):
    c1 = database.cursor()
    try:
        c1.execute("SELECT Row0, Row1, Row2, Row3, Row4 FROM Show WHERE Showid = ?",(receive['sid'],))
        smap = c1.fetchone()
        send = {
            'Action' : 'DisSeat',
            'flag' : True,
            'sid' : receive['sid'],
            'r0' : smap[0],
            'r1' : smap[1],
            'r2' : smap[2],
            'r3' : smap[3],
            'r4' : smap[4]
        }
        return send
    except:
        send = {
            'Action' : 'DisSeat',
            'flag' : False,
            'sid' : receive['sid'],
            'r0' : None,
            'r1' : None,
            'r2' : None,
            'r3' : None,
            'r4' : None
        }
        return send

def UpdSeat(receive,database):
    c1 = database.cursor()
    try:
        c1.execute("UPDATE Show SET Row0 = ?, Row1 = ?, Row2 = ?, Row3 = ?, Row4 = ? WHERE Showid = ?",
            (receive['r0'],receive['r1'],receive['r2'],receive['r3'],receive['r4'],receive['sid'],))
        database.commit()
        send = {
            'Action' : 'UpdSeat',
            'flag' : True
        }
        return send
    except:
        send = {
            "Action" : 'UpdSeat',
            'flag' : False
        }
        return send

def DisShow(receive,database):
    c1 = database.cursor()
    content = []
    send = {
        'Action' : 'DisShow',
        'flag' : False,
        'content' : content
    }
    if receive['filter'] == 'moviename':
        try:
            c1.execute("SELECT Movieid, Showtime, Cinemaid, Screenid, Row0, Row1, Row2, Row3, Row4 FROM Show INNER JOIN Movie ON Show.Movieid = Movie.ID WHERE Movie.Name = ?",(receive['text'],))
            shows = c1.fetchall()
            for show in shows:
                c1 = c1.execute("SELECT Cinemaname FROM Cinema WHERE Cinema.Cinemaid = ?",(show[2],))
                cname = c1.fetchone()
                cell = {
                    'moviename' : receive['text'],
                    'showtime' : show[1],
                    'cinemaname' : cname[0],
                    'screenid' : show[3],
                    'row0' : show[4],
                    'row1' : show[5],
                    'row2' : show[6],
                    'row3' : show[7],
                    'row4' : show[8]
                }

                content.insert(len(content)+1, cell)
            send['flag'] = True
        except:
            content = None

    elif receive['filter'] == 'showtime':
        try:
            c1.execute("SELECT Movieid, Showtime, Cinemaid, Screenid, Row0, Row1, Row2, Row3, Row4 FROM Show WHERE Showtime = ?",(receive['text'],))
            shows = c1.fetchall()
            for show in shows:
                c1 = c1.execute("SELECT Cinemaname FROM Cinema WHERE Cinemaid = ?",(show[2],))
                cname = c1.fetchone()
                c1 = c1.execute("SELECT Name FROM Movie WHERE ID = ?",(show[0],))
                mname = c1.fetchone()
                
                cell = {
                    'moviename' : mname[0],
                    'showtime' : show[1],
                    'cinemaname' : cname[0],
                    'screenid' : show[3],
                    'row0' : show[4],
                    'row1' : show[5],
                    'row2' : show[6],
                    'row3' : show[7],
                    'row4' : show[8]
                }
                content.insert(len(content)+1, cell)
            send['flag'] = True
        except:
            content  = None

    elif receive['filter'] == 'cinemaname':

        try:
            c1.execute("SELECT Cinemaid FROM Cinema WHERE Cinemaname = ?",(receive['text'],))
            cid = c1.fetchone()
            c1.execute("SELECT Movieid, Showtime, Cinemaid, Screenid, Row0, Row1, Row2, Row3, Row4 FROM Show WHERE Cinemaid = ?",(cid[0],))
            shows = c1.fetchall()
            for show in shows:
                c1 = c1.execute("SELECT Name FROM Movie WHERE ID = ?",(show[0],))
                mname = c1.fetchone()

                cell = {
                    'moviename' : mname[0],
                    'showtime' : show[1],
                    'cinemaname' : receive['text'],
                    'screenid' : show[3],
                    'row0' : show[4],
                    'row1' : show[5],
                    'row2' : show[6],
                    'row3' : show[7],
                    'row4' : show[8]
                }
                content.insert(len(content)+1, cell)
            send['flag'] = True
        except:
            content = None

    else:
        content = None

    return send


# MakeRes handler.
def MakeRes(receive,database):
    cur = database.cursor()
    cur.execute("INSERT INTO Reservation (Resid, Username, Moviename, Cinemaname, Showtime, Seat) \
        VALUES (?, ?, ?, ?, ?, ?)",
         (None,receive['username'],receive['moviename'],
            receive['cinemaname'],receive['showtime'],receive['seat']))
    database.commit()
    try:
        cur = database.cursor()
        cur.execute("SELECT Resid FROM Reservation WHERE Username = ? AND Moviename = ? AND Cinemaname = ? AND Showtime = ? AND Seat = ?",
            (receive['username'],receive['moviename'],receive['cinemaname'],receive['showtime'],receive['seat'],))
        rid = cur.fetchone()
        send = {
            'Action' : 'MakeRes',
            'flag'  : True,
            'resid' : rid[0] 
        }
    except:
        send = {
            'Action' : 'MakeRes',
            'flag'   : False
        }
    return send


#Pay session
def Pay(receive,database):
    #connect to 3rd party interface.
    #return successful transaction.
    #then...
    cur = database.cursor()
    try:
        cur.execute("UPDATE Reservation SET Paid = 'YES' WHERE Resid = ?",(receive['resid'],))
        database.commit()
        send = {
            'Action' : 'Pay',
            'flag' : True
        }
    except:
        send = {
            'Action' : 'Pay',
            'flag' : False
        }
    return send


#Show this user all reservation infos.
def ShowRes(receive,database):
    cur = database.cursor()
    content = []
    try:
        cur.execute("SELECT * FROM Reservation WHERE Username = ?",(receive['user'],))
        ress = cur.fetchall()
        if len(ress) == 0:
            send = {
                'Action' : 'ShowRes',
                'flag' : False,
                'content' : None
            }
            return send
        for res in ress:
            cell = {
                'resid' : res[0],
                'moviename' : res[2],
                'cinemaname' : res[3],
                'showtime' : res[4],
                'seat' : res[5],
                'paid' : res[6]
            }
            content.insert(len(content)+1, cell)
        send = {
            'Action' : 'ShowRes',
            'flag' : True,
            'content' : content
        }
    except:
        send  = {
            'Action' : 'ShowRes',
            'flag' : False,
            'content' : None
        }
    return send


# Cancal reservation by given resid.
def CancRes(receive,database):
    try:
        cur = database.cursor()
        cur.execute("DELETE FROM Reservation WHERE Resid = ?",(receive['resid'],))
        database.commit()
        send = {
            'Action' : 'CancRes',
            'flag' : True
        }
    except:
        send = {
            'Action' : 'CancRes',
            'flag' : False
        }
    return send


def MovieInfo(receive, database):
    c1 = database.cursor()
    try:
        c1.execute("SELECT Type, Description, Actors FROM Movie WHERE Name = ?",(receive['moviename'],))
        info = c1.fetchone()
        print(info)
        send = {
            'Action' : 'MovieInfo',
            'flag' : True,
            'type' : info[0],
            'description' : info[1],
            'actors' : info[2]
        }
        return send
    except:
        send = {
            'Action' : 'MovieInfo',
            'flag' : False,
            'type' : None,
            'description' : None,
            'actors' : None
        }

def UpdAccount(receive, database):
    c1 = database.cursor()
    try:
        cur.execute("UPDATE Customer SET Firstname = ?, Lastname = ?, Email = ?, Phone = ?, Password = ? WHERE Username = ?",
            (receive['firstname'], receive['lastname'], receive['email'], receive['phone'], receive['password'], receive['username'],))
        database.commit()
        send = {
            'Action' : 'UpdAccount',
            'flag' : True
        }
        return send
    except:
        send = {
            'Action' : 'UpdAccount',
            'flag' : False
        }
        return send




