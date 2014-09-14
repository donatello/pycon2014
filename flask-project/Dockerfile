FROM      ubuntu

RUN apt-get update && apt-get install -y git python-virtualenv wget ca-certificates
RUN bash -c "wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -"
RUN bash -c "wget --quiet -O - http://nginx.org/keys/nginx_signing.key | apt-key add -"
RUN bash -c "echo deb http://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main > /etc/apt/sources.list.d/pgdg.list"
RUN bash -c "echo deb http://nginx.org/packages/ubuntu/ trusty nginx > /etc/apt/sources.list.d/nginx.list"
RUN apt-get update && apt-get upgrade -y && sudo apt-get install -y postgresql-9.3 emacs23-nox vim nginx libpq-dev python-dev curl byobu

# setup environment for project
RUN mkdir -p /home/project
ADD requirements.txt /home/project/requirements.txt
RUN pip install -r /home/project/requirements.txt

# copy code
ADD code/ /home/project/code

# copy nginx config
ADD nginx/nginx.conf /etc/nginx/nginx.conf
RUN rm -rf /etc/nginx/conf.d/*
ADD nginx/mysite.conf /etc/nginx/conf.d/mysite.conf

# copy uswgi config
ADD uwsgi/uwsgi.ini /home/project/uwsgi.ini

