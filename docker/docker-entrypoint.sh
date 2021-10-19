#!/bin/bash

if [ "x$DJANGO_MANAGEPY_MIGRATE" == 'xon' ]; then
  echo "executing django migrate..."
  python manage.py migrate --noinput
else
  echo "skipping django migrate..."
fi

exec "$@"