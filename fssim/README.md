This example contains a server program that behaves approximately like
a FreeSWITCH Event Socket. The FreeSWITCH Event Socket responds to
commands and sends Events via the same socket.

The client program demonstrates using Gevent to talk to the event
socket in a non-blocking way using Gevent's synchronisation features,
namely, locking and AsyncResult.

To start the server:

```
bash start_server.sh
```

To observe how the server works, use nc and enter some text. The
server will respond and terminate it's response with a blank
line. After the first request is made, the server also starts sending
events to the client:

```
$ nc localhost 10000
hi
Response: YOU SENT hi

Event: 735
Data: dummy

Event: 878
Data: dummy

abc
Response: YOU SENT abc
```

Running the client program after starting the server, demonstrates
that the command sending greenlets and the greenlet that listens for
data sent by the server. The listening greenlet, spawns new greenlets
to handle events received, and sends the responses of commands to the
greenlets that sent them by using a `gevent.event.AsyncResult`:

```
$ python client.py 
Starting responses handler
Greenlet with commands from 0 to 500 started!
Greenlet with commands from 1000 to 1500 started!
Greenlet with commands from 2000 to 2500 started!
Greenlet with commands from 3000 to 3500 started!
Greenlet with commands from 4000 to 4500 started!
For CMD: 'CMD - 0\n' Got RESP: 'Response: YOU SENT CMD - 0\n'
For CMD: 'CMD - 1000\n' Got RESP: 'Response: YOU SENT CMD - 1000\n'
For CMD: 'CMD - 2000\n' Got RESP: 'Response: YOU SENT CMD - 2000\n'
For CMD: 'CMD - 3000\n' Got RESP: 'Response: YOU SENT CMD - 3000\n'
For CMD: 'CMD - 4000\n' Got RESP: 'Response: YOU SENT CMD - 4000\n'
Got Event Data: 'Event: 103\nData: dummy\n'
Got Event Data: 'Event: 295\nData: dummy\n'
Got Event Data: 'Event: 569\nData: dummy\n'
Got Event Data: 'Event: 465\nData: dummy\n'
For CMD: 'CMD - 1\n' Got RESP: 'Response: YOU SENT CMD - 1\n'
For CMD: 'CMD - 1001\n' Got RESP: 'Response: YOU SENT CMD - 1001\n'
For CMD: 'CMD - 2001\n' Got RESP: 'Response: YOU SENT CMD - 2001\n'
For CMD: 'CMD - 3001\n' Got RESP: 'Response: YOU SENT CMD - 3001\n'
For CMD: 'CMD - 4001\n' Got RESP: 'Response: YOU SENT CMD - 4001\n'
```
