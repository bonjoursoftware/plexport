#!/usr/bin/env bash
set -euo pipefail

docker run \
  --rm \
  --network=host \
  --env PLEX_API_TOKEN="$PLEX_API_TOKEN" \
  --env PLEX_HOST="$PLEX_HOST" \
  --env MONGO_HOST="$MONGO_HOST" \
  --env MONGO_USER="$MONGO_USER" \
  --env MONGO_PASSWORD="$MONGO_PASSWORD" \
  --env MONGO_DATABASE="$MONGO_DATABASE" \
  --env MONGO_COLLECTION="$MONGO_COLLECTION" \
  bonjoursoftware/plexport:local \
  --load
