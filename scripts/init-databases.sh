#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE user_service_db;
    CREATE DATABASE email_service_db;
    CREATE DATABASE push_service_db;
    CREATE DATABASE template_service_db;
EOSQL
