# Keep the legacy application runtimes without relying on retired APT repositories.
FROM node:10.24.1-buster-slim AS node
FROM python:3.5.10-slim-buster

COPY --from=node /usr/local/bin/node /usr/local/bin/node
COPY --from=node /usr/local/lib/node_modules/npm /usr/local/lib/node_modules/npm
RUN ln -s /usr/local/lib/node_modules/npm/bin/npm-cli.js /usr/local/bin/npm
ENV TZ=Europe/Vienna
ENV DEBIAN_FRONTEND=noninteractive
# COLLECT ALL STATIC FILES IN /STATIC
ENV DIOEDB_STATIC_URL=/static/
ENV DIOEDB_STATIC_ROOT=/static
# Debian Buster is archived; use its signed archive instead of live mirrors.
RUN \
  --mount=type=cache,target=/var/cache/apt,sharing=locked \
  --mount=type=cache,target=/var/lib/apt,sharing=locked \
  rm -f /etc/apt/apt.conf.d/docker-clean && \
  echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' >/etc/apt/apt.conf.d/keep-cache && \
  printf '%s\n' \
    'deb http://archive.debian.org/debian buster main' \
    'deb http://archive.debian.org/debian-security buster/updates main' > /etc/apt/sources.list && \
  apt-get update && apt-get install -y --no-install-recommends \
    build-essential ca-certificates git tzdata nginx supervisor sqlite3 postgresql-client \
    libpq-dev libtiff5-dev libjpeg62-turbo-dev zlib1g-dev libfreetype6-dev liblcms2-dev \
    libwebp-dev libharfbuzz-dev libfribidi-dev tcl8.6-dev tk8.6-dev && \
  ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# ADD (THE REST OF) OUR CODE
COPY . /home/docker/code/

RUN \
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
