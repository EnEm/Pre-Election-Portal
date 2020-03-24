#!/bin/bash

NAME="preelectionportal2020"                                      		# Name of the application
DJANGODIR=/home/bhasker/PycharmProjects/PreElectionPortal       # Django project directory
SOCKFILE=/home/bhasker/PycharmProjects/PreElectionPortal/run/gunicorn.sock  		# we will communicte using this unix socket
USER=bhasker                                          		# the user to run as
GROUP=bhasker                                          		# the group to run as
NUM_WORKERS=5                                       		# how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=PreElectionPortal.settings         		# which settings file should Django use
DJANGO_WSGI_MODULE=PreElectionPortal.wsgi                 		# WSGI module name

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source venv/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec ../bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-file=-
