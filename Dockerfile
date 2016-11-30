# DIOE
FROM ubuntu:14.04

# INSTALL EVERYTHING (”-y” WITHOUT ASKING FOR PERMISSION)
RUN apt-get update
RUN apt-get install -y git
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-dev
RUN apt-get install -y python3-setuptools
RUN apt-get install -y nginx
RUN apt-get install -y supervisor
RUN apt-get install -y sqlite3
RUN apt-get install -y postgresql-client
RUN rm -rf /var/lib/apt/lists/*

RUN pip3 install uwsgi

# NGINX STANDARD SETUP
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY nginx-app.conf /etc/nginx/sites-available/default
COPY supervisor-app.conf /etc/supervisor/conf.d/

COPY app/requirements.txt /home/docker/code/app/
RUN pip3 install -r /home/docker/code/app/requirements.txt

# ADD (THE REST OF) OUR CODE
COPY . /home/docker/code/

EXPOSE 80
CMD ["supervisord", "-n"]
