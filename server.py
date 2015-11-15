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
 
HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
#Start listening on socket
s.listen(10)
print 'Socket now listening'
 
#Function for handling connections. This will be used to create threads
def clientthread(conn):
    QueryEngine qe = QueryEngine()
    #Sending message to connected client
    conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string
     
    #infinite loop so that function do not terminate and thread do not end.
    while True:
        #Receiving from client
        data = conn.recv(1024)
        print data
        params = qe.deserialize(data)
        param_type = params[0]

        if param_type == QueryType.SELECT:
            reply = "selecting"
            #reply = db.select(params[1:])
        elif param_type == QueryType.INSERT:
            reply = "inserting"
            #reply = db.insert(params[1:])
        elif param_type == QueryType.UPDATE:
            reply = "updating"
            #reply = db.update(params[1:])
        else:
            # throw exception
            reply = "Invalid arguments, should be start with SELECT, INSERT, or UPDATE"
     
        conn.sendall(reply)
     
    conn.close()
 
#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
     
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn,))
 
s.close()
