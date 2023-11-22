#!/usr/bin/env python3
# Plexport - Plex Media Server database ETL
#
# https://github.com/bonjoursoftware/plexport
#
# Copyright (C) 2020 - 2023 Bonjour Software Limited
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
import os

from typing import Any, Dict, List, Union

from pymongo import MongoClient

from plexport.plex_db_transform import transform_plex_db
from plexport.plex_films_extractor import PlexFilmsExtractor
from plexport.plex_films_mycollections_importer import PlexFilmsMyCollectionsImporter


def main(args: argparse.Namespace) -> None:
    films = transform_plex_db(_extract_plex_films())
    print(json.dumps(films))
    if args.load:
        _import_plex_films(films)


def _extract_plex_films() -> Dict[Any, Any]:
    plex_host = os.getenv("PLEX_HOST") or input("Plex host address: ")
    return PlexFilmsExtractor(plex_host).extract_plex_films()


def _import_plex_films(films: List[Dict[str, Union[str, List[str]]]]) -> None:
    mongo_db = os.getenv("MONGO_DATABASE") or input("Database name of a MyCollections MongoDB instance: ")
    mongo_col = os.getenv("MONGO_COLLECTION") or input("Collection name of a MyCollections MongoDB instance: ")
    return PlexFilmsMyCollectionsImporter(_build_mongo_client(), mongo_db, mongo_col).import_plex_films(films)


def _build_mongo_client() -> MongoClient:
    mongo_host = os.getenv("MONGO_HOST") or input("Host address of a MyCollections MongoDB instance: ")
    mongo_user = os.getenv("MONGO_USER") or input("Username of a MyCollections MongoDB instance: ")
    mongo_password = os.getenv("MONGO_PASSWORD") or input("Password of a MyCollections MongoDB instance: ")
    return MongoClient(f"mongodb+srv://{mongo_user}:{mongo_password}@{mongo_host}/?retryWrites=true&w=majority")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plexport: Plex Media Server database ETL - Bonjour Software Limited")
    parser.add_argument("--load", action="store_true", help="Import films in a MyCollections instance if present")
    return parser.parse_args()


if __name__ == "__main__":
    main(_parse_args())
