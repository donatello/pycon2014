from gevent.monkey import patch_all
patch_all()

import gevent
import collections
import socket

HOST = '127.0.0.1'
PORT = 10000

class Transport(object):
    def __init__(self, host=HOST, port=PORT):
        self.sock = socket.socket()
        self.sock.connect((HOST, PORT))
        self.sock.settimeout(None)
        self.sockfd = self.sock.makefile()
        self.closed = False

    def write(self, data):
        if self.closed:
            return
        self.sockfd.write(bytearray(data, 'utf-8'))
        self.sockfd.flush()

    def readline(self):
        if self.closed:
            return ""
        return self.sockfd.readline()

    def close(self):
        self.closed = True
        self.sock.shutdown(2)
        self.sock.close()

def read_response(t):
    try:
        lines = []
        while (not lines) or lines[-1] != '\n':
            # print('read_response: lines {}'.format(lines))
            line = t.readline()
            if line == '':
                raise Exception('NoData!')
            lines.append(line)
        data = ''.join(lines[:-1])
        return data
    except KeyboardInterrupt:
        t.close()
        print('Exiting while read response')

def send_command(t, cid, cmd):
    t.write(cmd)

COMMANDS = collections.deque()
LOCK = gevent.lock.RLock()

def handle_event(data):
    print('Got Event Data: {}'.format(repr(data)))

def handle_responses(t):
    print('Starting responses handler')
    while True:
        resp = read_response(t)
        if resp.startswith('Event:'):
            gevent.spawn(handle_event, resp)
        else:
            # we got a command response
            cid, async_res = COMMANDS.popleft()
            # wake up waiting command
            async_res.set((cid, resp))

def commander(t, cid, cmd):
    async_res = gevent.event.AsyncResult()
    with LOCK:
        COMMANDS.append((cid, async_res))
        send_command(t, cid, cmd)
    # command sent to ESL - now block until response is got.
    _cid, resp = async_res.get()
    if cid != _cid:
        raise Exception('Commands out of sync!')
    return resp

def command_func(t, start, count):
    print('Greenlet with commands from {} to {} started!'.format(
        start, start + count))
    for cid in range(start, start + count):
        cmd = 'CMD - {}\n'.format(cid)
        resp = commander(t, cid, cmd)
        print('For CMD: {} Got RESP: {}'.format(repr(cmd), repr(resp)))
        gevent.sleep(1.5)
    return True

def start_command_greenlets(t, num_threads):
    threads = []
    for tno in range(num_threads):
        threads.append(gevent.spawn(command_func, t, tno*1000, 500))
    gevent.joinall(threads)
    if not all(map(lambda x: x.value, threads)):
        print('Greenlet had errors!')

if __name__ == '__main__':
    t = Transport()

    # start the response handler
    gevent.spawn(handle_responses, t)

    # start command threads
    start_command_greenlets(t, 5)

