import select
import random
import sys


def flush_write(s):
    try:
        sys.stdout.write(s)
        sys.stdout.flush()
    except IOError:
        sys.exit(1)

def flush_write_err(s):
    try:
        sys.stderr.write(s)
        sys.stderr.flush()
    except IOError:
        sys.exit(1)

def doit():
    started = False
    reads = [sys.stdin]
    timeout = 0.5
    while True:
        rs, ws, es = select.select(reads, [], reads, timeout)
        if es:
            sys.stderr.write('Got error! Exiting!')
            sys.exit(1)
        if (not rs) and started:
            # write some random data to stdout
            r = random.randint(1, 1000)
            flush_write('Event: {}\nData: dummy\n\n'.format(r))
            flush_write_err('Wrote Event!\n')
            timeout = r / 1000.0
        elif rs:
            started = True
            flush_write_err('Waiting to read command\n')
            line = sys.stdin.readline()
            flush_write('Response: YOU SENT {}\n\n'.format(line.strip()))
            flush_write_err('Wrote Response!\n')
        elif es:
            flush_write_err('Got ERROR condition')

doit()
