#!/bin/sh

while ! nc -z "$PG_HOST" "$PG_PORT" ; do
  sleep 10
  printf "Database %ss:%s not ready" "$PG_HOST" "$PG_PORT"
done

exec "$@"