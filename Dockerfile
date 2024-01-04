# DIOE
FROM ubuntu:20.04
ENV TZ=Europe/Vienna
ENV DEBIAN_FRONTEND=noninteractive
# COLLECT ALL STATIC FILES IN /STATIC
ENV DIOEDB_STATIC_URL=/static/
ENV DIOEDB_STATIC_ROOT=/static
# ADD SOURCES FOR BUILD DEPENDENCIES
RUN \
  --mount=type=cache,target=/var/cache/apt,sharing=locked \
  --mount=type=cache,target=/var/lib/apt,sharing=locked \
  rm -f /etc/apt/apt.conf.d/docker-clean && \
  echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' >/etc/apt/apt.conf.d/keep-cache && \
  ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
  apt-get update && apt-get install -y apt-transport-https software-properties-common curl gnupg && \
  echo "deb-src http://in.archive.ubuntu.com/ubuntu/ bionic main restricted" >> /etc/apt/sources.list && \
  echo "deb-src http://in.archive.ubuntu.com/ubuntu/ bionic-updates main restricted" >> /etc/apt/sources.list && \
  curl -sL https://deb.nodesource.com/setup_10.x | grep -v deprecation_warning\$ | bash && apt-get install -y --force-yes nodejs && \  
  add-apt-repository ppa:deadsnakes/ppa && \
  apt-get update

# INSTALL EVERYTHING (”-y” WITHOUT ASKING FOR PERMISSION)
RUN \
  --mount=type=cache,target=/var/cache/apt,sharing=locked \
  --mount=type=cache,target=/var/lib/apt,sharing=locked \
  apt-get install -y --force-yes git python3.5 python3.5-dev python3-pip python3-setuptools \
  nginx supervisor sqlite3 postgresql-client && \
  rm /usr/bin/python3 && \
  ln -s /usr/bin/python3.5 /usr/bin/python3

# RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
# RUN python3.5 get-pip.py

# ADD (THE REST OF) OUR CODE
COPY . /home/docker/code/

RUN \
  --mount=type=cache,target=/var/cache/apt,sharing=locked \
  --mount=type=cache,target=/var/lib/apt,sharing=locked \
  apt-get install -y libpq-dev libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev \
  libwebp-dev libharfbuzz-dev libfribidi-dev tcl8.6-dev tk8.6-dev python-tk && \
  # CLEAN UP \
  # rm -rf /var/lib/apt/lists/* && \
  # Install psycopg2-binary \
  # apt-get build-dep -y python-psycopg2 && \
  # INSTALL UWSGI \
  pip3 install psycopg2-binary && \
  pip3 install uwsgi && \
  # NGINX STANDARD SETUP \
  echo "daemon off;" >> /etc/nginx/nginx.conf && \
  cp /home/docker/code/nginx-gzip.conf /etc/nginx/conf.d/ && \
  cp /home/docker/code/nginx-app.conf /etc/nginx/sites-available/default && \
  cp /home/docker/code/supervisor-app.conf /etc/supervisor/conf.d/ && \
    # INSTALL PYTHON MODULES \
    # COPY app/requirements.txt /home/docker/code/app/ \
    pip3 install -r /home/docker/code/app/requirements.txt && \
    # Webpacks \
    mkdir -p /home/docker/code/webpack_src/ && \
    # Tagsystem VUE Komponente \
    git clone https://github.com/german-in-austria/tagsystemVUE /home/docker/code/webpack_src/tagsystemVUE --branch v0.04 --depth 1 && \
    cd /home/docker/code/webpack_src/tagsystemVUE && npm install && npm run build && \
    # Annotations Tool \
    git clone https://github.com/german-in-austria/annotationsDB-frontend /home/docker/code/webpack_src/annotationsDB --branch v0.61.0 --depth 1 && \
    cd /home/docker/code/webpack_src/annotationsDB && npm install && npm run build && \
    # Anno-sent \
    # COPY webpack_src/annoSent /home/docker/code/webpack_src/annoSent/ \
    cd /home/docker/code/webpack_src/annoSent && npm install && npm run build && \
    # Anno-check \
    # COPY webpack_src/annoCheck /home/docker/code/webpack_src/annoCheck/ \
    cd /home/docker/code/webpack_src/annoCheck && npm install && npm run build && \
    python3.5 /home/docker/code/app/manage.py collectstatic --noinput

EXPOSE 80
CMD ["supervisord", "-n"]
