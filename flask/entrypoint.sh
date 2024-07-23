#!/bin/bash

MAX_TRIES=10
TRY_COUNT=0
WAIT_TIME=1

while [[ $TRY_COUNT -lt $MAX_TRIES ]]; do
  if pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$POSTGRES_USER"; then
    echo "Info: Database is up and running."
    break
  else
    echo "Info: Database is not ready. Retry $((TRY_COUNT + 1))/$MAX_TRIES..."
    TRY_COUNT=$((TRY_COUNT + 1))
    sleep "$WAIT_TIME"
  fi
done

if [[ $TRY_COUNT -eq $MAX_TRIES ]]; then
  echo "Error: Timeout waiting for database to be ready"
  exit 1
fi

echo "Info: DB is ready, starting migrations"
alembic upgrade head
echo "Info: Migrations are done, starting the app"

exec "$@"
