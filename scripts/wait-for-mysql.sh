#!/bin/sh

set -e

cmd="$@"

>&2 echo "Checking if Mysql is running at port"

while ! nc -z db 3306; do
  >&2 echo "Mysql is unavailable - sleeping"
  sleep 1
done;

sleep 1
>&2 echo "Mysql is up - executing command"
>&2 echo $cmd

exec $cmd
