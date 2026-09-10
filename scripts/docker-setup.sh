#!/bin/sh

set -e

docker compose up -d postgres

docker compose run --rm app python -m app.core.db.init_db
docker compose run --rm app python -m app.core.db.seed

docker compose up app