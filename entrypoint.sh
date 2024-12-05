#!/bin/sh

echo "Starting entrypoint.sh"

if [ "$DATABASE" = "postgres" ]; then
  echo "Waiting for postgres..."

  while ! nc -z $SQL_HOST $SQL_PORT; do
    sleep 0.1
  done

  echo "PostgreSQL started"
fi

echo "Checking if user $POSTGRES_USER exists"
USER_EXISTS=$(psql -h $SQL_HOST -U $POSTGRES_USER -tAc "SELECT 1 FROM pg_roles WHERE rolname='$POSTGRES_USER'")
if [ "$USER_EXISTS" != "1" ]; then
  echo "User $POSTGRES_USER does not exist. Creating..."
  psql -h $SQL_HOST -U $POSTGRES_USER -c "CREATE USER $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASSWORD';"
  echo "User $POSTGRES_USER created."
else
    echo "User $POSTGRES_USER already exists."
fi

echo "Checking if database $POSTGRES_DB exists"
DB_EXISTS=$(psql -h $SQL_HOST -U $POSTGRES_USER -tAc "SELECT 1 FROM pg_database WHERE datname='$POSTGRES_DB'")
if [ "$DB_EXISTS" = "1" ]; then
  echo "Database $POSTGRES_DB does not exist. Creating..."
  psql -h $SQL_HOST -U $POSTGRES_USER -c "CREATE DATABASE $POSTGRES_DB;"
  echo "Database $POSTGRES_DB created."
else
    echo "Database $POSTGRES_DB already exists."
fi

echo "Creating the database tables..."
flask db init
flask db migrate -m "Update database"
flask db upgrade

echo "Executing command: $@"
exec "$@"