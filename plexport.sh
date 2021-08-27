#!/usr/bin/env bash
set -euo pipefail

docker run \
  --rm \
  --network=host \
  --env PLEX_API_TOKEN="$PLEX_API_TOKEN" \
  bonjoursoftware/plexport:local \
  --host "$PLEX_HOST"
