rm -f /tmp/f ; mkfifo /tmp/f ; cat /tmp/f  | python fssim.py  | nc -l 127.0.0.1 10000 > /tmp/f  
