FROM python:3.5

# COPY SOURCE
COPY . /usr/src/app

# CHANGE DIR
WORKDIR /usr/src/app

# INSTALL DEPENDENCIES
COPY requirements.txt ./
RUN pip install -r requirements.txt

# INSTALL UWSGI
RUN pip install uwsgi

# INSTALL POSTGRES, SQLITE & NGINX
RUN apt-get update
RUN apt-get install -y --no-install-recommends \
    postgresql-client \
    sqlite3 \
    nginx \
    && rm -rf /var/lib/apt/lists/*

RUN uwsgi --chdir=. \
  --module=dioeDB.wsgi:application \
  --env DJANGO_SETTINGS_MODULE=dioeDB.settings \
  --master --pidfile=/tmp/project-master.pid \
  # can also be a file
  --socket=127.0.0.1:49152 \
  # number of worker processes
  --processes=5 \
  # if root, uwsgi can drop privileges
  --uid=1000 --gid=2000 \
  # respawn processes taking more than 20 seconds
  --harakiri=20 \
  # respawn processes after serving 5000 requests
  --max-requests=5000 \
  # clear environment on exit
  --vacuum \
  # background the process
  --daemonize=/var/log/uwsgi/yourproject.log

# Make NGINX run in the foreground
# RUN echo "daemon off;" >> /etc/nginx/nginx.conf
# # Remove default configuration from Nginx
# RUN rm /etc/nginx/conf.d/default.conf
# # Copy the modified Nginx conf
# COPY nginx.conf /etc/nginx/conf.d/
# # Copy the base uWSGI ini file to enable default dynamic uwsgi process number
# COPY uwsgi.ini /etc/uwsgi/


EXPOSE 49152

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
