#!/bin/bash

if [ "x$DJANGO_MANAGEPY_MIGRATE" == 'xon' ]; then
  python manage.py migrate --noinput
fi

exec "$@"