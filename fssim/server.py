import socket
import select
import sys
from thread import start_new_thread

HOST, PORT = '127.0.0.1', 30001

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setblocking(0)
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

s.listen(100)

def clientthread(conn):

    read = [conn]
    while True:
        print('Waiting...')
        r, w, e = select.select(read, [], read, 1)
        if not r and not e:
            print('Got timeout!')
            conn.sendall('You timed out!')
        else:
            data = conn.recv(1024)
            if len(data) >= 1024:
                print("Too much data!")
                sys.exit(1)
            print('Got from Client: {}'.format(data))
            conn.sendall('Ok you sent: {}')

    # #Sending message to connected client
    # conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string
     
    # #infinite loop so that function do not terminate and thread do not end.
    # while True:
         
    #     #Receiving from client
    #     data = conn.recv(1024)
    #     reply = 'OK...' + data
    #     if not data:
    #         break
     
    #     conn.sendall(reply)
     
    # #came out of loop
    conn.close()
 
#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
     
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn,))
 
s.close()


