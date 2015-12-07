# methods: insert, update, query
# call Network class

'''
    Simple socket server using threads
    from: http://www.binarytides.com/python-socket-server-code-example/
'''
import socket
import sys
from QueryEngine import QueryEngine
from QueryEngine import QueryType
from enum import Enum
from thread import *
from Constants import Constants
from db import db

HOST = '127.0.0.1'   # Symbolic name meaning all available interfaces
PORT = 8000 # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

#Bind socket to local host and port
try:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, Constants.PORT))
    
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

#Start listening on socket
s.listen(10)
print 'Socket now listening'

#Function for handling connections. This will be used to create threads
def clientthread(conn):
    qe = QueryEngine()
    #Sending message to connected client
    #conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string

    #infinite loop so that function do not terminate and thread do not end.
    while True:
        #Receiving from client
        reply = ''
        data = conn.recv(1024)
        print data
        
        params = qe.deserialize(data)
        param_type = params[0]
        print param_type
        print 'PARAMS', params
        if param_type == QueryType.SELECT:
            reply = db.select(msToSec(params[1]), params[2])

        elif param_type == QueryType.INSERT:
            if params[2]=='':
                pass
            else:
                db.insert(msToSec(params[1]),params[2], params[3])
                reply = "inserting " + data
            
            #reply = db.insert(params[1:])
        elif param_type == QueryType.UPDATE:
            reply = "updating"
            #reply = db.update(params[1:])
        elif param_type == QueryType.SELECTRANGE:
            reply = db.selectRangeForDisplay(msToSec(params[1]), msToSec(params[2]), params[3])
        else:
            # throw exception
            reply = "Invalid arguments, should be start with SELECT, INSERT, or UPDATE"
        print reply
        conn.sendall(reply)
    
        
            #conn.close()
    conn.close()

def msToSec(milliseconds):
    return milliseconds/1000
#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])

    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn,))

s.close()
