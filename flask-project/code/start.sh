/etc/init.d/rsyslog start

/etc/init.d/postgresql start

su -c "psql -U postgres -f /home/project/code/db.sql" postgres

/etc/init.d/nginx start
/usr/local/bin/uwsgi --ini /home/project/uwsgi.ini

python /home/project/code/server.py -c
