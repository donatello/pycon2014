import sys
import os
import time
from flask import Flask, jsonify
from flask.ext.sqlalchemy import SQLAlchemy


if "PSYCOGREEN" in os.environ:

    # monkey patching
    from gevent.monkey import patch_all
    patch_all()
    from psycogreen.gevent import patch_psycopg
    patch_psycopg()

    using_gevent = True
else:
    using_gevent = False


# Create our Flask app
#
app = Flask(__name__)
app.config.from_pyfile('config.py')


# Create our Flask-SQLAlchemy instance
#
db = SQLAlchemy(app)
if using_gevent:

    # Assuming that gevent monkey patched the builtin
    # threading library, we're likely good to use
    # SQLAlchemy's QueuePool, which is the default
    # pool class.  However, we need to make it use
    # threadlocal connections
    #
    #
    db.engine.pool._use_threadlocal = True


class Account(db.Model):
    """ Simple Model
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    is_enabled = db.Column(db.Boolean)
    priority = db.Column(db.Integer)

    def as_dict(self):
        """ Individual Account as dict.
        """
        return {
            'id': self.id,
            'title': self.name,
            'done': self.is_enabled,
            'priority': self.priority
        }

    @classmethod
    def jsonify_all(cls):
        """ Get all accounts and format to Json
        """
        return jsonify(accounts=[account.as_dict() for account in cls.query.all()])


@app.route('/sleep/postgres/')
def sleep_postgres():
    """ This handler asks Postgres to sleep for 5s and will
        block for 5s unless psycopg2 is set up (above) to be
        gevent-friendly.
    """
    db.session.execute('SELECT pg_sleep(5)')
    return Account.jsonify_all()


@app.route('/sleep/python/')
def sleep_python():
    """ This handler sleeps for 5s and will block for 5s unless
        the webserver is using the gevent worker class.
    """
    time.sleep(5)
    return Account.jsonify_all()


# Initialize db with some dummy data
#
def create_data():
    db.create_all()
    accounts = []
    for i in range(50):
        account = Account(
            name="USER_NAME_{}".format(i),
            is_enabled=(i % 2 == 0),
            priority=(i % 5)
        )
        accounts.append(account)
    db.session.add_all(accounts)
    db.session.commit()


if __name__ == '__main__':

    if '-c' in sys.argv:
        create_data()
    else:
        app.run()
