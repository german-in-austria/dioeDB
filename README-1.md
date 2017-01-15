##dioe db tutorial

### start a postgres db
`docker run -p 5432:5432 --name my-postgres -e POSTGRES_PASSWORD=passwort -e POSTGRES_USER=user -e POSTGRES_DB=personendb postgres`

### start the dioe db with a container link and an exposed port
`docker run -p 3333:80 --env-file=.env --link my-postgres:postgres dioe/dioe-db:stage`

### inside the container
python3 /home/docker/code/app/manage.py migrate auth
python3 /home/docker/code/app/manage.py migrate
python3 /home/docker/code/app/manage.py createsuperuser