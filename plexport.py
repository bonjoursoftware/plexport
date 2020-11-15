#!/usr/bin/env python3
# Plexport - Plex Media Server database ETL
#
# https://github.com/bonjoursoftware/plexport
#
# Copyright (C) 2020 Bonjour Software Limited
#
# https://bonjoursoftware.com/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see
# https://github.com/bonjoursoftware/plexport/blob/master/LICENSE
import argparse
import json

from typing import Any, Dict

from plexport.plex_db_transform import transform_plex_db
from plexport.plex_films_extractor import PlexFilmsExtractor


def main(args: argparse.Namespace) -> None:
    plex_films = _load_plex_db_export(args.export) if args.export else _extract_plex_films(host=args.host)
    films = transform_plex_db(plex_films)
    print(json.dumps(films))


def _load_plex_db_export(path: str) -> Dict[Any, Any]:
    with open(path, "r") as plex_db_export:
        return json.load(plex_db_export)


def _extract_plex_films(host: str) -> Dict[Any, Any]:
    return PlexFilmsExtractor(host=host).extract_plex_films()


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plexport: Plex Media Server database ETL - Bonjour Software Limited")
    parser.add_argument("--host", type=str, help="Plex server IP address")
    parser.add_argument("--export", type=str, help="Path to a Plex database export; extract step skipped if present")
    return parser.parse_args()


if __name__ == "__main__":
    main(_parse_args())
