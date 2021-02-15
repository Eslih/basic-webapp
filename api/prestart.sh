#! /usr/bin/env sh

# Wait for database connection
while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  sleep 10
  printf "Database %s:%s not ready" "$PG_HOST" "$PG_PORT"
done

alembic upgrade head

exec "$@"
