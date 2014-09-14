from gevent.monkey import patch_all
patch_all()

import time
from flask import Flask

app = Flask(__name__)

@app.route('/hello/')
def hello():
    time.sleep(1) # yeah work being dne here!
    return "Hello World!"
