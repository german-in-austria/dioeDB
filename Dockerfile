# DIOE
FROM ubuntu:14.04

# INSTALL EVERYTHING (”-y” WITHOUT ASKING FOR PERMISSION)
RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:fkrull/deadsnakes
RUN apt-get update
RUN apt-get install -y git
RUN apt-get install -y python3.5
RUN rm /usr/bin/python3
RUN ln -s /usr/bin/python3.5 /usr/bin/python3
RUN apt-get install -y python3-pip
RUN apt-get install -y python3.5-dev
RUN apt-get install -y python3-setuptools
RUN apt-get install -y nginx
RUN apt-get install -y supervisor
RUN apt-get install -y sqlite3
RUN apt-get install -y postgresql-client
RUN apt-get build-dep -y python-psycopg2

RUN apt-get update
RUN apt-get install -y libtiff5-dev
RUN apt-get install -y libjpeg8-dev
RUN apt-get install -y zlib1g-dev
RUN apt-get install -y libfreetype6-dev
RUN apt-get install -y liblcms2-dev
RUN apt-get install -y libwebp-dev
RUN apt-get install -y libharfbuzz-dev
RUN apt-get install -y libfribidi-dev
RUN apt-get install -y tcl8.6-dev
RUN apt-get install -y tk8.6-dev
RUN apt-get install -y python-tk

# CLEAN UP
RUN rm -rf /var/lib/apt/lists/*

# INSTALL UWSGI
RUN pip3 install uwsgi

# NGINX STANDARD SETUP
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY nginx-app.conf /etc/nginx/sites-available/default
COPY supervisor-app.conf /etc/supervisor/conf.d/

# INSTALL PYTHON MODULES
COPY app/requirements.txt /home/docker/code/app/
RUN pip3 install -r /home/docker/code/app/requirements.txt
RUN pip3 install psycopg2

# ADD (THE REST OF) OUR CODE
COPY . /home/docker/code/

# COLLECT ALL STATIC FILES IN /STATIC
ENV DIOEDB_STATIC_ROOT=/static
RUN python3 /home/docker/code/app/manage.py collectstatic --noinput

EXPOSE 80
CMD ["supervisord", "-n"]
